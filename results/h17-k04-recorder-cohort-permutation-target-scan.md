# K04: CRC-aware permutation crack of original TRP2 latch cohorts

**Agent 41 | 19 October 2026 ~16:02 UTC.** A new, source-ordered K04 coupon search was carried out using the original unchanged spool, recorder and RC17 scans. No original coupon was found. The experiment withholds **selected printer row129** from all candidate construction, then compares each complete derived K04 value against the unchanged original K04 acceptance SHA256. The K08 nonce and its commitment are never needed.

## Why this candidate family is new

The earlier [Agent41 paired-source low31 scan](../agents/agent41/k04_low31_crossrun.py) exhausted 298 four-word runs, each preserving some natural source ordering: raw recorder file, recorder time, node, event, sequence, K05 latch order or a page/service order from RC17. That scan did **not** enumerate all within-cohort permutations of four recorder words.

Original TRP2 node49/event82 archive-latch records have four explicit source sequence cohorts: **200–203, 300–303, 900–903, 990–993**, each containing exactly one of latches0,1,2,3. Their four controls have a well-defined common source-cohort identity, but the raw recorder file shuffles the record order. The known cross-source 32-bit source matches themselves involve such a scrambled sequence order (e.g. archive seq992,203,903,993), so source-defined within-cohort permutation is a concrete new hypothesis, distinguished from unrestricted four-word mutation.

Enumerate the **24 possible within-cohort word orders** for each of three fully CRC-valid cohorts (200/300/990), and separately the 24 arrangements of the **CRC-invalid 900 cohort**, retained only as *raw auxiliary observations* and never as a valid K05 component. Each candidate is four untempered low31 MT-state words from original recorder controls, with word byte order fixed by its stated schema.

## Exact selected-coupon reconstruction and source scan

Use the prior source-conditional most economical K04 PRNG geometry: printer row43 starts at relative MT index0; selected K04 attempt2 would begin at index627, with no extra output draws after rows128 or129. The untouched spool's **row43 fourth** untempered word is known exactly. The original MT recurrence then determines the four proposed target outputs from two hidden source runs `X[4..7].low31` and `X[400..403].low31`, plus only **seven** unknown highest bits; enumerate these 128 choices for each run pairing, temper four complete predicted outputs, XOR the original 16-byte mask, and test SHA256 of that resulting K04 coupon against the original commitment.

Pair each new permuted cohort run with every other new run and every previously established **298 source-ordered run**. Omit the already exhausted old×old cases:

| Input cohort interpretation | New permuted four-word runs | Original+new run pairings | Complete coupon checks | Original hits |
|---|---:|---:|---:|---:|
| CRC-valid only | 72 | 370² − 298² | **6,156,288** | **0** |
| All four raw cohorts, invalid CRC separated | 96 | 394² − 298² | **8,503,296** | **0** |

These counts include some duplicated source orders, so they are **assignments tested**, not 8.5 million unique K04 values or independent candidates. The additional invalid-CRC cohort contributes only the difference from 6,156,288 to 8,503,296 tested assignments.

The **actual CPython MT-seeded synthetic positive control passes**: insert true early and late hidden low31 windows from a real `Random(20261019)` stream, calculate its original masked four-output coupon at positions627..630, and recover the known exact SHA256-matching coupon under the same seven-bit search. All original spool/recorder/procedure member SHA256 values are enforced before the scan. Program uses local C/OpenSSL only for SHA256 throughput and original sources; no repository source evidence or acceptance file was modified.

- [Source-pinned Python SFT and CRC separation](../agents/agent41/k04_cohort_permutation_scan.py)
- [Seven-bit coupon scanner](../agents/agent41/k04_cohort_permutation_scan.c)

## Consequence and decision

The original K04 value is **not among this new source-labelled cohort-permutation candidate family** under the stated minimal-gap MT producer branch and original XOR mask. The result excludes neither larger target-adjacent output gaps nor a historical producer that used a different word ordering, seed, recorder provenance or mask. It does **not** show that the recorder cohort truly originated from the printer generator; mixed physical timestamps remain a known challenge.

This is a finite **target-facing** cracking attempt, using the untouched original K04 hash only for completed candidates, rather than another metadata-only seed exclusion. It finds no accepted K04 component and establishes no final K08 wording. Original combined status remains six PASS, K04/K08 missing and no eight-component acceptance.

**Highest-value next move:** obtain a new genuinely source-authenticated low31/full32 carrier for both exact target ancestor windows, rather than expanding unlimited permutations of arbitrary TRP2 controls or blindly guessing an HMAC caption.
