"""Source-pinned, generator-agnostic cyclic CRC test for K04 spool recovery.

A fixed degree>=8 CRC polynomial divides the XOR of any two valid equal-
residue 128-bit codewords. Examine all four-row subsets and search for a
fifth independent row, allowing 30 of 35 original records to be corrupted.
No acceptance commitments or target hashes are read.
"""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import re
import sys

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
REVERSE_BYTE = bytes(int(f"{v:08b}"[::-1], 2) for v in range(256))


def polynomial_mod(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def polynomial_gcd(a, b):
    while b:
        a, b = b, polynomial_mod(a, b)
    return a


def payload_int(raw, orientation):
    if orientation == "big":
        return int.from_bytes(raw, "big")
    if orientation == "little":
        return int.from_bytes(raw, "little")
    if orientation == "reversed_bits":
        return int(f"{int.from_bytes(raw, 'big'):0128b}"[::-1], 2)
    if orientation == "reversed_byte_bits":
        return int.from_bytes(raw.translate(REVERSE_BYTE), "big")
    raise ValueError(orientation)


def inspect_cohort(payloads, orientation):
    values = [payload_int(p, orientation) for p in payloads]
    quartet_hits = []
    quintet_hits = []
    max_degree = -1
    for i, j, k, l in combinations(range(len(values)), 4):
        generator = polynomial_gcd(values[i] ^ values[j], values[i] ^ values[k])
        generator = polynomial_gcd(generator, values[i] ^ values[l])
        degree = generator.bit_length() - 1
        max_degree = max(max_degree, degree)
        if degree < 8:
            continue
        quartet_hits.append(((i, j, k, l), degree, generator))
        used = {i, j, k, l}
        for m in range(len(values)):
            if m in used:
                continue
            common = polynomial_gcd(generator, values[i] ^ values[m])
            if common.bit_length() - 1 >= 8:
                quintet_hits.append(((i, j, k, l, m), common))
    return {
        "orientation": orientation, "rows": len(values),
        "quartets_degree_at_least_8": len(quartet_hits),
        "quintets_degree_at_least_8": len(quintet_hits),
        "max_quartet_common_degree": max_degree,
        "quartets": quartet_hits, "quintets": quintet_hits[:3],
    }


def synthetic_controls():
    generator = 0x11021  # 16-bit CCITT polynomial
    offset = int.from_bytes(sha256(b"H17 synthetic affine offset").digest()[:16], "big")
    valid = []
    for i in range(5):
        message = int.from_bytes(sha256(f"good-{i}".encode()).digest()[:14], "big")
        codeword = message << 16
        codeword ^= polynomial_mod(codeword, generator)
        valid.append(codeword ^ offset)
    assert all(polynomial_mod(v ^ valid[0], generator) == 0 for v in valid)

    noise = []
    for i in range(30):
        value = int.from_bytes(sha256(f"independent-{i}".encode()).digest()[:16], "big")
        if polynomial_mod(value ^ valid[0], generator) == 0:
            value ^= 1
        noise.append(value)
    data = [x.to_bytes(16, "big") for x in valid + noise]
    check = inspect_cohort(data, "big")
    assert check["quintets_degree_at_least_8"] > 0
    assert any(set(ids) == set(range(5)) for ids, _ in check["quintets"])
    return "PASS: detects 5 unknown-codeword CRC16 examples amid 30 non-codewords"


def main(root):
    data = (root / "evidence/print/spool-reconstruction.log").read_bytes()
    assert sha256(data).hexdigest() == SOURCE_SHA256
    regular = []
    for line in data.splitlines():
        if b"PAYLOAD=" not in line or b"+00:00" not in line:
            continue
        fields = dict(re.findall(rb"(\w+)=([^\s]+)", line))
        if fields[b"CLASS"] == b"RECOVER":
            regular.append(bytes.fromhex(fields[b"PAYLOAD"].decode()))
    assert len(regular) == 35
    print(synthetic_controls())
    for orientation in ("big", "little", "reversed_bits", "reversed_byte_bits"):
        result = inspect_cohort(regular, orientation)
        print(orientation, {k: v for k, v in result.items() if k not in ("quartets", "quintets")})
        assert result["quintets_degree_at_least_8"] == 0
    print("NO_MATCH: no 5 regular RECOVER codewords admit a shared degree>=8 fixed CRC polynomial.")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources"))
