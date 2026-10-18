"""Bounded, read-only K04 printer bit/byte-orientation sensitivity test."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re


def bit_orient(byte, rotation, reverse_bits, complement):
    if reverse_bits:
        byte = int(f'{byte:08b}'[::-1], 2)
    if rotation:
        byte = ((byte << rotation) | (byte >> (8 - rotation))) & 255
    return byte ^ (255 if complement else 0)


def orient(payload, rotation, reverse_bits, complement, reverse_stream):
    value = bytes(bit_orient(b, rotation, reverse_bits, complement) for b in payload)
    return value[::-1] if reverse_stream else value


def variants(payload):
    for rotation in range(8):
        for reverse_bits in (False, True):
            for complement in (False, True):
                for reverse_stream in (False, True):
                    yield (rotation, reverse_bits, complement, reverse_stream), orient(
                        payload, rotation, reverse_bits, complement, reverse_stream
                    )


def run(root):
    spool_file = root / 'evidence/print/spool-reconstruction.log'
    spool = spool_file.read_bytes()
    routing = json.loads((root / 'evidence/recovery-routing.json').read_text())
    acceptance = json.loads((root / 'acceptance.json').read_text())
    mask = bytes.fromhex(routing['K04']['masked_component'])
    target = acceptance['slot_sha256']['K04']
    records = []
    for line in spool.decode('ascii').splitlines():
        payload_match = re.search(r'\bPAYLOAD=([A-F0-9]{32})\b', line)
        if payload_match:
            job = re.search(r'\bJOB=(\S+)', line).group(1)
            attempt = int(re.search(r'\bATTEMPT=(\d+)', line).group(1))
            state = re.search(r'\bSTATE=(\S+)', line).group(1)
            records.append((job, attempt, state, bytes.fromhex(payload_match.group(1))))

    def digest(payload):
        return sha256(bytes(a ^ b for a, b in zip(payload, mask))).hexdigest()

    selected = next(p for j, a, s, p in records
                    if j == 'PS-261003-0417' and a == 2 and s == 'ACK')
    assert selected.hex().upper() == 'A9A9DC5731A5E2AE879C47215C2559D5'
    assert orient(selected, 0, False, False, False) == selected
    control_target = digest(orient(selected, 3, True, True, True))
    assert any(digest(candidate) == control_target for _, candidate in variants(selected))
    assert len(records) == 133
    assert len(mask) == 16

    hits = []
    unique = set()
    attempts = 0
    for job, attempt, state, payload in records:
        for parameters, candidate in variants(payload):
            attempts += 1
            unique.add(candidate)
            if digest(candidate) == target:
                hits.append((job, attempt, state, parameters))

    print('source SHA-256:', sha256(spool).hexdigest())
    print('payloads:', len(records))
    print('transform assignments:', attempts, 'unique candidate bytes:', len(unique))
    print('selected unmodified component digest:', digest(selected))
    print('original commitment:', target)
    print('K04 hits:', hits)
    assert attempts == 8512 and len(unique) == 8512


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'resources')
    args = parser.parse_args()
    run(args.root)
