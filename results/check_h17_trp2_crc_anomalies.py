"""Read-only independent audit of H-17 TRP2 checksum anomalies."""
import hashlib
import json
from pathlib import Path
import struct
import zlib
from datetime import datetime, timezone

base = Path(__file__).resolve().parents[1]
root = base / "resources" if (base / "resources").exists() else base
data = (root / "evidence/recorder/trip-recorder.raw").read_bytes()
assert hashlib.sha256(data).hexdigest() == "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
assert struct.unpack_from("<8sHHI", data) == (b"TRP2DUMP", 2, 24, 88)

valid, bad, good_selections, all_selections = 0, [], {}, {}
for index in range(88):
    frame = data[16 + index * 24:16 + (index + 1) * 24]
    stamp, node, event, latch, sequence = struct.unpack_from("<IHBBI", frame)
    computed, recorded = zlib.crc32(frame[:20]), struct.unpack_from("<I", frame, 20)[0]
    is_valid = computed == recorded
    valid += is_valid
    if not is_valid:
        bad.append((index, stamp, latch, sequence, f"{computed ^ recorded:08X}"))
    if node == 49 and event == 82 and 1791062040 <= stamp < 1791062048:
        row = (sequence, frame[12:16].hex().upper())
        if is_valid and (latch not in good_selections or row > good_selections[latch]):
            good_selections[latch] = row
        if latch not in all_selections or row > all_selections[latch]:
            all_selections[latch] = row

assert valid == 84
assert [r[0] for r in bad] == [14, 41, 72, 77]
assert {r[4] for r in bad} == {"00000100"}
make = lambda rows: "".join(rows[i][1] for i in range(4))
correct, no_crc = make(good_selections), make(all_selections)
assert correct == "FF8B78200A56E8586DCDA00EF01E4572"
assert no_crc == "C2DE39CCBA1947822A4EE66DF2595C84"
target = json.loads((root / "acceptance.json").read_text())["slot_sha256"]["K05"]
assert hashlib.sha256(bytes.fromhex(correct)).hexdigest() == target
assert hashlib.sha256(bytes.fromhex(no_crc)).hexdigest() != target
print(json.dumps({"valid_crc": valid, "bad_rows": bad, "correct_K05": correct,
                  "unvalidated_K05": no_crc, "original_slot": "PASS",
                  "without_crc": "NO_MATCH"}, indent=2))
