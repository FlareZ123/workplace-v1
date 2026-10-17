"""Read-only H-17 ESC-N single-unit internal deletion/insertion diagnostic.

Run from a repository checkout: python results/check_h17_internal_splices.py resources
"""
import hashlib
import json
import sys
from pathlib import Path

from check_h17_bit_slips import selected_ack, sha_candidate


def variants(source, unit_bits):
    units = 128 // unit_bits
    unit_mask = (1 << unit_bits) - 1
    pieces = [(source >> (unit_bits * (units - position - 1))) & unit_mask for position in range(units)]
    for removed_at in range(units):
        remaining = pieces[:removed_at] + pieces[removed_at + 1:]
        for inserted_at in range(units):
            prefix = remaining[:inserted_at]
            suffix = remaining[inserted_at:]
            for unit_value in range(1 << unit_bits):
                candidate = 0
                for part in prefix:
                    candidate = (candidate << unit_bits) | part
                candidate = (candidate << unit_bits) | unit_value
                for part in suffix:
                    candidate = (candidate << unit_bits) | part
                yield removed_at, inserted_at, unit_value, candidate


def main():
    case = Path(sys.argv[1] if len(sys.argv) > 1 else 'resources')
    job, raw_hex = selected_ack(case)
    payload = int(raw_hex, 16)
    routing = json.loads((case / 'evidence/recovery-routing.json').read_text())
    acceptance = json.loads((case / 'acceptance.json').read_text())
    mask = int(routing['K04']['masked_component'], 16)
    expected = acceptance['slot_sha256']['K04']
    print(f'job={job}; ACK payload={raw_hex}; baseline match={sha_candidate(payload, mask) == expected}')

    # Independent byte-level witness: remove index 2, insert 0x7B at index 5.
    original_bytes = bytes.fromhex(raw_hex)
    shortened = original_bytes[:2] + original_bytes[3:]
    witness_bytes = shortened[:5] + b'\x7b' + shortened[5:]
    mask_bytes = mask.to_bytes(16, 'big')
    witness_hash = hashlib.sha256(bytes(a ^ b for a, b in zip(witness_bytes, mask_bytes))).hexdigest()
    seen = set()
    for bits in (1, 4, 8):
        assignment_count = 0
        new_values = 0
        positive_witness_seen = False
        for removed, inserted, value, candidate in variants(payload, bits):
            assignment_count += 1
            if bits == 8 and (removed, inserted, value) == (2, 5, 0x7B):
                positive_witness_seen = True
                assert candidate.to_bytes(16, 'big') == witness_bytes
                assert sha_candidate(candidate, mask) == witness_hash
            if candidate in seen:
                continue
            new_values += 1
            seen.add(candidate)
            if sha_candidate(candidate, mask) == expected:
                print(f'FOUND bits={bits} remove={removed} insert={inserted} value={value} payload={candidate:032X}')
                return
        assert positive_witness_seen if bits == 8 else True
        print(f'bits={bits} assignments={assignment_count} new_unique={new_values} NO_MATCH')
    print(f'NO_MATCH total_assignments=114688 union_unique_candidates={len(seen)}')
    print('Only one deleted and one inserted bit, nibble or byte was modeled; K04 is not recovered.')


if __name__ == '__main__':
    main()
