"""Calibrate H-17's exact-job RECOVER retries against a hypothetical iid-byte null.

Read-only, Python standard library, and never assumes the payloads truly are iid.
"""
from itertools import combinations
from math import comb, sqrt
from pathlib import Path
import re

SOURCE = Path(__file__).resolve().parents[1] / "resources/evidence/print/spool-reconstruction.log"


def main():
    rows = [line for line in SOURCE.read_text(encoding="utf-8").splitlines()
            if "JOB=PS-261003-0417" in line and "CLASS=RECOVER" in line]
    assert len(rows) == 3, "Expected the three documented RECOVER attempts"
    attempts = []
    for row in rows:
        attempt = int(re.search(r"ATTEMPT=(\d+)", row).group(1))
        payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", row).group(1))
        attempts.append((attempt, payload))
    attempts.sort()
    assert [a for a, _ in attempts] == [1, 2, 3]
    assert all(len(payload) == 16 for _, payload in attempts)

    print("H17 K04: hypothetical independent uniform byte baseline")
    for (a, first), (b, second) in combinations(attempts, 2):
        distance = sum((x ^ y).bit_count() for x, y in zip(first, second))
        byte_differences = sum(x != y for x, y in zip(first, second))
        deviation = abs(distance - 64)
        two_sided_tail = sum(comb(128, k) for k in range(129)
                             if abs(k - 64) >= deviation) / 2**128
        print(f"attempt {a} vs {b}: bits={distance}/128, differing bytes="
              f"{byte_differences}/16, z={(distance - 64) / sqrt(32):+.4f}, "
              f"binomial two-sided tail={two_sided_tail:.8f}")

    all_distinct = all(len({payload[i] for _, payload in attempts}) == 3
                       for i in range(16))
    probability = ((255 / 256) * (254 / 256)) ** 16
    print("All three bytes are distinct at every one of 16 positions:", all_distinct)
    print(f"Probability of this event for three independent uniform byte arrays: "
          f"{probability:.12f}")
    print("These null calculations do not authenticate any K04 payload.")


if __name__ == "__main__":
    main()
