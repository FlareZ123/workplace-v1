"""Check source-anchored K04 four-control-word donor permutations.

Run: python agents/agent8/k04_recorder_quadruple_donor.py original-case.zip
Read-only: does not modify the source, mask, commitments, or candidate.
The selected printer row129 does not enter this donor-word experiment.

Prior printer/recorder MT witness identifies four physically nonadjacent
TRP2 control words (record indices 28,17,72,45) as a four-word output run.
Test whether any four distinct node49/event82 control words, in *any* order,
provide the K04 coupon payload under the original XOR rule.
"""
import hashlib
import itertools
import json
import struct
import sys
import zipfile
import zlib

ARCHIVE_LATCH = (49, 82)
POSITIVE_CONTROL_ORDER = (28, 17, 72, 45)


def run(path):
    with zipfile.ZipFile(path) as archive:
        routing = json.loads(archive.read("evidence/recovery-routing.json"))
        acceptance = json.loads(archive.read("acceptance.json"))
        raw = archive.read("evidence/recorder/trip-recorder.raw")

    assert raw[:8] == b"TRP2DUMP"
    version, size, count = struct.unpack_from("<HHI", raw, 8)
    assert (version, size) == (2, 24)
    assert len(raw) == 16 + size * count
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    expected = acceptance["slot_sha256"]["K04"]
    records = []

    for index in range(count):
        record = raw[16 + index * size:16 + (index + 1) * size]
        _, node, event, _, sequence = struct.unpack_from("<IHBBI", record)
        if (node, event) != ARCHIVE_LATCH:
            continue
        crc = zlib.crc32(record[:20])
        stored_crc = struct.unpack_from("<I", record, 20)[0]
        records.append((index, sequence, crc == stored_crc, record[12:16]))

    assert len(records) == 16
    known = [next(record for record in records if record[0] == i)
             for i in POSITIVE_CONTROL_ORDER]
    assert len({r[0] for r in known}) == 4
    assert not known[2][2]  # The historically observed matching retry has bad CRC.

    def digest(words):
        raw_payload = b"".join(record[3] for record in words)
        component = bytes(a ^ b for a, b in zip(raw_payload, mask))
        return hashlib.sha256(component).hexdigest()

    synthetic = digest(known)
    assert synthetic != expected
    print("records", count, "archive_latch", len(records))
    print("source_quadruple", [(r[0], r[1], r[2]) for r in known])

    for include_bad in (False, True):
        permitted = [record for record in records if include_bad or record[2]]
        matches = []
        control_matches = []
        count_tested = 0
        for ordering in itertools.permutations(permitted, 4):
            value = digest(ordering)
            ids = [r[0] for r in ordering]
            if value == expected:
                matches.append(ids)
            if value == synthetic:
                control_matches.append(ids)
            count_tested += 1

        print("include_bad_crc", include_bad, "assignments", count_tested,
              "K04_commitment_matches", matches, "synthetic_control", control_matches)
        assert control_matches == (
            [list(POSITIVE_CONTROL_ORDER)] if include_bad else []
        )

    print("Note: zero matches excludes only directly concatenated four-control-word donors.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_recorder_quadruple_donor.py original-case.zip")
    run(sys.argv[1])
