"""Source timestamps test a just-in-time interpretation of K04 MT cross-carrier matches.

Usage: python agents/agent43/k04_control_time_order.py original-case.zip
Selected printer row129 and all REC8 commitments are never read.
"""
import hashlib
import re
import struct
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import untemper, SHA, SPOOL
TRP_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
BRIDGES = ((26,7,3,38,0),(40,9,2,40,0),(12,9,3,40,1),
           (28,10,0,41,0),(17,10,1,41,1),(72,10,2,41,2),(45,10,3,41,3))


def inverse_twist(v):
    parity = v >> 31
    return (((v ^ (0x9908B0DF if parity else 0)) << 1) | parity) & 0xFFFFFFFF


def main(source):
    with ZipFile(source) as archive:
        spool = archive.read(SPOOL)
        recorder = archive.read("evidence/recorder/trip-recorder.raw")
    assert hashlib.sha256(spool).hexdigest() == SHA
    assert hashlib.sha256(recorder).hexdigest() == TRP_SHA
    lines = [line for line in spool.decode().splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    assert recorder[:8] == b"TRP2DUMP" and len(recorder) == 16 + 88*24

    def word(row, col):
        assert row != 129
        payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})",lines[row]).group(1))
        return untemper(struct.unpack_from("<I",payload,4*col)[0])

    valid = 0
    for record, a, j, b, k in BRIDGES:
        chunk = recorder[16+24*record:16+24*(record+1)]
        sec,node,event,latch,seq,control,aux,crc = struct.unpack("<IHBBI4sII", chunk)
        crc_ok = zlib.crc32(chunk[:20]) == crc
        source_word = untemper(struct.unpack("<I",control)[0])
        mixed = inverse_twist(word(a,j) ^ word(b,k))
        assert ((source_word ^ mixed) & 0x7FFFFFFF) == 0
        recorder_at = datetime.fromtimestamp(sec,timezone.utc)
        printer_at = datetime.fromisoformat(lines[a].split()[0])
        delay_hours = (recorder_at-printer_at).total_seconds()/3600
        assert delay_hours > 13
        valid += crc_ok
        print(record,"recorded_at",recorder_at.isoformat(),"printer_row",a,
              "printer_at",printer_at.isoformat(),"delay_hours",round(delay_hours,3),
              "crc_valid",crc_ok,"inferred_prior_mt_index",f"s{a}+{j}-396")
    assert valid == 6
    print("source_valid_controls_with_later_record_times",valid)
    print("conditional_contradiction","one chronological RNG, just-in-time source emission")
    print("possible_escape","precomputed controls, timestamp-not-generation-time, or synthetic shared provenance")
    print("selected_printer_row129_and_acceptance_excluded",True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
