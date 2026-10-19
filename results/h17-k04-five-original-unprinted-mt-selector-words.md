# K04: five complete original unprinted selector state words reconstructed

**Agent 1, 19 October 2026 ~23:35 UTC.** New direct original-source MT state reconstruction, not selected K04 coupon bytes. The original 43-member export supplies all evidence for these values. [Read-only, standalone source and synthetic SFT](../agents/agent1/k04_two_twist_original_hidden_words.py). Original row129, K04 mask, original hash commitments, nonce and REC8 verifier were never consulted.

## How the words are recovered

The new [three original 31-bit two-twist quartet anchors](h17-k04-original-two-twist-31bit-new-chronology-anchors.md) give index-locked links between early, middle and late intact printer words under a common MT19937 output stream. The 31-bit relation

`F(X[u]) XOR F(X[u+227]) = (X[u+396] XOR X[u+850]) & 0xBFFFFFFF`, with `F(w)=twist(0,w)&0xBFFFFFFF`,

allows one **unprinted early/middle** state to be reconstructed from the other three intact *shifted* witnesses. Here F is invertible over the 31 low state bits: bit31 of F gives bit0 of the state, and the 30 low bits recover its state bits1..30. Original `CLASS` and `DEST` metadata then selects between the two remaining state MSB possibilities.

Three shifted original quartet placements are particularly valuable:

1. Source quartet r4w3, r35w0, r58w0, r118w1, and its **+1 and +2 indexed shifts** each retain all three last source words. These three source words predict the low31 of r4's **first two post-payload DEST draws**. Both possible first-two-draw codes are `{1,3}`, while original row4 DEST is **store=0**. Therefore neither may accept desk1; both must be rejection code3, fixing the MSB for each.
2. Source quartet r9w2, r40w0, r63w0, r124w0, and its **+2 and +3 indexed shifts**, likewise yield complete low31 predictions for row9's first two DEST draws. The first can only code1 or3, so it rejects. The second can code2 or0, and row9 original DEST is store0, so it must accept immediately with code0, fixing the MSB. This establishes **exactly two DEST samples** in this conditional original row.
3. Source quartet r5w3, r36w0, r59w1, r119w3, shifted **-1**, leaves its second index as row36's final immediately pre-payload **CLASS** sample; the other three full original words survive. The predicted low31 yields tempered CLASS high3 `{4,0}`; original row36's CLASS is **LABEL=0**, so the accepted value must be code0, fixing the MSB.

## Reconstructed 32-bit original latent state

| New original hidden location | Untempered MT `X[t]` | Exact tempered output | Metadata consequence |
|---|---|---|---|
| row4 at `s4+4` | **81BB818B** | F5A7DF12 | DEST rejection 3 |
| row4 at `s4+5` | **8AF3AD7E** | F00ECB88 | DEST rejection 3 |
| row9 at `s9+4` | **8DAE2276** | F377FB6F | DEST rejection 3 |
| row9 at `s9+5` | **DE28452A** | 0F3393EE | DEST accepted store 0 |
| row36 at `s36-1` | **A0EB5B13** | 14DB574E | CLASS accepted LABEL 0 |

The two consecutive original DEST rejections at r4 increase its ordinary row transition floor to `s5-s4 >= 8` (four payload words + at least three DEST draws + at least one next CLASS draw). Row9's rejected-then-accepted DEST sets `s10-s9 >= 7`. These are exact **under the hypothesized no-extra-call, metadata gate boundary order**, and do not assert the whole producer order is historically authenticated. The five full words are new intact inferred source state observations, useful to add as five extra GF(2) rows/words to the whole-spool target projection once an original chronology exists. They may also generate new recurrence/index witnesses through a second source-only scan.

## Evidentiary strength and limitations

The SFT checks the original SHA-pinned spool, verifies all three original 31-bit quartet equalities, and performs 1,024 synthetic inverse-F controls from true CPython MT outputs. This derivation uses *multiple separate original words* and actual original selector labels; it predicts unprinted state rather than a free-choice hash candidate. Nevertheless historical proof of an actual common MT producer is still missing, and the recovered state positions are **row-relative** until an exact global chronology is fixed.

None of these five latent state words is an accepted or authenticated K04 selected-row coupon. **Original K04 selected bits recovered: 0 of 128.** The correct next measurement remains full indexed source consistency and source-only rank of the missing row129 target, with these five hidden words and the all-row CLASS/DEST constraints appended. K08 verbatim final words remain absent.
