"""Audit case mail-index correlation and ZIP packaging timestamps.

Read-only; all comparisons are within the preserved export, not against a
historical email server, sender receipt, printer clock, or original media.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from email.parser import BytesParser
from email.policy import default
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
import re
import struct
import zipfile


INDEX_RECORD = re.compile(r"^\\|\\s*(\\d{2})\\s*\\|\\s*(\\d{4}-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\dZ)\\s*\\|", re.MULTILINE)
MESSAGE_ID = re.compile(r"^<(\\d{2})\\.IR261003@\\[censored\\]>$")
ZIP_HEADER = struct.Struct("<IHHHHHIIIHH")


def dos_datetime(date_word: int, time_word: int) -> tuple[int, int, int, int, int, int]:
    return (
        1980 + (date_word >> 9),
        (date_word >> 5) & 15,
        date_word & 31,
        time_word >> 11,
        (time_word >> 5) & 63,
        (time_word & 31) * 2,
    )


def inspect(archive_path: Path) -> dict[str, object]:
    with zipfile.ZipFile(archive_path) as z:
        body = archive_path.read_bytes()
        members = z.infolist()
        index = z.read("evidence/mail/INDEX.md").decode("utf-8")
        indexed = {key: value for key, value in INDEX_RECORD.findall(index)}
        mail_rows: list[dict[str, object]] = []
        for number in range(1, 21):
            key = f"{number:02}"
            message = BytesParser(policy=default).parsebytes(z.read(f"evidence/mail/{key}.eml"))
            utc = parsedate_to_datetime(str(message["Date"])).astimezone(timezone.utc)
            index_utc = datetime.fromisoformat(indexed[key].replace("Z", "+00:00"))
            message_id = str(message["Message-ID"])
            id_match = MESSAGE_ID.fullmatch(message_id)
            mail_rows.append({
                "number": key,
                "date_equals_index": utc == index_utc,
                "indexed_message_id": id_match is not None and id_match.group(1) == key,
                "indexed_records_reference": str(message["X-Records-Reference"]) == f"MAIL-{key}",
                "utc": utc.isoformat().replace("+00:00", "Z"),
            })

        zip_times: list[tuple[int, int, int, int, int, int]] = []
        for member in members:
            header = ZIP_HEADER.unpack_from(body, member.header_offset)
            assert header[0] == 0x04034B50, f"Bad ZIP local signature for {member.filename}"
            local_time = dos_datetime(header[5], header[4])
            assert local_time == member.date_time, f"Local/central date mismatch for {member.filename}"
            zip_times.append(local_time)

        return {
            "zip_members": len(members),
            "zip_local_central_date_agreements": len(zip_times),
            "zip_distinct_packaging_dates": [list(t) for t in sorted(set(zip_times))],
            "mail_messages": len(mail_rows),
            "mail_index_date_agreements": sum(row["date_equals_index"] for row in mail_rows),
            "mail_numbered_message_ids": sum(row["indexed_message_id"] for row in mail_rows),
            "mail_numbered_records_refs": sum(row["indexed_records_reference"] for row in mail_rows),
            "anomalous_mail_dates": {row["number"]: row["utc"] for row in mail_rows if row["number"] in ("13", "16")},
            "mail_indexes_non_decreasing": all(
                mail_rows[i]["utc"] <= mail_rows[i + 1]["utc"]
                for i in range(len(mail_rows) - 1)
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Path to original case ZIP")
    args = parser.parse_args()
    print(json.dumps(inspect(args.archive), indent=2))


if __name__ == "__main__":
    main()
