"""Read-only bit-boundary slip diagnostic for H-17 escrow spool payload.

Usage: python check_h17_bit_slips.py path/to/extracted-case 20
No candidate is promoted without matching the original K04 commitment.
"""
import hashlib
import json
import sys
from pathlib import Path

WIDTH = 128
ALL = (1 << WIDTH) - 1


def sha_candidate(payload_int, mask_int):
    return hashlib.sha256((payload_int ^ mask_int).to_bytes(16, 'big')).hexdigest()


def candidates(payload_int, start, end):
    for k in range(start, end + 1):
        left = (payload_int << k) & ALL
        right = payload_int >> k
        high = WIDTH - k
        for edge in range(1 << k):
            yield 'left', k, edge, left | edge
            yield 'right', k, edge, right | (edge << high)


def selected_ack(case):
    labels = (case / 'evidence/archive-labels.ini').read_text()
    in_current_section = False
    job_id = None
    for raw in labels.splitlines():
        line = raw.strip()
        if line.startswith('['):
            in_current_section = line == '[printer_routes_2026-09-01_to_2026-10-03]'
        elif in_current_section and line.startswith('ESC-N='):
            job_id = line.split('=', 1)[1]
            break
    if job_id is None:
        raise ValueError('ESC-N current printer route not found')

    ack = []
    for line in (case / 'evidence/print/spool-reconstruction.log').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        fields = dict(part.split('=', 1) for part in line.split()[1:])
        if fields['JOB'] == job_id and fields['STATE'] == 'ACK' and fields['CLASS'] == 'RECOVER':
            ack.append((int(fields['ATTEMPT']), fields['PAYLOAD']))
    if not ack:
        raise ValueError('No ACK RECOVER payload for ESC-N')
    return job_id, max(ack)[1]


def main():
    case = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    max_bits = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    min_bits = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    if not 1 <= min_bits <= max_bits <= 23:
        raise ValueError('max_bits must be 1..23 for bounded runtime')
    job, raw_hex = selected_ack(case)
    payload = int(raw_hex, 16)
    mask = int(json.loads((case / 'evidence/recovery-routing.json').read_text())['K04']['masked_component'], 16)
    expected = json.loads((case / 'acceptance.json').read_text())['slot_sha256']['K04']

    # Positive control exercises the same generator and SHA-256 comparison.
    witness = ((payload << 3) & ALL) | 5
    witness_hash = sha_candidate(witness, mask)
    assert ('left', 3, 5, witness) in [entry for entry in candidates(payload, 3, 3) if sha_candidate(entry[3], mask) == witness_hash]

    print(f'K04 job={job} last-ACK payload={raw_hex}')
    print(f'original last-ACK match={sha_candidate(payload, mask) == expected}')
    checked = 0
    for direction, k, edge, test_payload in candidates(payload, min_bits, max_bits):
        checked += 1
        if sha_candidate(test_payload, mask) == expected:
            print(f'FOUND direction={direction} bits={k} edge={edge:X} payload={test_payload:032X}')
            return
    print(f'NO_MATCH bit-shift boundary assignments={checked}; shifts={min_bits}..{max_bits} both directions')
    print('This rules out only the stated bit-boundary model, and cannot authenticate the damaged spool record.')


if __name__ == '__main__':
    main()
