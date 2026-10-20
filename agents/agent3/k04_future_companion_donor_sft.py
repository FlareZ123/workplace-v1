"""Conditional K04 future-donor companion signature gate; original source only.

Usage: python agents/agent3/k04_future_companion_donor_sft.py original-case.zip
Excludes selected row129, K04 mask/digest, K08 nonce/caption and verifier.
"""
import hashlib
import json
import re
import struct
import sys
import zipfile
import zlib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from agents.agent33.k04_global_target_projection import source_rows, state_expressions, untemper, temper

TRP_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
AX_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"
DONORS = (1185, 1411, 1412, 1865, 1866, 1974)


def original_future_masks(case_path, starts):
    terms = state_expressions(1982)
    basis = {}

    def reduce(expr, bit=0):
        v = (expr << 1) | (bit & 1)
        while v:
            old = basis.get(v.bit_length() - 1)
            if old is None:
                return v
            v ^= old
        return 0

    for rownum, row in enumerate(source_rows(case_path)):
        for j, word in enumerate(row):
            for bit, expr in enumerate(terms[starts[rownum] + j]):
                v = reduce(expr, word >> bit)
                assert v != 1, (rownum, j, bit)
                if v:
                    basis[v.bit_length() - 1] = v
    assert len(basis) == 15305, len(basis)
    result = {}
    for i in range(970, 1983):
        v = [reduce(expr) for expr in terms[i]]
        result[i] = (
            sum(1 << b for b, x in enumerate(v) if x in (0, 1)),
            sum(x << b for b, x in enumerate(v) if x in (0, 1)),
        )
    return result


def target_windows(masks):
    windows = []
    for length in (3, 4, 5):
        for donor in DONORS:
            for start in range(max(971, donor - length + 1), donor + 1):
                companions = [(i, *masks[i]) for i in range(start, start + length)
                              if i != donor and masks[i][0]]
                bits = sum(mask.bit_count() for _, mask, _ in companions)
                if bits >= 48:
                    windows.append((length, donor, start, companions, bits))
    assert len(windows) == 25
    assert any(donor == 1974 and bits == 65 for _, donor, _, _, bits in windows)
    return windows


def recorder_runs(raw):
    assert hashlib.sha256(raw).hexdigest() == TRP_SHA
    assert len(raw) == 16 + 88 * 24
    by_node, by_pair = defaultdict(dict), defaultdict(dict)
    for recnum in range(88):
        rec = raw[16 + 24 * recnum:16 + 24 * (recnum + 1)]
        _, node, event, _, seq, opaque, _, crc = struct.unpack("<IHBBI4sII", rec)
        valid = zlib.crc32(rec[:20]) == crc
        by_node[node][seq] = (opaque, valid, event)
        by_pair[(node, event)][seq] = (opaque, valid, event)
    runs = []
    for groups, label in ((by_pair, "node,event"), (by_node, "node")):
        for group, entries in groups.items():
            for start in sorted(entries):
                for length in (3, 4, 5):
                    if all(s in entries for s in range(start, start + length)):
                        values = tuple(entries[s][0] for s in range(start, start + length))
                        runs.append((f"TRP2 {label}={group} seq={start} length={length}", values))
    return runs


def procedure_runs(raw):
    by_rev, scan = defaultdict(dict), defaultdict(list)
    for page in raw.decode().split("\f"):
        a = re.search(r"REV (B|C|D-draft) / SECTION (DRAIN|ISOLATE|PURGE|VERIFY)", page)
        b = re.search(r"Footer control strip: ([A-F0-9]{8})", page)
        if a and b:
            revision, section = a.groups()
            value = bytes.fromhex(b.group(1))
            by_rev[revision][section] = value
            scan[revision].append(value)
    assert set(by_rev) == {"B", "C", "D-draft"}
    result = []
    for rev, entries in by_rev.items():
        assert len(entries) == 4
        service = tuple(entries[s] for s in ("DRAIN", "ISOLATE", "PURGE", "VERIFY"))
        result.extend(((f"RC17 {rev} service", service), (f"RC17 {rev} scanner", tuple(scan[rev]))))
    return result


def transfer_runs(raw):
    assert hashlib.sha256(raw).hexdigest() == AX_SHA
    grouped = defaultdict(lambda: defaultdict(dict))
    for line in raw.decode().splitlines():
        entry = json.loads(line)
        if entry.get("kind") == "CHUNK":
            grouped[entry["transfer"]][entry["seq"]][entry["attempt"]] = bytes.fromhex(entry["checkpoint"])
    assert len(grouped) == 4
    result = []
    for transfer, seqs in grouped.items():
        assert set(seqs) == set(range(8))
        for policy in ("first", "last"):
            values = {seq: alternatives[min(alternatives) if policy == "first" else max(alternatives)]
                      for seq, alternatives in seqs.items()}
            for start in range(8):
                for length in (3, 4, 5):
                    if all(i in values for i in range(start, start + length)):
                        result.append((f"{transfer} {policy} seq{start} len{length}",
                                       tuple(values[i] for i in range(start, start + length))))
    return result


