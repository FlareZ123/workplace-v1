"""K04 cross-source MT19937 fingerprints (source-only, selected spool row withheld).

Usage: python agents/agent48/k04_recorder_bridge.py original-case.zip

This investigation does not load recovery-routing.json, acceptance.json,
K04 mask, K08 nonce, or the selected row129 printer words.
Uses Agent23's 42 recurrence witnesses and Agent31's fixed-point peeling.
"""
import re
import struct
import sys
import zlib
from pathlib import Path
from zipfile import ZipFile

here = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(here / "agent23"), str(here / "agent31")]
from k04_mt_rowstart import untemper
from k04_mt_recursive_peel import rows, groups, close_group, temper

ALL = 0xFFFFFFFF

def main(source: Path) -> None:
    values = rows(source)
    assert len(values) == 133 and values[129] == []
    entries = groups(source, values)
    states = {root: close_group(group, values)[0] for root, group in entries.items()}

    with ZipFile(source) as archive:
        raw = archive.read("evidence/recorder/trip-recorder.raw")
        spool = archive.read("evidence/print/spool-reconstruction.log").decode("ascii")
    header, version, size, count = struct.unpack_from("<8sHHI", raw)
    assert (header, version, size, count) == (b"TRP2DUMP", 2, 24, 88)
    assert len(raw) == 16 + size * count
    source_lines = [line for line in spool.splitlines() if line.startswith("2026-")]
    assert len(source_lines) == 133

    hits = []
    for record in range(count):
        start = 16 + record * size
        sec, node, event, latch, seq, control, aux, crc = struct.unpack_from("<IHBBI4sII", raw, start)
        if node != 49 or event != 82:
            continue
        word = untemper(int.from_bytes(control, "little"))
        crc_good = (zlib.crc32(raw[start:start + 20]) & ALL) == crc
        for root, state in states.items():
            for pos, (known, bits) in state.items():
                if known.bit_count() < 31:
                    continue
                if (word ^ bits) & known:
                    continue
                hits.append((root, pos, record, seq, latch,
                             control.hex().upper(), known.bit_count(), crc_good))

    hits.sort(key=lambda v: v[1])
    assert len(hits) == 4, hits
    observed = [(pos, record, seq, hexword, bits, valid)
                for _, pos, record, seq, _, hexword, bits, valid in hits]
    expected = [
        (-623, 28, 992, "9359AC1F", 32, True),
        (-622, 17, 203, "BFB00270", 32, True),
        (-621, 72, 903, "F2595C84", 32, False),
        (-620, 45, 993, "30D78977", 31, True),
    ]
    assert observed == expected, (observed, expected)
    assert len({root for root, *_ in hits}) == 1
    row41_group = next(group for group in entries.values()
                       if any(row == 41 for row, _ in group))
    row41_root = next(root for root, group in entries.items() if group is row41_group)
    assert hits[0][0] == row41_root
    print("cross_source_recorder_fingerprint_count", len(hits))
    for root, pos, record, seq, latch, word, nbits, valid in hits:
        print("mt_relative_position", pos, "recorder_row", record,
              "sequence", seq, "latch", latch, "control_bytes", word,
              "independently_known_bits", nbits, "crc_ok", valid)
    print("fourth_untempered_state", f"{untemper(0x7789D730):08X}")
    print("source_scope", "TRP2 node49/event82 controls and unselected printer rows")
    print("K04_K08_UNRESOLVED")

    # Two additional model-dependent hidden outputs: the first accepted
    # post-payload destination sampler for rows21 and22.
    destination = {"store": 0, "desk": 1, "bench": 2}
    for row, offset, expected_output, first_reject in (
        (21, 4, 0x9ACC8EED, False),
        (22, 5, 0xADFF876E, True),
    ):
        group = next(e for e in entries.values() if any(r == row for r, _ in e))
        state, _ = close_group(group, values)
        start = next(p for r, p in group if r == row)
        if first_reject:
            mask0, value0 = state[start + 4]
            assert mask0 == ALL and (temper(value0) >> 30) == 3
        mask, value = state[start + offset]
        assert mask == 0x7FFFFFFF
        label = re.search(r"DEST=([a-z]+)", source_lines[row]).group(1)
        possibilities = [temper(value | (bit << 31)) >> 30 for bit in (0, 1)]
        assert sorted(possibilities) == [0, 2] and destination[label] == 2
        winning = next(bit for bit in (0, 1)
                       if (temper(value | (bit << 31)) >> 30) == destination[label])
        predicted = temper(value | (winning << 31))
        assert predicted == expected_output
        print("inferred_after_row", row, "draw_offset", offset,
              "generator_word", f"{predicted:08X}", "conditional_on_DEST_sampler", True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_recorder_bridge.py original-case.zip")
    main(Path(sys.argv[1]))
