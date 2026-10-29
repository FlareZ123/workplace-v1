"""Original-H17 late-Z clock-ticked LCG blind heldout SFT.

Usage: python k04_late_minute_lcg_sft.py SOURCE.zip
Hypothesis: one modulo-2^128 affine state advance per elapsed UTC minute.
Never decodes selected row129, route mask, acceptance, or K08.
"""
from hashlib import sha256
import random
import re
import sys
from zipfile import ZipFile

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MASK = (1 << 128) - 1


def step(x: int, a: int, b: int) -> int:
    return (x * a + b) & MASK


def step_n(x: int, a: int, b: int, n: int) -> int:
    for _ in range(n):
        x = step(x, a, b)
    return x


def constraint(a: int, x2: int, x23: int, x24: int) -> int:
    power = 1
    series = 0
    for _ in range(21):
        series = (series + power) & MASK
        power = (power * a) & MASK
    b = (x24 - a * x23) & MASK
    return (power * x2 + b * series - x23) & MASK


def solve_a(x2: int, x23: int, x24: int) -> list[int] | None:
    roots = [r for r in (0, 1) if constraint(r, x2, x23, x24) & 1 == 0]
    for bit_index in range(1, 128):
        bit = 1 << bit_index
        wordmask = (bit << 1) - 1
        roots = [
            extended
            for r in roots
            for extended in (r, r | bit)
            if constraint(extended, x2, x23, x24) & wordmask == 0
        ]
        if len(roots) > 256:
            return None
        if not roots:
            return []
    return roots


def synthetic_control() -> None:
    rnd = random.Random(0x8E1732)
    a = rnd.getrandbits(128) | 1
    b = rnd.getrandbits(128) | 1
    x0 = rnd.getrandbits(128)
    x2 = step_n(x0, a, b, 2)
    x23 = step_n(x2, a, b, 21)
    x24 = step(x23, a, b)
    recovered = solve_a(x2, x23, x24)
    assert recovered is not None and a in recovered
    assert step_n(x0, a, b, 2) == x2
    print("synthetic 21-minute clock-ticked LCG: PASS")


def main(zipname: str) -> None:
    synthetic_control()
    with ZipFile(zipname) as archive:
        data = archive.read("evidence/print/spool-reconstruction.log")
    assert sha256(data).hexdigest() == SPOOL_SHA
    rows = [line for line in data.decode("utf-8").splitlines() if "PAYLOAD=" in line]
    assert len(rows) == 133
    # Rows 128,130,131,132 are the four intact late events. The selected
    # row129 is never decoded; our predictor sees only historical controls.
    for orientation in ("big", "little"):
        def value(row: int) -> int:
            assert row in (128, 130, 131, 132)
            match = re.search(r"PAYLOAD=([0-9A-F]{32})", rows[row])
            assert match
            return int.from_bytes(bytes.fromhex(match.group(1)), orientation)
        x2, x23, x24 = value(130), value(131), value(132)
        roots = solve_a(x2, x23, x24)
        assert roots is not None
        print(f"{orientation} full128 roots using r130/r131/r132:", len(roots))
        if roots:
            x0 = value(128)
            matches = [
                a for a in roots
                if step_n(x0, a, (x24 - a * x23) & MASK, 2) == x2
            ]
            print(f"{orientation} blind intact r128->r130 full128 matches:", len(matches))
            assert not matches
        if orientation == "big":
            assert len(roots) == 2
        else:
            assert len(roots) == 0
    print("selected K04 row129/route mask/acceptance never inspected: PASS")
    print("target K04 selected bits recovered: 0/128")


if __name__ == "__main__":
    main(sys.argv[1])
