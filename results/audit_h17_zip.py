"""Read-only structural and raw-DEFLATE forensic audit of H-17 ZIP.

The optional compiled zlib helper measure_raw_deflate_slack.c exposes the
unused bit count at each stream's final DEFLATE block boundary. This is
only a check of obvious standard-container hiding locations; it cannot
rule out arbitrary content or compressed-data steganography.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import zipfile
import zlib


def audit(path: Path, helper: Path | None = None) -> dict[str, object]:
    data = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        members = sorted(archive.infolist(), key=lambda member: member.header_offset)
        crc_failure = archive.testzip()
        anomalies: list[str] = []
        slack_distribution: Counter[int] = Counter()
        nonzero_slack: list[str] = []
        previous_end = 0
        extra_payload_bytes = 0
        for member in members:
            offset = member.header_offset
            header = struct.unpack_from("<IHHHHHIIIHH", data, offset)
            signature, _, flags, method, _, _, _, compressed_size, size, name_bytes, extra_bytes = header
            if signature != 0x04034B50:
                raise ValueError(f"invalid local header for {member.filename}")
            if offset != previous_end:
                anomalies.append(f"unreferenced gap before {member.filename}: {offset - previous_end} bytes")
            if flags & 1 or member.flag_bits & 1:
                anomalies.append(f"encrypted entry: {member.filename}")
            if method != 8 or member.compress_type != 8:
                anomalies.append(f"non-DEFLATE member: {member.filename}")
            if member.extra or member.comment or extra_bytes:
                anomalies.append(f"extra/comment metadata: {member.filename}")
            if compressed_size != member.compress_size or size != member.file_size:
                anomalies.append(f"local/central size disagreement: {member.filename}")
            start = offset + 30 + name_bytes + extra_bytes
            compressed = data[start:start + compressed_size]
            previous_end = start + compressed_size
            d = zlib.decompressobj(-15)
            actual = d.decompress(compressed) + d.flush()
            extra_payload_bytes += len(d.unused_data) + len(d.unconsumed_tail)
            if not d.eof or actual != archive.read(member):
                anomalies.append(f"DEFLATE decoding mismatch: {member.filename}")
            if helper is not None:
                result = subprocess.run([str(helper)], input=compressed,
                                        capture_output=True, check=True)
                rc, flags, consumed, produced, boundary = map(int, result.stdout.split())
                unused = flags & 63
                if rc not in (0, 1) or not (flags & 128) or boundary != 1:
                    anomalies.append(f"missing final block boundary: {member.filename}")
                if consumed != compressed_size or produced != member.file_size or unused > 7:
                    anomalies.append(f"incorrect final stream measurement: {member.filename}")
                slack_distribution[unused] += 1
                high_bits = (compressed[-1] >> (8 - unused)) if unused else 0
                if high_bits:
                    nonzero_slack.append(member.filename)
        if previous_end != archive.start_dir:
            anomalies.append(f"gap before central directory: {archive.start_dir - previous_end} bytes")
        eocd = data.rfind(b"PK\x05\x06")
        if eocd < 0:
            raise ValueError("EOCD signature not found")
        comment_length = struct.unpack_from("<H", data, eocd + 20)[0]
        trailing_bytes = len(data) - (eocd + 22 + comment_length)
        if trailing_bytes:
            anomalies.append(f"trailing bytes: {trailing_bytes}")
        if archive.comment:
            anomalies.append("archive comment present")
        return {
            "zip_sha256": hashlib.sha256(data).hexdigest(),
            "members": len(members),
            "unique_names": len(set(archive.namelist())),
            "crc_failure_member": crc_failure,
            "central_directory_start": archive.start_dir,
            "eocd_offset": eocd,
            "size_bytes": len(data),
            "extra_compressed_trailer_bytes": extra_payload_bytes,
            "padding_counts_by_unused_bits": dict(sorted(slack_distribution.items())) if helper else None,
            "total_unused_padding_bits": sum(k * v for k, v in slack_distribution.items()) if helper else None,
            "nonzero_padding_members": nonzero_slack if helper else None,
            "anomalies": anomalies,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zipfile", type=Path)
    parser.add_argument("--inflate-helper", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.zipfile, args.inflate_helper), indent=2))


if __name__ == "__main__":
    main()
