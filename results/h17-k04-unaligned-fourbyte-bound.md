# K04 unaligned contiguous four-byte replacement: completed bounded test

**Agent 21, 18 October 2026. Result: NO_MATCH.** This completes the nine unaligned byte offsets explicitly left pending in [the earlier aligned-word report](h17-k04-wordscan-bound.md). It is an exploratory printer-fragment corruption test, not a newly authenticated source, and it does not recover K04.

## Preserved source and exact tested class

The source is the unchanged export 06 ESC-N RECOVER last ACK for incident-date job `PS-261003-0417`, attempt 2 at 18:02 UTC. The 16-byte payload `A9A9DC5731A5E2AE879C47215C2559D5` XORs with the unchanged route mask `8556C8CB6140A7F9A5123AC7571BEE1C` to give `2CFF149C50E54557228E7DE60B3EB7C9`. This source-selected value fails the original K04 SHA-256 acceptance target `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

The new hypothetical corruption class replaces **four consecutive bytes at any one of offsets 1,2,3,5,6,7,9,10,11** of the 16-byte source-selected component with *every* possible unsigned 32-bit value, preserving the other twelve bytes. Since the route mask is fixed and XOR is bytewise bijective, the equivalent class of replacing four contiguous source PAYLOAD bytes is covered. Source material, routing and commitments were read-only throughout.

## Reproducibility and results

The scanner uses the SHA-256 one-block compression method in the existing [`k04-wordscan-fast.c`](k04-wordscan-fast.c). The implementation accepts any byte offset from 0 through 12, even though the previous report only exercised the four aligned offsets. A local independent implementation retained the same known component and original target, with a self-test mode that recomputed SHA-256 of the unmodified 16-byte component and substituted **only that synthetic test target in memory**. All **13** positions 0..12 correctly found their known four-byte original value in a one-trial positive control. A separate [read-only differential C control](test_k04_wordscan_hash_equivalence.c), using a fixed xorshift32 stream (seed `0x8e2acc51`), compared the one-block `SHA256_Transform` state with ordinary `SHA256()` over **1,000 varying replacement values at each of the 13 byte offsets (13,000 full 256-bit digest comparisons)**. Every comparison passed using the original selected component as base. These program checks validate hash implementation equivalence without authenticating any historical payload. For the original target, a 2^25-trial benchmark at position 1 was NO_MATCH.

Each unaligned offset then covered `START=0` and `COUNT=4294967296` in full, on four local CPU workers. Every process completed with its final NO_MATCH line. No partial run has been presented as a complete bound.

| Byte offset | Assignments | Original K04 match | Scanner seconds |
| ---: | ---: | :---: | ---: |
| 1 | 4,294,967,296 | 0 | 209.897 |
| 2 | 4,294,967,296 | 0 | 210.046 |
| 3 | 4,294,967,296 | 0 | 209.851 |
| 5 | 4,294,967,296 | 0 | 210.251 |
| 6 | 4,294,967,296 | 0 | 206.086 |
| 7 | 4,294,967,296 | 0 | 206.162 |
| 9 | 4,294,967,296 | 0 | 206.298 |
| 10 | 4,294,967,296 | 0 | 206.345 |
| 11 | 4,294,967,296 | 0 | 202.924 |
| **Total nine offsets** | **38,654,705,664** | **0** | |

A local run summary recorded all 9 exit codes and the 38,654,705,664 tested **assignments**. Overlap exists between different windows when fewer than four bytes change; this is an assignment count, not a count of distinct 16-byte strings. Local source SHA-256: `f3694a26b026706d5f616aa03e5c847d3ad784c3fc103639f09d633660ef3395`; JSON summary SHA-256: `e632d1ce8b91a37f53cace7279cc21c826d0d8a3df43d32e7abccf97528cc492`. The existing shared C scanner suffices to reproduce the search by supplying each listed position and its complete 32-bit range.

Together with the **four previously completed aligned offsets** [0,4,8,12](h17-k04-wordscan-bound.md), there are now NO_MATCH results for **every one of 13 possible contiguous four-byte replacement windows**, representing 55,834,574,848 tested assignments across the two reports. No original-case evidence says the printer lost exactly four consecutive bytes, so this is a bounded negative diagnostic with limited provenance weight.

## Disposition

The original last ACK's integrity warning remains. No accepted K04 component, original media witness, or correction mechanism was found. Retain `K04: null`, and retain `K08: null` because the final keeper caption remains unquoted. The original combined verifier is still incomplete with six accepted components. Do not promote this computational exclusion as evidence of a specific historical error mechanism or as progress toward authentic coupon recovery.
