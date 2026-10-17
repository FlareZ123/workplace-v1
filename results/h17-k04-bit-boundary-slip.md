# H-17 K04: bounded sub-byte spool alignment test (Agent 9)

**Date:** 17 October 2026. **Result:** the unchanged K04 slot commitment matches none of **33,554,428** candidate components in the explicitly defined bit-boundary slip model. K04 remains unresolved.

## Evidence and method

Original `resources/evidence/archive-labels.ini` resolves incident-date ESC-N to job `PS-261003-0417`. The last `ACK` `CLASS=RECOVER` attempt (number 2, at 18:02 UTC in `resources/evidence/print/spool-reconstruction.log`) has a recovered 16-byte payload `A9A9DC5731A5E2AE879C47215C2559D5`. The route sheet mask is `8556C8CB6140A7F9A5123AC7571BEE1C`. XOR yields the known baseline `2CFF149C50E54557228E7DE60B3EB7C9`, whose SHA-256 fails the untouched K04 acceptance value `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

Hypothesis: the 128-bit recovered payload was misaligned by a whole number of **bits** during fragment recovery. For each bit shift `k = 1..23`, enumerate every possible `k`-bit unknown edge and test both candidate payloads:

- Left: `((payload << k) & (2**128-1)) | edge`.
- Right: `(payload >> k) | (edge << (128-k))`.

For each candidate, XOR with the unmodified route-sheet mask, hash the resulting 16 bytes with SHA-256 and compare the exact original slot commitment. This tests candidate assignments, not whether any particular shift actually happened. The maximum 23 bits was chosen to cover every partial-bit displacement smaller than three full bytes; earlier independent work already covered whole-byte boundary slips of one to three bytes. Bit-shifts at 8 and 16 bits overlap those earlier classes.

## Reproducibility

Read-only Python standard-library script: [`check_h17_bit_slips.py`](check_h17_bit_slips.py). It reselects the incident-date ESC-N job from the preserved routing label and the last acknowledged RECOVER attempt from the spool. It reads `resources/evidence/recovery-routing.json` for the mask and `resources/acceptance.json` for the acceptance target. Positive control uses an independently derived known left-three-bit witness and verifies that the enumeration finds it.

From the repository root, run the script against `resources` in four bounded runs: arguments `resources 20 1`, `resources 21 21`, `resources 22 22`, and `resources 23 23`. Source script SHA-256 in the local tested copy: `35d89a4cda7e3e840bc5ac47fa7d085ef6441ce30cdde4fcf5d3bdcf56821fab`. This separates the final large range into feasible segments without altering the tested class.

| Tested bit shifts | Candidate assignments | Original K04 commitment |
| --- | ---: | --- |
| 1–20, both directions | 4,194,300 | NO_MATCH |
| 21, both directions | 4,194,304 | NO_MATCH |
| 22, both directions | 8,388,608 | NO_MATCH |
| 23, both directions | 16,777,216 | NO_MATCH |
| **1–23 total** | **33,554,428** | **NO_MATCH** |

## Interpretation and limitations

This specifically excludes a shifted 128-bit payload with an otherwise intact 128−k-bit contiguous fragment and arbitrary replacement edge bits, for the tested 1–23-bit displacements. It does not address insertion/deletion in the middle, noncontiguous corruption, different missing original bytes, or incorrectly selected/unauthenticated sources. The custodian explicitly states the spool ACK does **not** authenticate recovered payload integrity. No evidence establishes that a bit-slip occurred, so this is a bounded diagnostic rather than a reconstructed K04 value.

The archive recovery remains **six accepted components of eight**. The original K04 coupon/media with independent integrity evidence, and the exact authenticated keeper caption for K08, remain missing from the preserved export. Do not modify source evidence, commitments, or verifier and do not promote the spool baseline.
