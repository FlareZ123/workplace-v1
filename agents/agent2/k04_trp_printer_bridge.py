"""Source-only K04 MT19937 recorder/printer hidden-word bridge.

Run: python agents/agent2/k04_trp_printer_bridge.py original-case.zip
Selected ACK row129 and all acceptance commitments are withheld.
"""
import hashlib
import re
import struct
import sys
import zlib
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import untemper
from k04_mt_inverse_peel import inverse_twist

SPOOL = "evidence/print/spool-reconstruction.log"
TRP = "evidence/recorder/trip-recorder.raw"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def main(source):
    with ZipFile(source) as archive:
        spool = archive.read(SPOOL)
        recorder = archive.read(TRP)
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert recorder[:8] == b"TRP2DUMP"
    count = struct.unpack_from("<I", recorder, 12)[0]
    assert len(recorder) == 16 + 24 * count
    lines = [line for line in spool.decode().splitlines()
             if line.startswith("2026-")]
    assert len(lines) == 133

    words = []
    for row, line in enumerate(lines):
        if row == 129:
            continue
        payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))
        for j, value in enumerate(struct.unpack("<4I", payload)):
            words.append((row, j, untemper(value)))

    control = defaultdict(list)
    for i in range(count):
        rec = recorder[16 + 24*i:16 + 24*(i+1)]
        stamp, node, event, latch, seq, raw, aux, crc = struct.unpack("<IHBBI4sII", rec)
        if node == 49 and event == 82:
            value = untemper(struct.unpack("<I", raw)[0])
            control[value & 0x7FFFFFFF].append(
                (i, seq, latch, value, (zlib.crc32(rec[:20]) & 0xFFFFFFFF) == crc))
    assert sum(map(len, control.values())) == 16

    hits = []
    for a, (row, j, x) in enumerate(words):
        for nextrow, k, y in words[a+1:]:
            if row == nextrow:
                continue
            implied = inverse_twist(x ^ y)
            for i, seq, latch, actual, valid in control.get(implied & 0x7FFFFFFF, ()):
                hits.append((i, seq, latch, row, j, nextrow, k, actual,
                             implied, valid))
    assert [(s, r, j, t, k) for _,s,_,r,j,t,k,_,_,_ in hits] == [
        (990,9,2,40,0), (201,9,3,40,1),
        (992,10,0,41,0), (203,10,1,41,1),
        (903,10,2,41,2), (993,10,3,41,3)]
    assert sum(valid for *_, valid in hits) == 5
    for i, seq, latch, row, j, nextrow, k, actual, implied, valid in hits:
        print("TRP",i,"seq",seq,"latch",latch,
              "printer_pair",f"{row}.{j}",f"{nextrow}.{k}",
              "observed32",f"{actual:08X}","implied31",
              f"{implied & 0x7FFFFFFF:08X}","valid_crc",valid)
    print("source_only",True,"selected_ACK_row129_withheld",True)
    print("TRP_sha256",hashlib.sha256(recorder).hexdigest())
    print("total_hidden_word_matches",len(hits),
          "valid_crc_matches",sum(v[-1] for v in hits))
    print("K04_K08","UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_trp_printer_bridge.py original-case.zip")
    main(Path(sys.argv[1]))
