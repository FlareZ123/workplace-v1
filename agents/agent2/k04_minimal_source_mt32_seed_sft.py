"""Minimal source-pair first-cycle std::mt19937 init_genrand(uint32) exclusion.

Requires original 43-member H17 case ZIP. No p955 vector, target coupon,
route mask, acceptance checksum, or external input is consulted.
"""
import hashlib
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

MASK = 0xFFFFFFFF
MAG = 0x9908B0DF
A = 1812433253
SPOOL = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def undo_right(y, bits):
    x = y
    for _ in range(6):
        x = y ^ (x >> bits)
    return x & MASK


def undo_left(y, bits, bitmask):
    x = y
    for _ in range(6):
        x = y ^ ((x << bits) & bitmask)
    return x & MASK


def untemper(y):
    return undo_right(undo_left(undo_left(undo_right(y, 18), 15, 0xEFC60000),
                                7, 0x9D2C5680), 11)


def twist(highbit, next_low31):
    x = (highbit & 0x80000000) | (next_low31 & 0x7FFFFFFF)
    return ((x >> 1) ^ (MAG if x & 1 else 0)) & MASK


def untwist_halves(value):
    lowbit = value >> 31
    mixed = (((value ^ (MAG if lowbit else 0)) << 1) | lowbit) & MASK
    assert twist(mixed, mixed) == value
    return mixed & 0x80000000, mixed & 0x7FFFFFFF


def recover_two_initialized_words(earlier, later):
    """If their four-word MT payload starts differ by 228, undo first twist."""
    # First pair earlier[1] -> later[0] is 227 outputs apart.
    z1 = earlier[1] ^ later[0]
    z2 = earlier[2] ^ later[1]
    z3 = earlier[3] ^ later[2]
    hi2, lo1 = untwist_halves(z1)
    hi3, lo2 = untwist_halves(z2)
    hi4, _ = untwist_halves(z3)
    return lo1 | hi3, lo2 | hi4


def source_rows(path):
    with ZipFile(path) as z:
        raw = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SPOOL
    lines = [line for line in raw.decode().splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    rows = []
    for row, line in enumerate(lines):
        match = re.search(r"PAYLOAD=([0-9A-F]{32})", line)
        assert match
        if row == 129:
            rows.append(None)
            continue
        rows.append(tuple(map(untemper, struct.unpack("<4I", bytes.fromhex(match.group(1))))))
    return rows


def reference_first_cycle(seed):
    initialized = [seed]
    for i in range(1, 624):
        x = initialized[-1]
        initialized.append((A * (x ^ (x >> 30)) + i) & MASK)
    state = initialized.copy()
    for i in range(624):
        combined = (state[i] & 0x80000000) | (state[(i + 1) % 624] & 0x7FFFFFFF)
        state[i] = (state[(i + 397) % 624] ^ (combined >> 1) ^
                    (MAG if combined & 1 else 0)) & MASK
    return initialized, state


def main(path):
    rows = source_rows(path)
    # Two independent source-only MT recurrence witnesses, no guessed
    # global layout. A: s86-s3=622, B: s86-s34=394 => s34-s3=228.
    a = rows[86][2] ^ rows[56][3]
    b = rows[116][3] ^ rows[86][2]
    assert a == twist(rows[3][0], rows[3][1])
    assert b == twist(0, rows[34][0])
    print("source_recurrence_A=s86_minus_s3_622 PASS")
    print("source_recurrence_B=s86_minus_s34_394 PASS")
    print("two_original_witnesses_imply_s34_minus_s3=228")

    # Synthetic, true first-cycle reference MT with rows 228 apart:
    seed = 0xA1234567
    initial, post = reference_first_cycle(seed)
    for phase in (0, 17, 96, 340):
        expected = initial[phase + 229:phase + 231]
        actual = recover_two_initialized_words(post[phase:phase+4],
                                               post[phase+228:phase+232])
        assert tuple(expected) == actual
        residue = (actual[1] - A * (actual[0] ^ (actual[0] >> 30))) & MASK
        assert residue == phase + 230
    print("synthetic_real_first_cycle=PASS seeds=1 source_offsets=4")

    # Historical producer assumption: same first standard-MT output cycle,
    # unknown phase s3 in 0..(624-232). The necessary initializer recurrence
    # residue at position s3+230 must lie in 230..622.
    first, second = recover_two_initialized_words(rows[3], rows[34])
    residue = (second - A * (first ^ (first >> 30))) & MASK
    possible = [phase for phase in range(393)
                if residue == phase + 230]
    print("original_pre_twist_init_state_1", f"{first:08X}")
    print("original_pre_twist_init_state_2", f"{second:08X}")
    print("original_initializer_implied_index", residue)
    print("possible_true_first_cycle_phase", possible)
    assert residue == 2011796279 and not possible
    print("source_only_conditional_32bit_reference_MT_first_cycle=EXCLUDED")
    print("K04_recovered_bits=0; K08_exact_words=0")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
