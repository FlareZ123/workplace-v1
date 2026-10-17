"""Read-only K04 printer retained-fragment ordering hypothesis.

Run: python results/check_h17_fragment_permutations.py resources [min_parts=2] [max_parts=5]
"""
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

from check_h17_bit_slips import selected_ack


def arrangements(payload, fragments):
    """Yield possible concatenations of contiguous cuts, permuted and optionally reversed."""
    for cuts in itertools.combinations(range(1, 16), fragments - 1):
        starts = (0, *cuts)
        ends = (*cuts, 16)
        parts = tuple(payload[a:b] for a, b in zip(starts, ends))
        for order in itertools.permutations(range(fragments)):
            selected = tuple(parts[idx] for idx in order)
            for flags in range(1 << fragments):
                yield b''.join(piece[::-1] if flags & (1 << pos) else piece
                               for pos, piece in enumerate(selected))


def main():
    case = Path(sys.argv[1] if len(sys.argv) > 1 else 'resources')
    min_parts = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    max_parts = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    if not 2 <= min_parts <= max_parts <= 5:
        raise ValueError('tested fragment count range must stay in 2..5')
    job, source_hex = selected_ack(case)
    payload = bytes.fromhex(source_hex)
    mask = int(json.loads((case / 'evidence/recovery-routing.json').read_text())['K04']['masked_component'], 16)
    target = bytes.fromhex(json.loads((case / 'acceptance.json').read_text())['slot_sha256']['K04'])
    print(f'job={job}; last ACK={source_hex}; original match={hashlib.sha256((int.from_bytes(payload, "big") ^ mask).to_bytes(16, "big")).digest() == target}')

    # Known 3-part order-and-orientation witness, independent of the sweep target.
    witness_parts = (payload[:5], payload[5:11], payload[11:])
    witness = witness_parts[2][::-1] + witness_parts[0] + witness_parts[1]
    witness_target = hashlib.sha256((int.from_bytes(witness, 'big') ^ mask).to_bytes(16, 'big')).digest()
    witness_found = False
    for candidate in arrangements(payload, 3):
        if hashlib.sha256((int.from_bytes(candidate, 'big') ^ mask).to_bytes(16, 'big')).digest() == witness_target:
            witness_found = True
            break
    assert witness_found

    total = 0
    for count in range(min_parts, max_parts + 1):
        checked = 0
        for variant in arrangements(payload, count):
            checked += 1
            if hashlib.sha256((int.from_bytes(variant, 'big') ^ mask).to_bytes(16, 'big')).digest() == target:
                print(f'FOUND with fragments={count}; raw_payload={variant.hex().upper()}')
                return
        expected = math.comb(15, count - 1) * math.factorial(count) * (1 << count)
        assert checked == expected
        total += checked
        print(f'fragment_count={count} assignments={checked} NO_MATCH', flush=True)
    print(f'NO_MATCH total_tested_assignments={total}; parts={min_parts}..{max_parts}')
    print('These are variable-size contiguous blocks with reordering and per-block byte reversal, not verified original media.')


if __name__ == '__main__':
    main()
