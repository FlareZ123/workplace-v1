# TRP2 four-record CRC syndrome: a bounded K04 auxiliary-carrier integrity discriminator

**Agent 12 | 19 October 2026 ~19:22 UTC.** Source: original `evidence/recorder/trip-recorder.raw` SHA256 `5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba`, format note's CRC32 over 20 bytes and four-byte stored CRC. The original file and K01–K08 commitments were not modified or used as an oracle. [Read-only self-contained reproducer](../agents/agent12/k04_trp2_crc_syndrome.py).

## Original-record hypothesis and precomputed discriminant

The recorder format says CRC failures occur in a damaged tail. The 900-series archive-latch cohort at node49/event82 is wholly CRC-invalid; notably original recorder row72/seq903 independently provides one of Agent2's **already known** exact MT predecessor fingerprints for intact printer rows10/41. A plausible narrowly falsifiable hypothesis was that the CRC failures reflect systematic corruption of **the stored check bytes**, leaving original control fields viable as auxiliary MT witnesses. Under a *single- or two-bit corruption model* the precise bit position can be determined independently from the stored CRC and the retained twenty-byte record body. A surviving control-body-bit repair would create a new four-byte candidate donor before any K04 hash test. No broad donor pool or alternate original printer payload was hypothesized.

For each original 24-byte record, compute `zlib.crc32(record[:20]) XOR uint32le(record[20:24])`. Enumerate **all 192 single-bit flips** and **all 18,336 two-bit flips** and check which transformed records satisfy CRC. This exhausts the explicitly bounded 1–2-bit fault model per record. Synthetic positive control corrupts one CRC-valid original control byte, then recovers the correct data-bit position.

## Result

| 0-based TRP2 row | Original sequence | Recorded control bytes | CRC syndrome | Unique 1-bit repair | Number of 2-bit repairs |
|---:|---:|---|---|---|---:|
| 14 | 900 | C2DE39CC | 00000100 | byte21, bit0 (stored CRC) | 0 |
| 41 | 901 | BA194782 | 00000100 | byte21, bit0 (stored CRC) | 0 |
| 72 | 903 | F2595C84 | 00000100 | byte21, bit0 (stored CRC) | 0 |
| 77 | 902 | 2A4EE66D | 00000100 | byte21, bit0 (stored CRC) | 0 |

All **84 other records** already pass CRC. Thus the *only* original 1- or 2-bit repair for every invalid record is to flip **bit8 of the recorded CRC**, without changing the 20-byte record body. No corrected control-body alternative exists within this exact error radius. Independent tested positive: a synthetic one-bit control-byte flip is correctly localized to its control byte.

A separate finite slip test searched control-word windows at offsets9..15 **within only these four invalid records** against 139,128 intact-printer inverse-MT successor fingerprints (selected ESC-N ACK withheld). It found **zero shifted-control matches**. Seven exact-field matches over all original recorder entries were recovered as positive controls; these correspond to **previously published** TRP2/printer links, not new observations. This local search is a narrow shift hypothesis, not an exhaustive misalignment or data-recovery result.

## Cracking consequence and limits

The uniform `0x00000100` error is a striking source-specific checksum-only pattern; under a 1–2-bit recording-error premise, the associated 900-series control bytes do **not** need data-bit correction. This justifies preserving seq903's known cross-source MT match as an **auxiliary observation** rather than silently discarding its raw bytes when exploring cached-producer lineage.

It **does not** make any of these four records CRC-valid *in the original archive*: K05 must continue to exclude all four. A deliberately generated bad checksum or a more complex body-plus-checksum alteration remains possible; the syndrome does not authenticate historical control-byte integrity absolutely. Agent41 already tested **the same raw 900-series controls**, including their 24 permutations, as K04 conditional donors at p=627 with zero acceptance, so this checksum finding is **not** a new K04 candidate pool and must not trigger a replay of that scan. The selected original coupon, its two missing indexed ancestor windows, and exact K08 keeper words remain unknown. **Original accepted status unchanged: six PASS, K04/K08 MISSING, combined INCOMPLETE.**

**Stop criterion:** 1- or 2-bit data-corruption/byte-slip corrections in the invalid recorder cohort supply no new donor, so close this branch without broadening to source-free bit or permutation search. Reopen only if new independent original checksum provenance, source-index ordering, or an observed ancestor relation appears.
