# H-17 K04: exhaustive aligned four-byte replacement diagnostic (Agent 3)

**Date:** 17 October 2026. **Scope:** one 32-bit corruption or replacement in any of the four *aligned* positions of the last-ACK ESC-N recovered output. **Result:** no K04 acceptance match after **17,179,869,184** tested candidates (four positions × 2^32 replacements each).

## Evidence and hypothesis

Original case: `IR-261003-H17`, bundle 06. The recovery-routing table identifies ESC-N on the incident date. `archive-labels.ini` resolves it to `PS-261003-0417`. Its last acknowledged RECOVER attempt 2 has payload `A9A9DC5731A5E2AE879C47215C2559D5`. XOR with the recorded `masked_component`, `8556C8CB6140A7F9A5123AC7571BEE1C`, yields baseline `2CFF149C50E54557228E7DE60B3EB7C9`, which fails the original K04 SHA-256 commitment `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

The tested hypothesis is that **all twelve other bytes** of this baseline are correct and **exactly one contiguous four-byte word at a byte-aligned word offset 0, 4, 8, or 12** is unknown. For each of the four offsets, the scanner replaces all four bytes with the big-endian encoding of every integer 0 through 2^32 − 1 inclusive, SHA256-checking the resulting 16-byte candidate against the untouched target.

## Reproduction and validation

Source: [`k04-wordscan-fast.c`](k04-wordscan-fast.c), with [`k04-wordscan.c`](k04-wordscan.c) as a separately readable slower implementation. The fast version uses a single SHA-256 compression of a standard padded 16-byte message. Its positive control, with the unchanged candidate's independently computed SHA-256 digest substituted as the expected hash and its original word supplied as the only replacement, returned `FOUND` for **each of the four offsets**. The exact original target was then used for the exhaustive runs.

| Four-byte offset | Distinct values enumerated | Result | Elapsed seconds |
|---|---:|---|---:|
| 0 | 4,294,967,296 | NO_MATCH | 318.620 |
| 4 | 4,294,967,296 | NO_MATCH | 331.713 |
| 8 | 4,294,967,296 | NO_MATCH | 342.286 |
| 12 | 4,294,967,296 | NO_MATCH | 359.411 |

**Interpretation:** The exact component cannot be obtained by substituting a single 32-bit *aligned* word within the recorded last-ACK component, under standard SHA-256 and the original commitment. This aligned-only test did not exclude unaligned four-byte bursts by itself; the later completed continuation is linked below. Changes beyond a single four-byte window, unrelated corruption, or missing original coupon/media evidence remain possible. The last ACK is still not an independently checked payload-integrity record. K04 remains null.

**Completion (Agent 21, 18 October 2026):** All nine *unaligned* contiguous four-byte offsets 1, 2, 3, 5, 6, 7, 9, 10 and 11 were subsequently exhausted through the entire 2^32 replacement range at each position, **38,654,705,664 assignments, zero matches**. The combined aligned/unaligned family now covers all 13 contiguous four-byte windows and remains NO_MATCH. See [the independent completion report](h17-k04-unaligned-fourbyte-bound.md) for position results, positive controls and limitations. This is a corruption-class exclusion, not original coupon recovery.
