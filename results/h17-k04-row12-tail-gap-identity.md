# K04: four original MT witnesses couple row12 rejection draws to the selected row129 gaps

**Agent 45, 19 October 2026 ~13:34 UTC. New source-conditional cracking relation, with a complete 10-row source-only SFT. No K04 coupon or K08 caption recovered.**

## Original-record anchors

The original `evidence/print/spool-reconstruction.log` (SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`) contains four exact 32-bit MT19937 inverse-twist witnesses previously included among Agent23's **17 predecessor witnesses**:

| Unknown predecessor | Middle intact word | Later intact word | Predecessor MSB |
| --- | --- | --- | ---: |
| (row12, before word0) | (row66, word0) | (row96, word1) | 0 |
| (row13, before word0) | (row67, word1) | (row97, word2) | 1 |
| (row43, before word0) | (row96, word3) | (row128, word0) | 1 |
| (row44, before word0) | (row97, word2) | (row130, word3) | 0 |

For each, the observed equality is `X[later] XOR X[middle] = twist(MSB<<31, X[row,0])`. The missing predecessor's 31 low bits are irrelevant to the test; the opposite MSB completion fails. The [standalone SFT](../agents/agent45/k04_row12_tail_gap_identity.py) SHA-pins the original spool, untempers only ten intact source rows, checks these four complete 32-bit equalities, and runs three actual CPython MT positive recurrence controls. **Disputed row129, K04 mask, all commitments, verifier and K08 nonce are excluded.**

## New direct elimination

Let `s[r]` denote the first MT output used for spool row `r`, and `g[r] = s[r+1] - s[r] - 4 >= 0` the invisible draws after its four-word payload. The standard MT19937 recurrence separates predecessor, middle and later words by 397 and 624 output positions. The four original equalities therefore give:

```text
W12: s96  - s12 = 622
W13: s97  - s13 = 621
W43: s96  - s43 = 393       and  s128 - s43 = 623
W44: s97  - s44 = 394       and  s130 - s44 = 620
```

Subtract W12/W43 to obtain `s43=s12+229`. Subtract W13/W44 to obtain `s44=s13+227`. Therefore `s44-s43=(s13-s12)-2`, i.e. **`g43=g12-2`**.

The two later relations yield `s130-s128=(s44-s43)-3=(s13-s12)-5`. Rows128 and129 together must contribute at least eight MT draws because each has four consecutive payload words. Substituting `s130-s128 = 8+g128+g129` and `s13-s12=4+g12` yields the exact new source-conditioned identity:

```text
g128 + g129 = g12 - 9
g12 >= 9.
```

This is an explicit early-to-tail bridge, not merely another local skip lower bound. **At least nine unrecorded 32-bit outputs must occur between consecutive intact ordinary rows12 and13** if all four source matches share the same chronological MT stream. A global linear-programming feasibility test of all 42 established witnesses independently corroborates that **no assignment with every `g[r] <= 8` exists**, even without importing the previously published local lower-bound floors; there is a feasible integral assignment with cap9. A greedy infeasible subset is precisely these four predecessor witnesses. The four-witness algebra above supplies the simpler exact proof without requiring an optimizer.

## New target-facing prediction

Because `s128=s43+623`, the selected printer row129 begins at

```text
s129 = s43 + 627 + g128,
where 0 <= g128 <= g12-9.
```

The hypothesis **`g12=9`** yields `g128=g129=0` and uniquely fixes `s129=s43+627`. The hypothesis **`g12=10`** leaves only the two splits `(g128,g129)=(0,1),(1,0)` and selected positions `s43+627` or `s43+628`. Higher `g12` creates exactly `g12-8` possible nonnegative split allocations.

Thus a **separately source-authenticated count of the early row12→13 nonpayload draws** would immediately fix or sharply restrict the original target-adjacent draw allocation, without searching the target hash. The recovered row13 preword and any producer `CLASS/DEST` sampler hypothesis should be tested specifically against this unusually long early gap. A universal maximum-eight-gap producer is excluded under the four-witness model. Importantly, fixing the target *position* does not determine the four 32-bit payload words: the missing row43→44 ancestral outputs remain necessary.

## Confidence and limitations

- **Source observations:** four exact inverse-temper/twist equalities from preserved intact payloads (not selected row129). This report derives a new relationship from previously known witnesses; it does not claim new independent carrier bits.
- **Mathematical consequence:** the displayed equality and nine-draw floor are exact given a common, monotonically emitted MT19937 stream, a four-output payload per spool row, and these particular predecessor-index assignments.
- **Unverified historical premises:** shared physical generator and output creation order. Inter-device acquisition timestamps already challenge simple on-demand chronological interpretations. Records do not supply actual printer producer code or certify every payload.
- **Recovery status:** K01/K02/K03/K05/K06/K07 previously PASS; K04 and K08 unresolved. No original acceptance hash queried in this experiment and no complete key has been accepted.

Suggested next discriminating research: reconstruct/source-classify the **nine-plus** invisible row12→13 words using the now coupled row43 gap and any independently grounded producer calls, then test whether a producer predicts the untouched row13 label and original later row44/130 outputs. Avoid a blind search of row129 values or caption paraphrases.
