"""Extend the K04 printer/recorder MT bridge to all TRP2 control-word records.

Usage: python agents/agent47/k04_all_trp_bridge.py ORIGINAL_CASE.zip
Purely local read-only analysis; selected printer ACK row129 and REC8 commitments
remain unused. Imports the existing source-only MT witnesses and closure code.
"""
import hashlib
import re
import struct
import sys
import zlib
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "agent23"))
sys.path.insert(0, str(HERE.parents[1] / "agent6"))
from k04_mt_rowstart import untemper
from k04_mt_inverse_peel import inverse_twist, rows, groups
from k04_mt_ternary_class_gate import close_group

SPOOL = "evidence/print/spool-reconstruction.log"
RECORDER = "evidence/recorder/trip-recorder.raw"
SHA_SPOOL = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
LOW31 = 0x7FFFFFFF


def discover_controls(source):
    with ZipFile(source) as archive:
        raw_spool = archive.read(SPOOL)
        raw_trp = archive.read(RECORDER)
    assert hashlib.sha256(raw_spool).hexdigest() == SHA_SPOOL
    assert raw_trp[:8] == b"TRP2DUMP"
    count = struct.unpack_from("<I", raw_trp, 12)[0]
    assert count == 88 and len(raw_trp) == 16 + 24 * count

    by_low31 = defaultdict(list)
    for i in range(count):
        chunk = raw_trp[16 + 24*i : 16 + 24*(i+1)]
        _, node, event, _, seq, opaque, _, crc = struct.unpack("<IHBBI4sII", chunk)
        x = untemper(struct.unpack("<I", opaque)[0])
        valid = zlib.crc32(chunk[:20]) == crc
        by_low31[x & LOW31].append((i, node, event, seq, x, valid))

    lines = [s for s in raw_spool.decode().splitlines() if s.startswith("2026-")]
    assert len(lines) == 133
    printer = []
    for row, line in enumerate(lines):
        if row == 129:
            continue
        payload = bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})", line).group(1))
        for j, word in enumerate(struct.unpack("<4I", payload)):
            printer.append((row, j, untemper(word)))

    hits = []
    for i, (arow, acol, a) in enumerate(printer):
        for brow, bcol, b in printer[i+1:]:
            if arow == brow:
                continue
            inferred = inverse_twist(a ^ b)
            for rid, node, event, seq, observed, valid in by_low31.get(inferred & LOW31, ()):
                hits.append((rid, node, event, seq, arow, acol, brow, bcol,
                             observed, inferred, valid))
    return hits


def main(path):
    matches = discover_controls(path)
    assert len(matches) == 7
    novel = [h for h in matches if h[0] == 26]
    assert len(novel) == 1
    rid, node, event, seq, row_a, col_a, row_b, col_b, observed, inferred, valid = novel[0]
    assert (rid, node, event, seq, row_a, col_a, row_b, col_b, valid) == (
        26, 50, 8, 70, 7, 3, 38, 0, True)
    assert observed == 0xBBC259FD and inferred == 0x3BC259FD

    words = rows(path)
    clusters = list(groups(path, words).values())
    baseline = sum(close_group(g, words)[1] for g in clusters)
    assert baseline == 65
    ga = next(g for g in clusters if any(r == 7 for r, _ in g))
    gb = next(g for g in clusters if any(r == 38 for r, _ in g))
    assert ga is not gb
    s7 = next(s for r, s in ga if r == 7)
    s38 = next(s for r, s in gb if r == 38)
    # Printer middle row7 word3 at k+397, end row38 word0 at k+624.
    # Hence s38 - s7 = 227 + 3 - 0 = 230.
    merged = ga + [(r, s + s7 + 230 - s38) for r, s in gb]
    full, new_recovered = close_group(merged, words)
    total = (baseline - close_group(ga, words)[1]
             - close_group(gb, words)[1] + new_recovered)
    assert total == 70

    expected = {-395: 0x2F9F1C79, -394: 0x4373C70C,
                397: 0x80621516, 398: 0xD867C1A3, 399: 0xE34440AD}
    for relative, word in expected.items():
        assert full[s7 + relative] == word

    print("source_only", True, "selected_ack_row129_withheld", True)
    print("opaque_controls", 88, "matching_pairs", len(matches))
    print("new_crc_valid_trp", rid, "node", node, "event", event, "seq", seq)
    print("pair", f"{row_a}.{col_a}", f"{row_b}.{col_b}")
    print("observed_untempered32", f"{observed:08X}",
          "inverse_mixed31", f"{inferred & LOW31:08X}")
    print("model_conditional_s38_minus_s7", 230)
    print("reconstructed_full_words", baseline, "->", total)
    print("five_extra", {str(k): f"{v:08X}" for k, v in expected.items()})
    print("K04/K08", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_all_trp_bridge.py ORIGINAL_CASE.zip")
    main(Path(sys.argv[1]))
