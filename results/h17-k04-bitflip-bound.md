# H-17 K04: bounded bit-flip diagnostic (Agent 4)

**Date:** 17 October 2026. **Scope:** historical archive printer-buffer recovery only. **Result:** no K04 slot-commitment match after testing **all 275,584,033** components within Hamming distance 0 through 5 bits of the source-selected candidate.

## Evidence and hypothesis

The local custodian note warns that reconstructed spool bytes lack independent integrity confirmation. The routing rule and `archive-labels.ini` choose logical ESC-N, incident-date job `PS-261003-0417`. `mail/16.eml` selects its final acknowledged RECOVER attempt; the original spool log has ACK at attempt 2 and a later REQUESTED attempt 3 without ACK.

- Source ACK payload: `A9A9DC5731A5E2AE879C47215C2559D5`.
- Routing XOR mask: `8556C8CB6140A7F9A5123AC7571BEE1C`.
- Resulting 16-byte K04 candidate: `2CFF149C50E54557228E7DE60B3EB7C9`.
- SHA-256(candidate): `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`.
- Unchanged slot commitment: `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

The precise test hypothesis is **up to five individually flipped bits at arbitrary positions in that 128-bit reconstructed candidate**. This is narrower than arbitrary byte corruption or choosing a different source.

## Reproducible exhaustive test

For each `k = 0,1,2,3,4,5`, enumerate all `itertools.combinations(range(128), k)`. XOR `1 << (bit % 8)` at byte index `bit // 8` of the selected candidate, then SHA-256 the resulting 16 bytes and compare against the original K04 commitment. There are no random trials or probabilistic sampling.

| Flipped bits | Distinct candidates |
|---|---:|
| 0 | 1 |
| 1 | 128 |
| 2 | 8,128 |
| 3 | 341,376 |
| 4 | 10,668,000 |
| 5 | 264,566,400 |
| **Total** | **275,584,033** |

**No matching digest** in the tested domain. A native C/OpenSSL SHA-256 implementation completed all six classes. An independent Python standard-library implementation, [h17-k04-bitflip-check.py](h17-k04-bitflip-check.py), derives the initial candidate from the unmodified source files and is suitable for independent reproduction. Its independent Python run completed all six Hamming classes and matched the C result exactly (275,584,033 failed candidates). SHA-256 of the source spool file: `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.

The same-job RECOVER attempts are not near-duplicates: the unacknowledged attempt 1 payload differs from the acknowledged attempt 2 payload in **68 of 128 bits**, and unacknowledged attempt 3 differs from acknowledged attempt 2 in **62 bits**. Attempts 1 and 3 differ in **62 bits**. These are descriptive Hamming distances, not evidence of a recoverable majority or parity code. The routing rule still excludes both unacknowledged attempts; nothing supplied validates them as independent copies of the same coupon bytes.

## Interpretation and limits

Under the selected route, payload, XOR mask, and ordinary bit-flip model, any candidate satisfying the published K04 hash must have Hamming distance **at least 6** from the recorded result. The computation does not support an inference about which bytes might be missing, whether a different buffer is authentic, whether the route transcription is complete, or whether the original record suffered other corruption. Other corruption mechanisms, missing original evidence, and unrecovered exact source bytes remain open.

**Disposition:** K04 stays null in the shared candidate. K08 remains unsupported by an authenticated final caption. The combined key still cannot be verified. Prior K04 two-byte and three-contiguous-byte negative tests are separately documented in [h17-recovery.md](h17-recovery.md). This test is a bounded forensic diagnostic; it is not a mandate for unbounded preimage search.
