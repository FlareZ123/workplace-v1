# K04: three new original 31-bit two-twist printer chronology anchors

**Agent 1, 19 October 2026 ~23:16 UTC.** Original-source computational finding, beyond the previously catalogued 25 within-row plus 17 boundary MT recurrences. **No original coupon bytes recovered.** Read-only standard-library [SFT](../agents/agent1/k04_two_twist_31bit_source_witness.py); the original row129 selected coupon and the K04/K08 hash commitments were **never read** for this search.

## Exact second-order MT19937 source relation

Write `X[t]` for untempered MT19937 32-bit state-output words, and `twist(a,b) = ((a & 0x80000000)|(b & 0x7fffffff)) >> 1 XOR ((b & 1) ? 0x9908b0df : 0)`. The established MT recurrence is `X[t+624] = X[t+397] XOR twist(X[t],X[t+1])`.

Apply it twice, at `t` and `t+227`:

`X[t+851] XOR X[t+397] = twist(X[t],X[t+1]) XOR twist(X[t+227],X[t+228])`.

On every bit other than bit30, `twist(a,b)` depends only on `b`; define `F(w) = twist(0,w) & 0xBFFFFFFF`. Taking `u=t+1` gives an **exact 31-bit equality**:

`(X[u+850] XOR X[u+396]) & 0xBFFFFFFF = F(X[u]) XOR F(X[u+227])`.

This source-only relation is a **four-word check** at offsets `u, u+227, u+396, u+850`, distinct from the previously used single-step three-word inverse. It is asserted for 449 withheld-index control positions on genuine `random.Random(20261019).getrandbits(32)` outputs.

## Original source scan and independent new source-index edges

From the 133-row original SHA-pinned printer log, with selected row129 excluded, untemper exactly 528 retained 32-bit words and join ordered pairs by their 31-bit identity. The SFT found **15 original matched ordered quartets** (all of them listed internally by the reproducer and in the original scan). Of these, the following **three quartets provide nine source-index relations not already implied by the earlier 42 witness recurrences**:

| Original source quartet `(row, word)` | `s_b-s_a` | `s_c-s_a` | `s_d-s_a` |
|---|---:|---:|---:|
| (4,3), (35,0), (58,0), (118,1) | 230 | 399 | 852 |
| (5,3), (36,0), (59,1), (119,3) | 230 | 398 | 850 |
| (9,2), (40,0), (63,0), (124,0) | 229 | 398 | 852 |

**Graph effect:** the 42 existing source recurrences give 84 independent rigid row-start components across 133 printer rows; accepting these three disjoint second-order relations reduces the component count to **75**. The other 12 observed 31-bit quartets are consistent with, or already implied by, these and the old witness graph, including a separate, adjacent-original-word recurrence (9,3), (40,1), (63,1), (124,1). That adjacent four-word check corroborates the row9/40/63/124 assignment using different preserved payload words, but was identified within the same retrospective exhaustive scan, **not a preregistered holdout**.

A broader 30-bit scan returned 18 matches; the three extra isolated matches failed the additional high-bit relation and are excluded from every proposed chronology equation. The 31-bit scan has no contradictions against the established 42-edge graph. The original source data, mask, selected attempt and verifier have not been modified.

## Interpretation and targeted next step

These are three new **original-source conditional producer/index anchors**, unlike a general seed-length exclusion or an unindexed donor permutation. Under the common MT stream and chronological-row hypotheses, the three quartets impose nine precise relative row-start equations. Their support combines actual original 31-bit word identities, chronological word ordering, exact MT algebra, and compatibility with all previously anchored recurrences. The index inferences remain model-conditional: an incidental 31-bit pair collision is possible in a broad exhaustive join, and the actual printer producer implementation is still unauthenticated.

Integrate these nine new source-only equations into Agent37's global original chronology solver, retaining all 42 earlier recurrence anchors, ordinary-row minimum metadata consumption and full inverse source contradiction checks. For any resultant **zero-contradiction 133-row vector**, immediately feed the full 528-word projector from Agent33 and the [new all-row CLASS/DEST parity extension](h17-k04-all-row-destination-parity-target-projection.md). Report original selected coupon quotient rank, actual fixed masks and independently held-out source predictions. A provisional MILP vector with even a single source contradiction remains invalid. No original K04 bit or K08 final word is yet recovered.

The original 31-bit scan used only `evidence/print/spool-reconstruction.log` (SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`). No K04 mask, nonce, acceptance digest, or source row129 payload entered the witness-generation path.
