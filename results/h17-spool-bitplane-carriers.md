# H-17 K04: 128-row regular spool one-bit carrier test

**Agent 16, 18 October 2026.** Outcome: **NO_MATCH** in a finite, explicitly hypothetical bitplane/parity encoding class. Neither original K04 nor K08 is recovered.

## Source observation and why this test was considered

The supplied `resources/evidence/print/spool-reconstruction.log` contains exactly **128** regularly formatted, `+00:00`-timestamped jobs `PS-261003-0300` through `PS-261003-0427` in index order, each carrying a complete 16-byte hexadecimal `PAYLOAD`. A separate five-line tail uses `Z` timestamps, including incident-date RECOVER entries, and is excluded from this test. A hypothetical exactly-one-bit-per-regular-row side carrier would produce a 128-bit value, the same width as the 16-byte missing coupon. That width coincidence motivated this bounded test; **no source instruction claims that the regular spool encodes a coupon this way**.

The original fixed K04 mask `8556C8CB6140A7F9A5123AC7571BEE1C` and the original untouched `resources/acceptance.json` K04 SHA-256 commitment are read directly from case files. The script pins the original spool SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`, asserts the expected row count and job identifiers, and performs no source writes.

## Exact coverage and positive control

For every regularly ordered 16-byte `PAYLOAD`, form one extracted bit under these four classes:

| Per-row extraction class | Options | Packing options | Assignments |
| --- | ---: | ---: | ---: |
| Pick a fixed payload byte and bit position | 16 × 8 | 4 | 512 |
| Parity of a fixed payload byte | 16 | 4 | 64 |
| XOR parity at one fixed bit position over 16 payload bytes | 8 | 4 | 32 |
| Parity of all 128 payload bits | 1 | 4 | 4 |
| **Total** | **153** | **4** | **612** |

The four packing choices are forward/reversed row order times most-/least-significant-bit-first packing within each output byte. Each constructed 16-byte value is interpreted as a hypothetical raw coupon and XORed with the original fixed mask, then the SHA-256 of that candidate component is compared to the original K04 slot commitment.

Before the original test, a synthetic control derives a target commitment from a deliberately known enumerated candidate and confirms it is found by the same enumeration.

## Observed result

The original 133-row spool split was confirmed as 128 regular and five tail records. All **612** assignments were evaluated. The synthetic test passed; **zero** original K04 commitment matches were found. Reproduce using [check_h17_spool_bitplanes.py](check_h17_spool_bitplanes.py) against the untouched extracted case or the shared `resources/` directory, with standard-library Python 3.

This result rules out *only* the declared direct bitplane and parity families. It does not authenticate the selected RECOVER/ACK payload, infer an error mechanism, rule out a more complex encoding, or supply the missing K08 caption. In particular, the source's 128 regular rows are not designated recovery-media bits, so this is a diagnostic, not evidence that a coupon side channel existed.

The existing route-selected K04 attempt-2 reduction remains NO_MATCH and the original verifier remains **6 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false**. Keep both unresolved slots null. For broader source-cohort context see [the spool cohort/identity audit](h17-spool-cohort-identity-audit.md), and for the human-readable case status see [results overview](README.md).
