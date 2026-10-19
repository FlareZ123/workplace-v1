"""Recover additional hidden K04-family MT states from four original printer rows.

Run: python agents/agent21/k04_two_step_fixedpoint_sft.py original-case.zip
Depends on sibling k04_double_twist_sft.py. No selected row129/acceptance data.
"""
import random
import sys
from k04_double_twist_sft import read, untemper, temper

ALL = 0xffffffff
HIGH = 0x80000000
LOW = 0x7fffffff
MAG = 0x9908b0df
SOURCE_STARTS = ((9, 0), (40, 229), (63, 398), (124, 852))
EXPECTED = {-394: 0x7168DD87, -393: 0x289D44B5, 4: 0x8DAE2276,
            625: 0x78204AD3, 626: 0xC472C638,
            627: 0xC34BEB5E, 628: 0x2EEBC38E}
PARTIAL = {-395: (HIGH, HIGH), -392: (LOW, 0x1FF49339),
           5: (LOW, 0x5E28452A), 228: (HIGH, 0)}


def twist(x, y):
    mix = (x & HIGH) | (y & LOW)
    return ((mix >> 1) ^ (MAG if mix & 1 else 0)) & ALL


def inverse_twist(v):
    bit = v >> 31
    return (((v ^ (MAG if bit else 0)) << 1) | bit) & ALL


def close(observed):
    state = {p: (ALL, v) for p, v in observed.items()}

    def add(p, mask, bits):
        old, val = state.get(p, (0, 0))
        assert not ((val ^ bits) & mask & old), (p, mask, bits)
        if old | mask == old:
            return False
        state[p] = (old | mask, val | bits)
        return True

    for iteration in range(100):
        changed = False
        for end, (mask, value) in list(state.items()):
            middle = end - 227
            if mask == ALL and state.get(middle, (0, 0))[0] == ALL:
                mixed = inverse_twist(value ^ state[middle][1])
                changed |= add(end - 624, HIGH, mixed & HIGH)
                changed |= add(end - 623, LOW, mixed & LOW)
        for first, (mask, value) in list(state.items()):
            if not mask & HIGH:
                continue
            nxt = state.get(first + 1, (0, 0))
            middle = state.get(first + 397, (0, 0))
            end = state.get(first + 624, (0, 0))
            if nxt[0] & LOW == LOW:
                delta = twist(value, nxt[1])
                if middle[0] == ALL:
                    changed |= add(first + 624, ALL, middle[1] ^ delta)
                if end[0] == ALL:
                    changed |= add(first + 397, ALL, end[1] ^ delta)
        if not changed:
            break
    assert iteration < 99
    return state


def main(path):
    rng = random.Random(80317)
    stream = [untemper(rng.getrandbits(32)) for _ in range(2500)]
    phase = 600
    witness = {phase + start + j: stream[phase + start + j]
               for _, start in SOURCE_STARTS for j in range(4)}
    control = close(witness)
    for p in EXPECTED:
        mask, value = control[phase + p]
        assert mask == ALL and value == stream[phase + p]
    for p in PARTIAL:
        mask, value = control[phase + p]
        assert (value & mask) == (stream[phase + p] & mask)
    print("synthetic source-state controls: 7 complete and 4 partial PASS")

    lines, rows = read(path)
    assert "DEST=store" in lines[9]
    observed = {start + j: value for row, start in SOURCE_STARTS
                for j, value in enumerate(rows[row])}
    assert len(observed) == 16
    state = close(observed)
    full = {p: v for p, (m, v) in state.items() if p not in observed and m == ALL}
    partial = {p: (m, v) for p, (m, v) in state.items()
               if p not in observed and m != ALL}
    assert full == EXPECTED, (full, EXPECTED)
    assert partial == PARTIAL, (partial, PARTIAL)
    assert temper(full[4]) >> 30 == 3
    assert temper(partial[5][1] | HIGH) >> 30 == 0
    assert temper(partial[5][1]) >> 30 == 2
    print("original source: 16 intact observed, seven inferred complete and four partial")
    print("inferred full", [(p, f"{v:08X}") for p, v in sorted(full.items())])
    print("inferred partial", [(p, f"{m:08X}", f"{v:08X}")
                               for p, (m, v) in sorted(partial.items())])
    print("two prehistory states -394,-393 require earlier generator epoch")
    print("K04 coupon bits recovered 0; K08 caption words recovered 0")


if __name__ == "__main__":
    main(sys.argv[1])
