"""Read-only H-17 K04 first-cycle standard MT19937 seed gate.

Uses original source plus a conditional source-consistent p955 chronology.
The selected row129 and all REC8 acceptance values are withheld.
Unlike direct tests of four printed words against init_genrand, this
reconstructs PRE-TWIST initialization words from 227-gap output pairs.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile

SP = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
M = 0xFFFFFFFF
A = 1812433253
MAGIC = 0x9908B0DF


def untemper(y: int) -> int:
    x = y
    for shift, mask, left in ((18, M, False), (15, 0xEFC60000, True),
                              (7, 0x9D2C5680, True), (11, M, False)):
        v = x
        for _ in range(6):
            x = v ^ (((x << shift) & mask) if left else x >> shift)
        x &= M
    return x


def initialized_from_posttwist(post: dict[int, int]) -> dict[int, int]:
    def untwist_pair(z: int) -> tuple[int, int]:
        parity = z >> 31
        x = (((z ^ (MAGIC if parity else 0)) << 1) | parity) & M
        return x & 0x80000000, x & 0x7FFFFFFF

    result = {}
    for u in sorted(post):
        if u + 228 >= 624 or any(k not in post for k in
                                   (u + 1, u + 227, u + 228)):
            continue
        lo = untwist_pair(post[u] ^ post[u + 227])[1]
        hi = untwist_pair(post[u + 1] ^ post[u + 228])[0]
        result[u + 228] = lo | hi
    return result


def init_genrand(seed: int) -> list[int]:
    state = [seed]
    for k in range(1, 624):
        x = state[-1]
        state.append((A * (x ^ (x >> 30)) + k) & M)
    return state


def twist_initial(initial: list[int]) -> list[int]:
    state = initial.copy()
    for k in range(624):
        x = (state[k] & 0x80000000) | (state[(k + 1) % 624] & 0x7FFFFFFF)
        state[k] = (state[(k + 397) % 624] ^ (x >> 1)
                    ^ (MAGIC if x & 1 else 0)) & M
    return state


def original_printer(zippath: Path, fixturepath: Path) -> dict[int, int]:
    with ZipFile(zippath) as archive:
        spool = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(spool).hexdigest() == SP
    fixture = json.loads(fixturepath.read_text(encoding="utf-8"))
    assert fixture["source_spool_sha256"] == SP
    starts = fixture["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    lines = [s for s in spool.decode().splitlines() if s.startswith("2026-")]
    assert len(lines) == 133
    out = {}
    for row, line in enumerate(lines):
        if row == 129:
            continue
        match = re.search(r"PAYLOAD=([A-F0-9]{32})", line)
        assert match
        payload = bytes.fromhex(match.group(1))
        for j in range(4):
            out[starts[row] + j] = untemper(int.from_bytes(payload[j*4:j*4+4], "little"))
    assert len(out) == 528
    return out


def links_and_hits(post: dict[int, int]) -> tuple[dict[int, int], int, list[tuple[int, int, int]]]:
    state = initialized_from_posttwist(post)
    pairs = [(k, state[k], state[k + 1]) for k in sorted(state)
             if k + 1 in state]
    hits = []
    for k, left, right in pairs:
        implied = (right - A * (left ^ (left >> 30))) & M
        phase = implied - (k + 1)
        if 0 <= phase and k + phase + 1 < 624:
            hits.append((k, implied, phase))
    return state, len(pairs), hits


def main(zippath: Path, fixturepath: Path) -> None:
    # Real standard first-cycle outputs are AFTER the full in-place MT twist.
    # The reference C++ std::mt19937(0xA1234567) first eight outputs agree
    # with temper(twist_initial(init_genrand(0xA1234567))) bit for bit.
    original_seed_state = init_genrand(0xA1234567)
    first = twist_initial(original_seed_state)
    synthetic = {k: first[k + 17] for k in range(607)}
    restored, npos, hits = links_and_hits(synthetic)
    assert len(restored) > 100
    assert all(value == original_seed_state[k + 17]
               for k, value in restored.items())
    assert len(hits) == npos and all(h[2] == 17 for h in hits)
    print(f"synthetic_reference_seed=PASS phase=17 links={npos}")

    original = original_printer(zippath, fixturepath)
    restored, links, hits = links_and_hits(original)
    assert len(restored) == 57 and links == 25 and hits == []
    print(f"original_printer_words={len(original)} recovered_initializer_words={len(restored)}")
    print(f"independent_initializer_adjacencies={links} accepted_phases={hits}")
    print("conditional_model_excluded=standard_uint32_init_genrand_first_cycle_with_p955")
    print("actual_selected_K04_coupon_bits_recovered=0")
    print("K08_final_words_recovered=0")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
