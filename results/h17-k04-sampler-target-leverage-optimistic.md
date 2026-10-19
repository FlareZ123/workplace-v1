# K04: ordinary CLASS/DEST metadata is a poor direct source of coupon bits

**Agent 5, 19 October 2026.** Source-only target-leverage calculation for the exact 42-witness MT19937 model. [Standalone read-only SFT](../agents/agent5/k04_sampler_target_leverage.py). This report **does not recover or authenticate any K04 bytes**. K08 final wording is likewise unresolved.

## Question and new test

Agents 6, 2 and 31 identified striking source-correlated three-bit pre-payload CLASS and two-bit post-payload DEST sampling patterns. Those patterns may help align the unobserved generator consumption. A separate question is whether recovering these particular metadata outputs would algebraically constrain any of the **four missing selected coupon words**.

Use the already source-linked groups without adding another speculative seed recipe:

- Group43: regular rows 12, 43, 66, 96 and tail row128, relative starts `-229,0,167,393,623`.
- Group44: regular rows 13, 44, 67, 97 and tail rows130, 131, relative starts `d-227,d,d+168,d+394,d+620,d+624`.

The shared MT recurrence is `X[t+624]=X[t+397]^twist(X[t],X[t+1])`, with its usual untempered bit31/low31 rule. The complete intact groups provide **1,123 linearly independent equations**. Selected row129 is completely excluded from fitting; its first-output index is `p` and its 128 symbolic bits are withheld.

For each of **eight ordinary rows** in these two groups, add hypothetical observations of:

1. The three tempered high bits of `X[s[row]-1]`, as though the final CLASS accepted draw were recovered completely.
2. The two tempered high bits of `X[s[row]+4]`, as though the first post-payload DEST draw were known. This is **optimistic** because that first draw could instead be a rejection; we grant the analyst its exact bits in all cases.
3. In a stronger upper-bound experiment, grant the analyst **all 32 state bits** of every one of the same 16 immediately pre/post-payload words. This supplies more information than the original metadata labels reveal.

Compute the GF(2) dimension of the four selected target words modulo the original intact words, then modulo each enlarged observation set. Only values from the SHA-256-pinned original spool `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083` are used in source consistency checks; original K04 row129, route mask, slot commitments, K08 nonce and original verifier are never inputs. An independent CPython MT synthetic stream checks the linear recurrence before original-source ranks are evaluated.

## New computational result

The following four admissible placements cover the minimum shift and three larger interior/boundary examples. `p` is the selected row129 starting index relative to row43.

| Unknown shift d | Target start p | Intact-source rank | Rank with all 40 ideal CLASS/DEST bits | Rank with all 512 bits of the 16 metadata-adjacent words | Remaining independent coupon bits (base / topbits / full words) |
|---:|---:|---:|---:|---:|---|
| 11 | 627 | 1,123 | 1,151 | 1,442 | **128 / 128 / 128** |
| 21 | 633 | 1,123 | 1,151 | 1,442 | **128 / 128 / 128** |
| 43 | 655 | 1,123 | 1,151 | 1,442 | **128 / 128 / 128** |
| 65 | 677 | 1,123 | 1,151 | 1,442 | **128 / 128 / 128** |

**The counterfactual full-word metadata observations yield 319 additional independent state equations and still zero constraints on the coupon's 128 bits in all four tested placements.** The 40 ideal sampler high bits contribute 28 independent equations with the same zero target gain. The intact-source equations are consistent in all four cases. These are exact linear ranks under the stated placements; there is no statistical null calculation and no REC8 acceptance test.

## Cracking implication

These observed metadata correlations can serve as **index / producer-order discriminators**. They should not be counted as coupon-byte recovery. Even perfect acquisition of the immediately adjacent sampler words from these eight ordinary rows leaves the four target words completely free in the tested linear model.

The positive route remains a joint observation in the **two target-carrying hidden ancestor windows**: the successors inside row43→44 and the middle words inside row96→97, or an independent producer/seed mechanism that predicts them and passes an intact-source holdout. The earlier [two-window 16-candidate completion](h17-k04-target-leverage-constellations.md) describes the constructive complement to this upper bound. Someone trying to convert more metadata rank into target recovery should first compute the target quotient rather than interpreting additional generator state equations as coupon progress.

**Limits:** Four representative `(d,p)` placements are tested, rather than all 1,540 allowed placements. The two-index-group common-MT interpretation and the locations of the hypothetical samplers are conditional; neither is authenticated historical producer code. The stronger full-word measurement is deliberately counterfactual. Different hidden metadata indices, a nonlinear initialization constraint, future observed words or genuine donors in both ancestor windows could change the target projection. No general impossibility theorem for K04 follows.

**Original REC8 state unchanged:** K01, K02, K03, K05, K06, K07 individually PASS; K04 and K08 MISSING; combined INCOMPLETE and `accepted: false`. Original files and commitments were not altered.
