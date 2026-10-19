# K04 direct UTC-second seed-to-source attempt: bounded original-output non-match

**Agent 40, 19 October 2026.** This is a **conditional direct K04 cracking attempt**, not a recovered component or authenticated producer identification. No original source, routing, acceptance inventory, or verifier was altered.

## Proposed producer and original anchor

The surviving original `evidence/archive-labels.ini` lists commissioning on **24 September 2026**. The original printer buffer `evidence/print/spool-reconstruction.log` contains complete regular payloads dated **3 October 2026** and is SHA256 pinned as:

`7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.

Assume **conditionally** that the ordinary printer payload stream was produced by CPython's `random.Random(integer)`, seeded with a **UTC Unix timestamp in seconds** from 24 September through 5 October, and that ordinary row3's four little-endian tempered MT19937 output words appear consecutively in the first 4,096 draws. This is a restricted, falsifiable *seed recipe*, not an attested historical implementation. The acquisition/producer chronology is explicitly uncertain (see `results/h17-k04-control-time-order-discriminator.md`).

Before any K04 target evaluation, use original regular zero-based row3, 3 Oct 07:15 UTC, with complete original `PAYLOAD=24FF4383374867B2F2FABB2B30F72AAF`; interpreted as four consecutive 32-bit little-endian words:

`8343FF24 B2674837 2BBBFAF2 AF2AF730`.

A candidate matching all four 32-bit values would be strong producer evidence and would have to predict a withheld other intact row, such as row34, **before** attempting selected row129 or the K04 commitment. A miss ends this **specific** seed recipe and window without parameter expansion.

## Original result

The newly retained [independent C++17 CPython MT scanner](../agents/agent40/k04_utc_seed_direct.cpp) implements `init_by_array` with a one-word uint32 integer key (correct for the scanned UTC seconds), 624-word MT19937 twist, and CPython tempering. It performs rolling four-word comparison, allowing matches that straddle a 624-word state regeneration. All four original source words must match in order.

- UTC seed range: **1,790,208,000 (inclusive) through 1,791,244,800 (exclusive)**, which is 24 Sep 2026 00:00 UTC through 6 Oct 2026 00:00 UTC.
- **1,036,800 distinct integer seeds**; **4,096 starting offsets** `0..4095` per seed; **4,246,732,800 complete four-word source-position assignments**.
- **1 single-first-word coincidence**; **zero complete four-word original source matches**.
- Three independent CPython Python 3 integer seeds supply 12 verbatim `getrandbits(32)` calibration outputs in the C++ source. A separate synthetic generator, seeded with 1,791,000,000 and sampled at offset1,473, recovers its full 128-bit planted source block at the exact offset; the same four-word pattern is confirmed independently with real CPython.
- Local GCC build at `-O3 -std=c++17` completed the original range in **10.856 CPU seconds**. Tool output: `first_word_matches=1 all_four_matches=0`.

This is source-output directed rather than another attempt to reverse the K04 SHA256 or replay six existing components. The entire disputed printer row129, original K04 mask, K08 nonce and all REC8 commitments were excluded from the search.

## Limitations and next rule

This result **eliminates only the tested UTC-second integer CPython seed family with a 4,096-draw source prefix**. It says nothing about historic seeding by milliseconds, local time strings, numeric dates, alternate generator implementations, unseen longer prefixes, cached producer data, separate producer epochs, or correctness of the contested selected ACK. None of these alternatives is justified for a new large scan by the present record.

Agent41 previously tested a narrower **tail epoch** (16:00–18:03Z, 2,001 offsets, four orientation hypotheses), using a different RECOVER-tail intact output. The present **regular early-spool / commissioning-to-incident interval** is separately scoped, although both belong to the general timestamp-seed investigation.

No original K04 target bits, source-indexed donor words or exact K08 final-caption words were obtained. **Stop this timestamp family unless new original material actually specifies a producer/seed/cache rule.** The higher-value unresolved route remains authentic observations in both row43→44 and row96→97 target-ancestor windows, or an original ESC-N attempt-2 media/mask witness. This technical exclusion is deliberately kept below the main recovery index.
