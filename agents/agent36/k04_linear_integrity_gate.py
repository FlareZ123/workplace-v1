"""K04 source-pinned gate for fixed linear printer integrity codes.

Explores a possible error-correction mechanism; never reads a hash commitment.
Run from repository root or pass the extracted original ZIP directory as argv[1].
"""
from hashlib import sha256
from pathlib import Path
import re
import sys

EXPECTED = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def rank_gf2(values):
    basis = {}
    for x in values:
        while x:
            bit = x.bit_length() - 1
            if bit not in basis:
                basis[bit] = x
                break
            x ^= basis[bit]
    return len(basis)


def rank_gf256(rows, polynomial):
    def mul(a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            a <<= 1
            if a & 256:
                a ^= polynomial
            b >>= 1
        return result

    def power(a, exponent):
        result = 1
        while exponent:
            if exponent & 1:
                result = mul(result, a)
            a = mul(a, a)
            exponent >>= 1
        return result

    matrix = [list(row) for row in rows]
    position = 0
    for col in range(len(matrix[0])):
        pivot = next((i for i in range(position, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[position], matrix[pivot] = matrix[pivot], matrix[position]
        inv = power(matrix[position][col], 254)
        matrix[position] = [mul(v, inv) for v in matrix[position]]
        for i in range(position + 1, len(matrix)):
            factor = matrix[i][col]
            if factor:
                matrix[i] = [v ^ mul(factor, p) for v, p in zip(matrix[i], matrix[position])]
        position += 1
        if position == len(matrix):
            break
    return position


def main(root):
    spool = (root / "evidence/print/spool-reconstruction.log").read_bytes()
    assert sha256(spool).hexdigest() == EXPECTED
    lines = [line for line in spool.splitlines() if b"PAYLOAD=" in line]
    payloads = [bytes.fromhex(re.search(rb"PAYLOAD=([0-9A-F]{32})", line).group(1).decode("ascii")) for line in lines]
    assert len(payloads) == 133
    assert all(b"+00:00" in line for line in lines[:128])
    assert all(line.split()[0].endswith(b"Z") for line in lines[128:])

    regular = [int.from_bytes(p, "big") for p in payloads[:128]]
    all_values = [int.from_bytes(p, "big") for p in payloads]
    ranks = (rank_gf2(regular), rank_gf2(all_values),
             rank_gf2([v | (1 << 128) for v in regular]),
             rank_gf2([v | (1 << 128) for v in all_values]))
    assert ranks == (128, 128, 128, 129)
    print("GF(2) regular/all ranks, affine augmented:", ranks)

    regular_recover = [payload for payload, line in zip(payloads[:128], lines[:128])
                       if b"CLASS=RECOVER" in line]
    assert len(regular_recover) == 35
    for poly in (0x11B, 0x11D):
        ranks = (rank_gf256(regular_recover, poly),
                 rank_gf256([p + bytes([1]) for p in regular_recover], poly))
        assert ranks == (16, 17)
        print(f"GF(256) RECOVER class, polynomial {poly:#05x}, linear/affine ranks:", ranks)

    # Synthetic positive controls for nontrivial parity codes.
    synthetic = [int.from_bytes(sha256(str(i).encode()).digest()[:16], "big")
                 for i in range(133)]
    parity_even = [x ^ (x.bit_count() & 1) for x in synthetic]
    parity_odd = [x ^ ((x.bit_count() + 1) & 1) for x in synthetic]
    assert rank_gf2(parity_even) <= 127
    assert rank_gf2([x | (1 << 128) for x in parity_odd]) <= 128
    print("synthetic even-parity / odd-affine-parity controls: PASS")
    print("No shared fixed affine GF(2) parity check across all 133 payloads.")
    print("No shared fixed affine GF(256) byte check across the 35 regular RECOVER payloads.")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources"))
