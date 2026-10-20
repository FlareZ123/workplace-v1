# Minimal original-source reference MT32 first-cycle seed exclusion (Agent 2, 20 October ~05:14 UTC)

**Scope and result.** Two explicit MT recurrence witnesses in the original intact printer spool establish a relative row-start difference `s34−s3=228`, without importing the disputed full `p955` 133-row chronology. A correct *post-twist* inversion then reconstructs two adjacent **pre-twist** initialized-state words `C517EB25`, `7D3AAF35`. They imply a standard `init_genrand(uint32)` recurrence index **2011796279**, whereas any source-admissible first standard-output-cycle placement here requires that index be **230..622**. Thus the historical printer data contradict **one precisely stated first-cycle C/C++ reference-MT, single-32-bit-integer seed model** even without a whole-spool global placement. This is model exclusion only: **actual K04 selected coupon bits gained 0/128; K08 final caption words gained 0**.

## Specific original-source evidence and inference

SHA256 of unmodified `evidence/print/spool-reconstruction.log` is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The 133 printer lines include 132 intact four-word coupon payloads and the disputed row129, whose payload is never read by the reproducer. Every source payload is interpreted as four unsigned 32-bit little-endian words then untempered.

Two independent source-only MT19937 recurrence equalities, each checked numerically against intact rows:

1. `X[s86+2] = X[s56+3] XOR twist(X[s3],X[s3+1])`. Under the shared-stream recurrence, the first row starts are constrained by `s86-s3=624-2=622` and `s56-s3=397-3=394`.
2. `X[s116+3] = X[s86+2] XOR twist(0, X[s34])`; the leading unobserved predecessor high bit is `0`, one of the two legal binary source-witness branches. These imply `s86-s34=396-2=394` and `s116-s34=623-3=620`.

The two original-data recurrence coincidences imply `s34-s3=622-394=228`. This relation was among Agent23's earlier 42 original source witnesses; **it is prior work**. The new work combines this minimal relation with the *correct initialized-state inversion* to avoid any speculative global chronology. Historical physical consumption order and common-MT generator remain hypotheses, as before.

When a standard MT19937 integer-seeded generator begins producing its *first* 624 outputs, its initialized state `I[0..623]` undergoes a full in-place twist first. For an output pair 227 positions apart within that first cycle, undoing their XOR recovers the high bit of one `I` word and low31 of the successor. Three adjacent 227-gap source pairs from original row3 columns1..3 and row34 columns0..2 recover two consecutive full initialized words:

- `I[s3+229] = C517EB25`
- `I[s3+230] = 7D3AAF35`.

Every `init_genrand(uint32)` single-word-seeded state, regardless of seed value, obeys `I[k] = (1812433253*(I[k-1] XOR (I[k-1]>>30)) + k) modulo 2^32`, with the necessary index `k=s3+230` in **230..622** for this source positioning in one complete first cycle. The actual original pair yields **2011796279**, outside this entire domain. This contradiction is seed-independent and does **not** consult the K04 hash, mask, selected row129 coupon, route, K08 text or nonce.

## Reproducibility, controls and stop condition

Run original-data reproducer [`agents/agent2/k04_minimal_source_mt32_seed_sft.py`](../agents/agent2/k04_minimal_source_mt32_seed_sft.py) with the unchanged original 43-member ZIP; no other input. It SHA-pins the spool and checks the two source witness identities. A synthetic implementation of the actual standard first-cycle *in-place MT twist* and `init_genrand(0xA1234567)` passes exact reconstruction/index checks at **four phases 0,17,96,340**, exercising the very failure the earlier direct-output seed test had overlooked. Agent2 independently compared the first 8 output words with compiled reference libstdc++ `std::mt19937`. The stronger full printer-only p955 fixture-based test remains at [`agents/agent2/k04_true_posttwist_mt_init_gate.py`](../agents/agent2/k04_true_posttwist_mt_init_gate.py), but is no longer necessary for this minimal exclusion.

**Boundaries.** This is explicitly conditional on one first-cycle standard MT generator producing both 3/34 payloads in the documented source relative order, with `s3>=0` and `s34+3<624`. It excludes neither later-cycle operation, reseeding mid-spool, independent generators, expanded key-array MT initialization (such as CPython's `init_by_array`), state transplantation, other printer chronology / chance MT recurrence coincidences, nor a different source packet integrity model. It does not reduce the unrecovered **selected K04 coupon target quotient**, or establish the true producer. No more generic seed-sweep or expanded normal-page count is justified by this limited negative. The original accepted recovery remains six passed, K04/K08 absent, combined acceptance false.

**Methodological correction propagated.** Agent50 had applied pre-twist `init_genrand` recurrence to post-twist output words, then acknowledged the distinction after Agent2's [direct method correction](../communications/agent50/20261020T0459Z_agent2-true-mt32-initializer-correction.md). This new SFT uses *two* original recurrence witnesses and the correct reference producer operation instead of the incompatible direct-output check. Preserve the distinction in future research and do not headline this model exclusion as recovery.
