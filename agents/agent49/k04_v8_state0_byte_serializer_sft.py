"""Agent49 source-only V8 byte producer pilot; two frozen mappings, no target parsing."""
from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

ZIP = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('c-energy-group-documents2026.zip')
SPOOL = 'evidence/print/spool-reconstruction.log'
SPOOL_SHA = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
MASK64 = (1 << 64) - 1


def step(s0: int, s1: int) -> tuple[int, int, int]:
    a, b = s0, s1
    s0 = b
    a ^= (a << 23) & MASK64
    a ^= a >> 17
    a ^= b
    a ^= b >> 26
    s1 = a & MASK64
    return s0, s1, (s0 >> 56) & 255


def samples(state: int, cache: bool) -> bytes:
    s0, s1 = state & MASK64, state >> 64
    values = []
    for _ in range(64):
        s0, s1, byte = step(s0, s1)
        values.append(byte)
    if cache:
        values.reverse()
    return bytes(values)


def observed_pair(data: bytes) -> tuple[bytes, bytes]:
    rows = {}
    for raw in data.decode('ascii').splitlines():
        if not raw.startswith(('2026-10-03T18:01:00Z ', '2026-10-03T18:03:00Z ')):
            continue
        fields = dict(token.split('=', 1) for token in raw.split()[1:])
        assert fields['JOB'] == 'PS-261003-0417' and fields['CLASS'] == 'RECOVER'
        assert fields['STATE'] == 'REQUESTED' and fields['DEST'] == 'bench'
        rows[raw[:20]] = bytes.fromhex(fields['PAYLOAD'])
    assert set(rows) == {'2026-10-03T18:01:00Z', '2026-10-03T18:03:00Z'}
    return rows['2026-10-03T18:01:00Z'], rows['2026-10-03T18:03:00Z']


def source_bits(first: bytes, second: bytes) -> int:
    output = first + second
    return sum(((v >> bit) & 1) << (8*i + bit) for i,v in enumerate(output) for bit in range(8))


def equations(cache: bool, first: bytes, second: bytes) -> tuple[list[int], list[int]]:
    columns = []
    for j in range(128):
        out = samples(1 << j, cache)
        columns.append(source_bits(out[:16], out[32:48]))
    rhs = source_bits(first, second)
    coefficients = []
    for row in range(256):
        co = sum(((col >> row) & 1) << j for j, col in enumerate(columns))
        coefficients.append(co)
    return coefficients, [(rhs >> row) & 1 for row in range(256)]


def solve(coefficients: list[int], rhs: list[int]) -> tuple[int, int, bool]:
    """Solve binary equations, returning rank, one state, and consistency."""
    pivot: dict[int, tuple[int, int]] = {}
    for co, value in zip(coefficients, rhs):
        while co:
            pos = co.bit_length() - 1
            if pos not in pivot:
                pivot[pos] = (co, value)
                break
            pc, pv = pivot[pos]
            co ^= pc
            value ^= pv
        else:
            if value:
                return len(pivot), 0, False
    solution = 0
    for pos in sorted(pivot):
        co, value = pivot[pos]
        parity = ((co & solution).bit_count()) & 1
        if value ^ parity:
            solution |= 1 << pos
    return len(pivot), solution, True


def main() -> None:
    with zipfile.ZipFile(ZIP) as z:
        original = z.read(SPOOL)
    digest = hashlib.sha256(original).hexdigest()
    assert digest == SPOOL_SHA, f'Original spool changed: {digest}'
    first, second = observed_pair(original)
    print('Original SHA256:', digest)
    print('Excluded from parser: selected 18:02 ACK2 and all acceptance/mask inputs')
    print('Intact controls:', first.hex().upper(), second.hex().upper())
    for cache in (False, True):
        name = 'reverse-64-cache' if cache else 'contiguous-64-bit'
        original_state = int.from_bytes(hashlib.sha256(name.encode()).digest()[:16], 'big')
        planted = samples(original_state, cache)
        co, rhs = equations(cache, planted[:16], planted[32:48])
        pr, ps, ok = solve(co, rhs)
        assert ok and samples(ps, cache)[:16] == planted[:16]
        assert samples(ps, cache)[32:48] == planted[32:48]
        print(name, 'synthetic-positive=PASS', f'rank={pr}')
        co, rhs = equations(cache, first, second)
        rank, solution, consistent = solve(co, rhs)
        if consistent:
            result = samples(solution, cache)
            matched_first = result[:16] == first
            matched_second = result[32:48] == second
        else:
            matched_first = matched_second = False
        print(name, 'original-state-consistent=', consistent, f'rank_to_failure={rank}',
              'original-pair-matched=', matched_first and matched_second)
        assert not consistent or matched_first and matched_second


if __name__ == '__main__':
    main()
