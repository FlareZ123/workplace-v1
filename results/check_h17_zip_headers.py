"""Check H-17 ZIP local-header redundancy and per-member central metadata.

Read-only standard-library source audit. This does not authenticate source content.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import struct
from zipfile import ZipFile


def analyze(zip_path: Path) -> dict[str, object]:
    data = zip_path.read_bytes()
    mismatches: list[dict[str, object]] = []
    metadata: Counter[tuple[int, ...]] = Counter()
    with ZipFile(zip_path) as archive:
        entries = archive.infolist()
        for entry in entries:
            (signature, version, flags, method, dos_time, dos_date, crc,
             compressed_size, original_size, name_length, extra_length) = struct.unpack_from(
                '<4sHHHHHIIIHH', data, entry.header_offset
            )
            local_name = data[entry.header_offset + 30:entry.header_offset + 30 + name_length]
            y, mo, day, hour, minute, sec = entry.date_time
            expected_time = hour * 2048 + minute * 32 + sec // 2
            expected_date = (y - 1980) * 512 + mo * 32 + day
            checks = {
                'local_signature': signature == b'PK\x03\x04',
                'version': version == entry.extract_version,
                'flags': flags == entry.flag_bits,
                'compression': method == entry.compress_type,
                'time': dos_time == expected_time,
                'date': dos_date == expected_date,
                'crc32': crc == entry.CRC,
                'compressed_size': compressed_size == entry.compress_size,
                'original_size': original_size == entry.file_size,
                'filename': local_name == entry.filename.encode('utf-8'),
                'local_extra_absent': extra_length == 0,
            }
            for check, passes in checks.items():
                if not passes:
                    mismatches.append({'member': entry.filename, 'field': check})
            metadata[(entry.create_system, entry.create_version, entry.extract_version,
                      entry.flag_bits, entry.volume, entry.internal_attr, entry.external_attr,
                      *entry.date_time, len(entry.extra), len(entry.comment))] += 1
        return {
            'members': len(entries),
            'local_header_checks': 11 * len(entries),
            'header_mismatches': mismatches,
            'metadata_classes': len(metadata),
            'metadata_class_counts': sorted(metadata.values()),
            'zip_member_names_lexicographically_sorted': archive.namelist() == sorted(archive.namelist()),
        }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('zipfile', type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(args.zipfile), indent=2))
