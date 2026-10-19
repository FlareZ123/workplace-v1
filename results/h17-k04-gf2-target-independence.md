# K04: exact GF(2) target observability across both source-pinned gap groups

**Agent 49, 19 October 2026 ~07:43 UTC. A newly implemented linear-algebra attack, with a rigorous negative target-observability result. K04/K08 remain MISSING and no original REC8 acceptance PASS is claimed.**

## The discriminating question

The 42 intact-source MT19937 recurrence witnesses place regular printer row43 and RECOVER row128 in one fixed-relative-position group; regular row44, row97 and RECOVER rows130/131 occupy a second group. Row129, the selected disputed K04 ACK, lies between row128 and row130. The two groups each have intact source-pinned words, and inverse/forward propagation alone has failed to produce the K04 target.

A previously untried attack is to solve the **entire coupled recurrence as a linear system over GF(2)**. Such a solve can recover information that local inverse-twist peeling misses: multiple partial constraints may combine to determine a bit or a relation between target bits even if no local recurrence has enough known arguments. This report tests that stronger inference directly.

## Model and exact computation

Let untempered 32-bit output words be `X[t]`, with the ordinary MT19937 stream recurrence:

`X[t+624] = X[t+397] XOR twist(X[t], X[t+1])`

The first 624 words from group43-relative `t=-229` to `394` are **19,968 symbolic GF(2) bit variables**. Later words are represented as exact bit-vectors in those variables, including the highest-bit/low31 split and conditional XOR constant `9908B0DF` of the standard twist. Three independent synthetic CPython `random.Random` seeds pass all 676 recurrence checks each.

The 42 previously documented witnesses fix the relative rows:

- Group43: rows `12:-229, 43:0, 66:167, 96:393, 128:623`
- Group44: rows `13:-227, 44:0, 67:168, 97:394, 130:620, 131:624`

All **44 complete, retained four-word payloads** in those two groups provide 1,408 source-bit equations. The disputed row129 is excluded from every equation; no K04 acceptance commitment or XOR mask is read.

For each proposed group shift `d=s44-s43` from **11 to 65** inclusive, embed the second group at its local positions plus `d`. A source-only four-output minimum implies selected row129's potential first output positions:

`s129-s43 = p, p=627..d+616`

The 55 shifts and their respective **1 through 55** selected positions produce **1,540 candidate placements**. Compute a binary Gaussian-elimination basis for each source model, then reduce each of the four selected words' 128 bit-function vectors modulo that basis. Also compute the rank of all 128 reduced target vectors to detect *linear relations even where no individual target bit is fixed*.

## Verified result

| Measurement | Exact result |
| --- | ---: |
| Group-shift hypotheses | 55 (`d=11..65`) |
| Potential selected row129 starts examined | **1,540** |
| Intact printer source words | 44 |
| Source bit equations per shift | 1,408 |
| Rank of source equations, every shift | **1,123** |
| Dependent source equations per shift | 285 |
| Individually determined selected-output bits | **0 of 128**, for all 1,540 placements |
| Rank of selected 128 bits modulo the source equations | **128**, for all 1,540 placements |
| Additional affine constraints among target bits | **0**, for all 1,540 placements |

Independent positive controls show that the same elimination **does** reconstruct row44's two previously verified hidden predecessor words `27D820C7` and `0ACF4761` and its intact first payload word for every shift. Thus the zero-target result is not explained by a solver that fails to recover source-implied hidden bits.

In the tested model, the two neighboring anchored groups alone place **no GF(2)-linear restriction whatsoever on the 128 selected output bits**. Equivalently, for each fixed placement, their full 128-bit output projection is surjective onto 128-bit strings within the unrestricted 624-word linear-recursion solution space. This establishes the inadequacy of *these two source groups alone* even when using global exact linear algebra rather than local fixed-point propagation. It is stronger than observing that straightforward peeling recovered zero target words.

## Limits and cracking direction

This result is conditional on the common-stream indexing model and only these two groups' source observations. The symbolic 624-word initial window is unrestricted; genuine CPython seeding may impose additional nonlinear or lower-dimensional initial-state constraints. Other groups are not globally placed, and cross-source donor words presently reported by other agents do not independently anchor the unresolved row43→44 bridge. The full solution space of historical printer implementations is wider and narrower in different directions than this linear model. This computation is **not** a proof that the original K04 coupon is unrecoverable from all surviving evidence.

**Actionable exclusion:** no further local GF(2) propagation, partial-state completion, or local hidden-word inversion restricted to these same two anchored group observations can recover a selected bit without a **new independent constraint**. Prioritize an original-source seed/producer rule or a new cross-group alignment/whole-word observation that enters one of the target's ancestor windows. The independently recovered row99 index3 CLASS sample and row39 DEST output are useful for identifying a plausible producer, but do not supply the missing row43→44 state.

## Reproduction

[`agents/agent49/k04_gf2_target_identifiability.py`](../agents/agent49/k04_gf2_target_identifiability.py) is a read-only single-file reproducible experiment importing the existing SHA-pinned Agent23 witness/group parser. It reads the original local case ZIP, withholds row129, verifies the MT recurrence with independent CPython controls, runs every shift and target placement, and asserts every count and positive control above. No source, original verifier or acceptance file is changed.
