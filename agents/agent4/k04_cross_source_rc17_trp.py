"""Find K04 MT19937 bridges from TRP2 control words and RC-17 footer strips.

Run: python agents/agent4/k04_cross_source_rc17_trp.py original-case.zip
Read-only original ZIP, SHA-pinned printer + recorder; selected printer row129
withheld, no REC8 commitments, no masked K04 component.
"""
import hashlib
import re
import struct
import sys
import zlib
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

AGENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(AGENTS / "agent23"), str(AGENTS / "agent6")]
from k04_mt_rowstart import SPOOL, SHA, untemper
from k04_mt_inverse_peel import inverse_twist, groups, rows
from k04_mt_ternary_class_gate import close_group

RECORDER = "evidence/recorder/trip-recorder.raw"
RECORDER_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
PROCEDURE = "evidence/procedures/RC-17-scans.txt"


def source_tokens(archive):
    recorder = archive.read(RECORDER)
    assert hashlib.sha256(recorder).hexdigest() == RECORDER_SHA
    assert recorder[:8] == b"TRP2DUMP"
    count = struct.unpack_from("<I", recorder, 12)[0]
    assert count == 88 and len(recorder) == 16 + 24 * count
    tokens = []
    for index in range(count):
        record = recorder[16 + 24 * index:16 + 24 * (index + 1)]
        _, node, event, latch, seq, raw, _, crc = struct.unpack("<IHBBI4sII", record)
        tokens.append((
            f"TRP[{index}] node={node} event={event} latch={latch} seq={seq}",
            raw,
            (zlib.crc32(record[:20]) & 0xFFFFFFFF) == crc,
        ))
    pages = archive.read(PROCEDURE).decode("utf-8").split("\f")
    assert len(pages) == 12
    for page in pages:
        tag = re.search(r"REV ([A-Z][^ /]*) / SECTION ([A-Z]+)", page)
        hexword = re.search(r"Footer control strip: ([0-9A-F]{8})", page)
        assert tag and hexword
        tokens.append((f"RC17 Rev{tag[1]} {tag[2]}", bytes.fromhex(hexword[1]), None))
    assert len(tokens) == 100
    return tokens


def source_hits(source):
    with ZipFile(source) as archive:
        spool = archive.read(SPOOL)
        assert hashlib.sha256(spool).hexdigest() == SHA
        tokens = source_tokens(archive)
    words = rows(source)
    assert len(words) == 133 and not words[129]
    observed = [(r, j, w) for r, block in enumerate(words) for j, w in enumerate(block)]
    pair_index = defaultdict(list)
    for i, (r, j, x) in enumerate(observed):
        for next_row, k, y in observed[i + 1:]:
            if next_row != r:
                pair_index[inverse_twist(x ^ y) & 0x7FFFFFFF].append(
                    (r, j, next_row, k)
                )
    assert sum(map(len, pair_index.values())) == 138336

    hits = []
    for source_name, original, crc_ok in tokens:
        word = untemper(struct.unpack("<I", original)[0])
        for r, j, next_row, k in pair_index.get(word & 0x7FFFFFFF, ()):
            hits.append((source_name, original.hex().upper(), crc_ok,
                         r, j, next_row, k))
    hits.sort()
    assert len(hits) == 9
    extra = [h for h in hits if (
        h[0].startswith("TRP[26]") or h[0].startswith("RC17")
    )]
    assert {(n, r, j, next_row, k) for n, _, _, r, j, next_row, k in extra} == {
        ("TRP[26] node=50 event=8 latch=0 seq=70", 7, 3, 38, 0),
        ("RC17 RevB PURGE", 28, 2, 59, 3),
        ("RC17 RevB VERIFY", 28, 1, 59, 2),
    }
    for entry in hits:
        print("cross_source_match", entry)
    return words, hits


def reconstructed_count(source, word_rows, use_cross_bridges):
    initial = groups(source, word_rows)
    parent = list(range(133))
    offset = [0] * 133

    def find(x):
        if parent[x] != x:
            p = parent[x]
            root = find(p)
            offset[x] += offset[p]
            parent[x] = root
        return parent[x]

    def equal(a, b, distance):
        ra, rb = find(a), find(b)
        va, vb = offset[a], offset[b]
        if ra == rb:
            assert vb - va == distance
        else:
            parent[rb] = ra
            offset[rb] = distance + va - vb

    for root, entries in initial.items():
        for row, start in entries:
            equal(root, row, start)

    if use_cross_bridges:
        # Source-conditioned MT index equalities: do not assert producer code.
        equal(9, 40, 229)   # Existing Agent2: two archive-latch controls
        equal(7, 38, 230)   # New: CRC-good node50 control
        equal(28, 59, 226) # New: two withdrawn RevB footer strips

    clusters = defaultdict(list)
    for row in range(133):
        clusters[find(row)].append((row, offset[row]))

    total = 0
    for entries in clusters.values():
        if all(not word_rows[row] for row, _ in entries):
            continue
        _, increment = close_group(entries, word_rows)
        total += increment
    return total


def main(source):
    rows_withheld, _ = source_hits(source)
    baseline = reconstructed_count(source, rows_withheld, False)
    bridged = reconstructed_count(source, rows_withheld, True)
    assert baseline == 65 and bridged == 77
    print("source_only", True, "selected_ack_row129_withheld", True)
    print("full_missing_mt_words_baseline", baseline)
    print("full_missing_mt_words_with_three_source_bridges", bridged)
    print("additional_full_missing_words", bridged - baseline)
    print("selected_K04_bytes", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_cross_source_rc17_trp.py original-case.zip")
    main(Path(sys.argv[1]))