def full_match(values, byteorder, start, companions):
    observed = [untemper(int.from_bytes(v, byteorder)) for v in values]
    return all(observed[index - start] & mask == val for index, mask, val in companions)


def half_match(values, byteorder, start, companions):
    observed = [int.from_bytes(v, byteorder) for v in values]
    return all(observed[index - start] == temper(val) >> 16 for index, _, val in companions)


def main(path):
    starts = json.loads((ROOT / "results/h17-k04-source-consistent-index955.json").read_text())["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    masks = original_future_masks(path, starts)
    windows = target_windows(masks)
    with zipfile.ZipFile(path) as z:
        trp = z.read("evidence/recorder/trip-recorder.raw")
        rc = z.read("evidence/procedures/RC-17-scans.txt")
        ax = z.read("evidence/transfers/transfer-audit.jsonl")
    full_runs = recorder_runs(trp) + procedure_runs(rc)
    full_tests = 0
    full_hits = []
    for name, values in full_runs:
        for length, donor, start, companions, fixed_bits in windows:
            if length != len(values):
                continue
            for byteorder in ("little", "big"):
                full_tests += 1
                if full_match(values, byteorder, start, companions):
                    full_hits.append((name, donor, start, byteorder, fixed_bits))
    half_runs = transfer_runs(ax)
    half_tests = 0
    half_hits = []
    for name, values in half_runs:
        for length, donor, start, companions, _ in windows:
            if length != len(values) or sum(mask == 0xFFFFFFFF for _, mask, _ in companions) < 3:
                continue
            for byteorder in ("little", "big"):
                half_tests += 1
                if half_match(values, byteorder, start, companions):
                    half_hits.append((name, donor, start, byteorder))
    assert full_tests == 3748, full_tests
    assert half_tests == 480, half_tests

    # Separate two-full-companion upper16 recognizer, particularly X1866.
    # This is a 32-bit recognition signature whose two complete companions
    # were excluded by the stricter three-full-companion gate above.
    twin_windows = []
    for length in (3, 4, 5):
        for donor in DONORS:
            for start in range(max(971, donor - length + 1), donor + 1):
                full_companions = tuple((i, *masks[i]) for i in range(start, start + length)
                                        if i != donor and masks[i][0] == 0xFFFFFFFF)
                if len(full_companions) >= 2:
                    twin_windows.append((length, donor, start, full_companions))
    assert len(twin_windows) == 24
    assert sum(donor == 1866 for _, donor, _, _ in twin_windows) == 6
    twin_tests = 0
    twin_hits = []
    for name, values in half_runs:
        for length, donor, start, full_companions in twin_windows:
            if length != len(values):
                continue
            for byteorder in ("little", "big"):
                twin_tests += 1
                if half_match(values, byteorder, start, full_companions):
                    twin_hits.append((name, donor, start, byteorder))
    assert twin_tests == 1760, twin_tests
    twin = next(w for w in twin_windows if w[1] == 1866 and w[2] == 1866 and w[0] == 3)
    length, donor, start, full_companions = twin
    control = [bytes.fromhex("7CA7") for _ in range(length)]
    for index, _, value in full_companions:
        control[index - start] = (temper(value) >> 16).to_bytes(2, "little")
    assert half_match(control, "little", start, full_companions)

    # Synthetic calibration: withheld arbitrary first donor, forced subsequent words.
    length, donor, start, companions, _ = next(
        w for w in windows if w[1] == 1412 and w[2] == 1412 and w[0] == 4)
    x = [bytes.fromhex("78563412") for _ in range(length)]
    for index, _, v in companions:
        x[index - start] = temper(v).to_bytes(4, "little")
    assert full_match(x, "little", start, companions)
    length, donor, start, companions, _ = next(
        w for w in windows if w[1] == 1185 and w[2] == 1185 and w[0] == 5)
    y = [bytes.fromhex("7CA7") for _ in range(length)]
    for index, _, v in companions:
        y[index - start] = (temper(v) >> 16).to_bytes(2, "little")
    assert half_match(y, "little", start, companions)
    assert untemper(temper(0x12345678)) == 0x12345678

    result = {
        "model": "conditional original source-consistent MT19937 p955",
        "target_informative_future_positions": DONORS,
        "source_anchored_windows": len(windows),
        "original_fullword_comparisons": full_tests,
        "original_fullword_matches": full_hits,
        "original_AX_comparisons": half_tests,
        "original_AX_matches": half_hits,
        "original_AX_twin_companion_windows": len(twin_windows),
        "original_AX_twin_comparisons": twin_tests,
        "original_AX_twin_matches": twin_hits,
        "synthetic_controls": "PASS",
        "new_K04_target_bits": 0,
        "new_K08_exact_words": 0,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python agents/agent3/k04_future_companion_donor_sft.py original-case.zip")
    main(Path(sys.argv[1]))
