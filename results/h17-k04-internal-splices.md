# H-17 K04: one-unit internal fragment splice audit (Agent 9)

**Date:** 17 October 2026. **Result:** 114,688 one-unit deletion/insertion assignments, corresponding to 83,945 distinct 16-byte recovered payload candidates across all tested classes, failed unchanged K04 acceptance. This diagnostic does not recover K04.

## Source and model

The primary source is the incident-date ESC-N `PS-261003-0417` last-ACK RECOVER attempt 2, payload `A9A9DC5731A5E2AE879C47215C2559D5` in `resources/evidence/print/spool-reconstruction.log`. The mask in the original `resources/evidence/recovery-routing.json` is `8556C8CB6140A7F9A5123AC7571BEE1C`. Direct XOR baseline `2CFF149C50E54557228E7DE60B3EB7C9` fails the original `resources/acceptance.json` K04 SHA-256 commitment. The custodian notes that retained printer fragments and ACK dispatch status do not certify payload integrity.

A possible fragment reassembly error could **lose one encoded unit and duplicate or insert a unit elsewhere within the payload**, preserving overall length. For granularity `g` equal to 1 bit, 4 bits (hexadecimal nibble), or 8 bits (byte):

1. Divide the recorded 128-bit payload into `128/g` contiguous units in original most-significant-first order.
2. Remove one unit at every possible position.
3. Insert every possible `g`-bit value at every possible position in the resulting shorter sequence, returning to 128 bits.
4. XOR each resulting candidate with the unchanged mask, SHA-256 hash the 16 raw resulting bytes, and compare to the unchanged K04 slot commitment.

Both insertion positions and deletion positions range across the entire reconstructed payload. The class includes a single-unit substitution as a special case; duplicates between assignments and granularities are deduplicated for the actual acceptance comparisons. This is a test of a hypothesized internal fragment splice, not a claim that any such error was observed.

## Deterministic reproduction

Read-only Python standard-library source: [`check_h17_internal_splices.py`](check_h17_internal_splices.py). It imports the source-selection and SHA routine of [`check_h17_bit_slips.py`](check_h17_bit_slips.py). From the repository root, run `python results/check_h17_internal_splices.py resources`. It derives the source job and ACK from preserved files rather than accepting an invented input. An independently constructed byte-level positive witness deletes the third observed byte, inserts hex `7B` at index five, and verifies the enumerated candidate bytes and masked SHA-256 digest.

Local tested script SHA-256: `815361de7f3afdcd3cd6c8a750ea95748f385106a88b4feade21239b030aff50`. The committed Git blob was separately compared with the local script and matched by SHA-1 object ID `ef664a82aceeb548cb79bca93cf17c9d228e81eb`.

| Granularity | Assignments | New distinct candidates beyond earlier rows | K04 result |
| --- | ---: | ---: | --- |
| 1 bit (128 units) | 32,768 | 9,417 | NO_MATCH |
| 4 bits (32 nibbles) | 16,384 | 14,509 | NO_MATCH |
| 8 bits (16 bytes) | 65,536 | 60,019 | NO_MATCH |
| **Total** | **114,688** | **83,945** | **NO_MATCH** |

The reported distinct values are computed over the union of all three granularities in that row order, so they can safely be summed. The number of assignment trials follows `N² × 2^g` for `N=128/g`.

## Limits and disposition

This excludes one deletion plus one inserted/replacement unit anywhere in the buffer at exactly the tested bit/nibble/byte granularity. It does not exclude multiple corruptions, larger missing blocks, byte permutations, alternate unrecovered printer media, errors to another source field, or an unattested original coupon.

Prior reports already exclude substantial other K04 classes (low-weight flips, contiguous burst repairs, word substitutions, byte mosaics, boundary slips). These are finite negative tests and do not restore the original bitstream. Leave K04 null until independently sourced bytes pass the original commitment. The same export lacks authenticated exact final keeper wording for K08, so combined REC8 recovery remains incomplete.
