"""K04: exact MT19937 draw-consumption inequality from original spool witnesses.

Usage: python h17-k04-mt-consumption-inequality.py original.zip
       python h17-k04-mt-consumption-inequality.py resources
Standard library only. Read-only, no acceptance commitment required.
"""
import argparse
import hashlib
import math
import re
import struct
import zipfile
from pathlib import Path

SOURCE = "evidence/print/spool-reconstruction.log"
SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
WITNESSES = (
    ((32, 0), (84, 2), (115, 0)),
    ((38, 0), (91, 3), (121, 3)),
    ((45, 0), (98, 3), (132, 3)),
)


def unright(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & 0xFFFFFFFF


def unleft(y, shift, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & 0xFFFFFFFF


def untemper(y):
    y = unright(y, 18)
    y = unleft(y, 15, 0xEFC60000)
    y = unleft(y, 7, 0x9D2C5680)
    return unright(y, 11)


def twist(a, b):
    value = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return (value >> 1) ^ (0x9908B0DF if value & 1 else 0)


def read_words(path):
    if path.is_file():
        with zipfile.ZipFile(path) as archive:
            raw = archive.read(SOURCE)
    else:
        raw = (path / SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA256, "Original spool SHA-256 mismatch"
    payloads = re.findall(rb"^2026-[^\n]* PAYLOAD=([A-F0-9]{32}) ", raw, re.MULTILINE)
    assert len(payloads) == 133, "Expected 128 regular records plus 5 tail records"
    return [tuple(untemper(w) for w in struct.unpack("<4I", bytes.fromhex(p.decode("ascii"))))
            for p in payloads]


def main(source):
    words = read_words(source)
    intervals = []
    for first, middle, last in WITNESSES:
        r, j = first
        m, k = middle
        f, n = last
        predicted = words[m][k] ^ twist(words[r][j], words[r][j + 1])
        assert predicted == words[f][n], f"Recurrence fails: {first} {middle} {last}"
        distance_middle = 397 + j - k
        distance_final = 624 + j - n
        late_distance = distance_final - distance_middle
        intervals.append(late_distance)
        print(f"WITNESS {first}->{middle}->{last}: "
              f"s[{m}]-s[{r}]={distance_middle}, "
              f"s[{f}]-s[{r}]={distance_final}, "
              f"s[{f}]-s[{m}]={late_distance}")
    assert intervals == [229, 227, 227]
    # U=d84..90, V=d91..97, W=d98..114,
    # X=d115..120, Y=d121..126, Z=d127..131.
    # The three equalities require U=X+2, V=Y+Z.
    # If every regular gap d0..126 >=7 and every gap >=4:
    u_min = 7 * 7
    x_min = u_min - 2
    w_min = 17 * 7
    y_min = 6 * 7
    z_min = 5 * 4
    c_min = w_min + x_min + y_min + z_min
    assert c_min == 228 and intervals[2] == 227
    print("TEST fixed 3+ hidden MT draws per regular row: CONTRADICTION")
    print(f"lower bound for s[132]-s[98]={c_min}; original witness={intervals[2]}")
    print("CONCLUSION at least one regular transition in "
          "84..90 or 98..126 consumes <=6 MT words (payload 4 + <=2 hidden).")
    # Random.choice(length=3) calls draw geometric(p=3/4) counts.
    skip_count = 624 - 4 * 83
    geometric_calls = 2 * 83
    tail = sum(math.comb(n - 1, geometric_calls - 1)
               * (0.75 ** geometric_calls) * (0.25 ** (n - geometric_calls))
               for n in range(skip_count, 800))
    print(f"TEST exactly two choice(3) calls per row: "
          f"83-row skip count={skip_count}, iid-model upper-tail P={tail:.12g}")
    print("Neither model determines K04 coupon bytes; acceptance unchanged.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    main(parser.parse_args().source)
