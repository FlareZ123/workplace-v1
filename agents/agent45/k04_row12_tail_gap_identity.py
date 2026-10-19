"""K04 source-only four-witness bridge: row12 metadata draw count to row129 tail.
Run: python agents/agent45/k04_row12_tail_gap_identity.py
Optional original ZIP: python agents/agent45/k04_row12_tail_gap_identity.py /path/c-energy-group-documents2026.zip
No selected row129 payload, verifier, mask, or acceptance material is examined.
"""
from hashlib import sha256
from pathlib import Path
import random
import re
import sys
import zipfile

SOURCE = "evidence/print/spool-reconstruction.log"
EXPECTED_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MASK = 0xFFFFFFFF


def read_source():
    if len(sys.argv) > 1:
        with zipfile.ZipFile(sys.argv[1]) as archive:
            return archive.read(SOURCE)
    return (Path(__file__).resolve().parents[2] / "resources" / SOURCE).read_bytes()


def untemper(value):
    value ^= value >> 18
    value ^= (value << 15) & 0xEFC60000
    fixed = value
    for _ in range(5):
        value = fixed ^ ((value << 7) & 0x9D2C5680)
    fixed = value
    for _ in range(3):
        value = fixed ^ (value >> 11)
    return value & MASK


def twist(previous, successor):
    mixed = (previous & 0x80000000) | (successor & 0x7FFFFFFF)
    return (mixed >> 1) ^ (0x9908B0DF if mixed & 1 else 0)


def witness(words, a, b, c, expected_high):
    """a=(row,-1) is the unobserved word immediately before a row."""
    ar, ai = a
    br, bi = b
    cr, ci = c
    assert ai == -1
    left = twist(expected_high << 31, words[ar][0])
    right = words[br][bi] ^ words[cr][ci]
    assert left == right, (a, b, c, hex(left), hex(right))
    assert twist((1 - expected_high) << 31, words[ar][0]) != right
    return left


def main():
    for seed in (0, 42, (1 << 250) + 123):
        generator = random.Random(seed)
        observed = [untemper(generator.getrandbits(32)) for _ in range(900)]
        assert all(
            twist(observed[i], observed[i + 1]) == observed[i + 397] ^ observed[i + 624]
            for i in range(276)
        )
    source = read_source()
    assert sha256(source).hexdigest() == EXPECTED_SHA256
    spool = [
        re.search(rb"PAYLOAD=([0-9A-F]{32})", line).group(1)
        for line in source.splitlines()
        if b"PAYLOAD=" in line
    ]
    assert len(spool) == 133
    # Row129 (the disputed coupon) is specifically not transformed or consulted.
    words = {}
    for row in (12, 13, 43, 44, 66, 67, 96, 97, 128, 130):
        raw = bytes.fromhex(spool[row].decode("ascii"))
        words[row] = [untemper(int.from_bytes(raw[4*i:4*i+4], "little")) for i in range(4)]

    matches = [
        ((12, -1), (66, 0), (96, 1), 0),
        ((13, -1), (67, 1), (97, 2), 1),
        ((43, -1), (96, 3), (128, 0), 1),
        ((44, -1), (97, 2), (130, 3), 0),
    ]
    for a, b, c, bit in matches:
        actual = witness(words, a, b, c, bit)
        print(f"PASS {a} -> {b} -> {c}, missing predecessor MSB={bit}, twist={actual:08X}")

    # If s[r] denotes a row's first four-word MT stream index:
    # W12: s96 - s12 = 622; W43: s96 - s43 = 393.
    # W13: s97 - s13 = 621; W44: s97 - s44 = 394.
    assert (622 - 393) == 229  # s43 - s12
    assert (621 - 394) == 227  # s44 - s13
    # Therefore d43=d12-2, where d_r=s[r+1]-s[r]=4+g_r.
    assert (227 - 229) == -2
    # W43: s128=s43+623; W44: s130=s44+620.
    assert (620 - 623) == -3
    # s130-s128 = d43-3 = d12-5.
    # Two four-output rows (128 and selected 129) require >=8 draws:
    #   (4+g128)+(4+g129) = d12-5 = (4+g12)-5
    # Consequently g128+g129=g12-9, and g12>=9.
    for hypothetical_g12 in range(9, 15):
        feasible_splits = [
            (g128, hypothetical_g12 - 9 - g128)
            for g128 in range(hypothetical_g12 - 8)
        ]
        assert all(sum(split) == hypothetical_g12 - 9 for split in feasible_splits)
        print(f"g12={hypothetical_g12}: g128+g129={hypothetical_g12 - 9}; "
              f"tail splits={feasible_splits}")
    print("CONCLUSION source-conditional g12 >= 9 and g128+g129 = g12-9")


if __name__ == "__main__":
    main()
