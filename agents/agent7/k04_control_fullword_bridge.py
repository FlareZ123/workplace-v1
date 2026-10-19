"""Promote source-matched MT ancestor control words from 31 to 32 bits.

Run: python agents/agent7/k04_control_fullword_bridge.py original-case.zip
Requires pre-existing Agent 4, 6 and 23 source-only modules.
Withholds selected spool row129. Reads no acceptance commitments or masks.
"""
import sys
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(root / "agent4"), str(root / "agent6"),
                str(root / "agent23")]
from k04_cross_source_rc17_trp import source_hits
from k04_mt_inverse_peel import groups
from k04_mt_ternary_class_gate import close_group
from k04_mt_rowstart import untemper

ALL = 0xFFFFFFFF
LOW31 = 0x7FFFFFFF


class RelativePositions:
    def __init__(self, count):
        self.parent = list(range(count))
        self.offset = [0] * count

    def find(self, index):
        parent = self.parent[index]
        if parent != index:
            root = self.find(parent)
            self.offset[index] += self.offset[parent]
            self.parent[index] = root
        return self.parent[index]

    def equal(self, first, second, delta):
        a = self.find(first)
        b = self.find(second)
        first_offset = self.offset[first]
        second_offset = self.offset[second]
        if a == b:
            assert second_offset - first_offset == delta
        else:
            self.parent[b] = a
            self.offset[b] = delta + first_offset - second_offset

    def clusters(self):
        out = defaultdict(list)
        for row in range(len(self.parent)):
            out[self.find(row)].append((row, self.offset[row]))
        return out


def analyze(source):
    # Agent 4's source-pinned fingerprint returns all nine matched carriers,
    # including revoked RC-17 and a TRP2 sample with a bad source CRC.
    word_rows, hits = source_hits(source)
    assert len(hits) == 9 and word_rows[129] == []

    relations = RelativePositions(len(word_rows))
    for root_row, entries in groups(source, word_rows).items():
        for row, relative_index in entries:
            relations.equal(root_row, row, relative_index)

    for name, data, crc_ok, first, j, second, k in hits:
        relations.equal(first, second, 227 + j - k)

    states = {}
    baseline_hidden = 0
    for group_root, entries in relations.clusters().items():
        state, increment = close_group(entries, word_rows)
        states[group_root] = state
        baseline_hidden += increment
    assert baseline_hidden == 77

    previously_complete = []
    high_bit_unresolved = []
    for name, data, crc_ok, first, j, second, k in hits:
        x = untemper(int.from_bytes(bytes.fromhex(data), "little"))
        group_root = relations.find(first)
        ancestor_index = relations.offset[first] + j - 396
        mask, known = states[group_root][ancestor_index]
        assert (mask & LOW31) == LOW31
        assert ((known ^ x) & mask) == 0, (name, ancestor_index)
        entry = (name, first, j, second, k, ancestor_index, f"{x:08X}")
        if mask == ALL:
            previously_complete.append(entry)
        else:
            assert mask == LOW31
            high_bit_unresolved.append(entry)

    # All five independently reconstruction-complete ancestors match both
    # high and low bits of their original cross-source carrier.
    assert len(previously_complete) == 5
    assert len(high_bit_unresolved) == 4
    expected = {
        ("TRP[26] node=50 event=8 latch=0 seq=70", "BBC259FD"),
        ("TRP[12] node=49 event=82 latch=1 seq=201", "289D44B5"),
        ("TRP[45] node=49 event=82 latch=3 seq=993", "96DF5138"),
        ("RC17 RevB PURGE", "EDDF3ED2"),
    }
    assert {(entry[0], entry[-1]) for entry in high_bit_unresolved} == expected

    print("selected_row129_withheld", True)
    print("existing_completed_hidden_words", baseline_hidden)
    print("source_carrier_highbits_independently_checked", len(previously_complete))
    for entry in previously_complete:
        print("independently_complete_fullword_match", *entry)
    for entry in high_bit_unresolved:
        print("model_conditional_new_fullword", *entry)
    print("model_conditional_hidden_fullwords_total",
          baseline_hidden + len(high_bit_unresolved))
    print("caveat", "four promoted high bits require cross-source common-stream interpretation")
    print("K04_K08", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_control_fullword_bridge.py original-case.zip")
    analyze(Path(sys.argv[1]))
