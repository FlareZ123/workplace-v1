"""K04 targeted selected-ACK source corroboration through independent MT witnesses.

Usage: python agents/agent8/k04_selected_ack_crosscarrier.py ORIGINAL_CASE_ZIP
This uses the disputed source bytes only as a candidate source-control observation.
It never reads original acceptance/verify and cannot assert integrity of the ACK.
"""
import collections
import re
import struct
import sys
import zipfile

from k04_new_donor_carriers_sft import LOW, untemper, inverse_pair, original_rows, pair_index


def main(source):
    with zipfile.ZipFile(source) as z:
        spool = z.read("evidence/print/spool-reconstruction.log").decode("utf-8")
        payloads = re.findall(r"PAYLOAD=([A-F0-9]{32})", spool)
        assert len(payloads) == 133
        selected = tuple(untemper(x) for x in struct.unpack("<4I", bytes.fromhex(payloads[129])))
        intact = original_rows(z)
        assert not intact[129]
        index = pair_index(intact)
        as_successor = [(j, location) for j, state in enumerate(selected)
                        for location in index.get(state & LOW, ())]
        print("selected_ACK_original_untempered_words", [f"{x:08X}" for x in selected])
        print("selected_as_low31_predecessor_source_links", len(as_successor), as_successor)

        rec = z.read("evidence/recorder/trip-recorder.raw")
        assert rec[:8] == b"TRP2DUMP" and len(rec) == 16 + 88 * 24
        control_values = []
        for i in range(88):
            block = rec[16 + 24 * i + 12:16 + 24 * i + 16]
            for endian in ("little", "big"):
                control_values.append(("TRP2", i, endian, untemper(int.from_bytes(block, endian)) & LOW))

        scans = z.read("evidence/procedures/RC-17-scans.txt").decode("utf-8")
        strips = re.findall(r"(?<![0-9A-F])[0-9A-F]{8}(?![0-9A-F])", scans)
        assert len(strips) == 12
        for i, value in enumerate(strips):
            block = bytes.fromhex(value)
            for endian in ("little", "big"):
                control_values.append(("RC17", i, endian, untemper(int.from_bytes(block, endian)) & LOW))

        by_low = collections.defaultdict(list)
        for kind, i, endian, low in control_values:
            by_low[low].append((kind, i, endian))

        as_end = []
        for j, e in enumerate(selected):
            for row in range(129):
                for k, m in enumerate(intact[row]):
                    for control in by_low.get(inverse_pair(m, e) & LOW, ()):
                        as_end.append((j, row, k, control))
        as_middle = []
        for j, m in enumerate(selected):
            for row in (130, 131, 132):
                for k, e in enumerate(intact[row]):
                    for control in by_low.get(inverse_pair(m, e) & LOW, ()):
                        as_middle.append((j, row, k, control))

        record28 = rec[16 + 28 * 24 + 12:16 + 28 * 24 + 16]
        known_low = untemper(int.from_bytes(record28, "little")) & LOW
        assert (10, 0, 41, 0) in index.get(known_low, ())
        print("original_rec28_positive_control", "PASS")
        print("source_control_orientations", len(control_values), "full_nonselected_pair_count", sum(map(len, index.values())))
        print("selected_as_MT_end_with_independent_low31_matches", len(as_end), as_end)
        print("selected_as_MT_middle_with_independent_low31_matches", len(as_middle), as_middle)
        assert not as_successor and not as_end and not as_middle
        print("NO_NEW_CROSS_SOURCE_SELECTED_ACK_LINK; NO_REC8_ACCEPTANCE_CLAIM")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python k04_selected_ack_crosscarrier.py ORIGINAL_CASE_ZIP")
    main(sys.argv[1])
