# K04: p621 period171 seeded-state edge rejected by AX8/9 checkpoint and printer metadata predictions

**Agent 18, 19 October 2026 ~15:13 UTC.** New source-conditioned edge extension of [our four-step 171-period seed bridge](h17-k04-row9-period171-fourstep-seed-bridge.md). The first-cycle `p=621` candidate was excluded from that source-only initialized-state test because `S[p+3]` would incorrectly denote array index624. Here **all indices remain within 0..623** and the model is tested with a different, explicitly **stronger** assumption: AX checkpoint positions 8/9 were generated immediately before the two post-row9 / pre-row10 metadata samplers, with no additional MT draws. This is a contested producer-order hypothesis, not an authenticated fact.

## Constructive p621 two-sampler predictions

The original row9→10 six-output hypothesis places row9 DEST at first unobserved word `X[p−172]` and next row10 CLASS at `X[p−171]`. The preserved original spool literally records row9 `DEST=store`, whose assumed `getrandbits(2)` top2 value is 0, and row10 `CLASS=STORES`, whose assumed `getrandbits(3)` top3 is 1.

AX-7778 source checkpoint positions 8/9 have original little-endian bytes **`7CA7`** and **`A234`**, giving independent presumed upper16 tempered generator outputs **`A77C`** at `X[p−399]` and **`34A2`** at `X[p−398]`, respectively. These are source observations rather than guessed bytes.

Use the same Agent28 source row9 initialized-state window `S[p−174]=418BDA1E,S[p−173]=2E02BC3D,S[p−172].low31=38EBB043` and Agent26 five complete late source state words `S[p−2..p+2]`, with **p=621**. For each seed-array word length `n` dividing171, three exact late KEY residues imply `S[p−171]` and `S[p−170]` from two forward CPython `init_by_array` steps. Two possibilities for `S[p−172].high` remain. The first-cycle MT output recurrence yields the two predicted metadata high16 values without needing unknown checkpoint low bits:

```text
predicted_DEST_high16 = A77C XOR temper(twist(S[p−172],S[p−171])).high16
predicted_CLASS_high16= 34A2 XOR temper(twist(S[p−171],S[p−170])).high16
```

They are the same for every `n=9,19,57,171` because the modular key indices alias over the 171-step separation.

| `S[p−172]` unknown high bit | Predicted DEST high16 | Predicted DEST top2 | Predicted CLASS high16 | Predicted CLASS top3 |
|---|---|---:|---|---:|
| 0 | `9CB3` | **2** | `FE9E` | **7** |
| 1 | `BD0E` | **2** | `C666` | **6** |
| Source-required | | **0** | | **1** |

Neither branch matches *either* of the independently recorded selector values. Hence **p621 is excluded for these seed lengths under the ordered-AX8/9 plus exactly-two-samplers assumptions**. This does not use any trailing S624 seeded state, any selected K04 row129 bytes, acceptance hashes or K08 caption.

[Read-only SFT](../agents/agent18/k04_row9_p621_ax89_metadata.py) SHA-pins the original transfer and spool, reuses the independently original-derived Agent26/28 initialized state windows, and verifies **20 actual CPython seeded synthetic positives** over four distinct numeric key-array lengths `9,19,57,171` and five phases `402,430,535,620,621`: the predicted full high16 metadata outcomes exactly match true generated outputs under the matching synthetic AX high16s. **20/20 PASS**. The original source comparison above is exact.

## Scope against the main 219-phase bridge

Our preceding four-step bridge rejected **p402..620** for n9,19,57,171 using a full32 independently preserved seeded-state holdout and **without AX8/9 adjacency**. The present p621 result extends that family to **p402..621** but only with the additional AX8/9 ordered metadata-draw premise. Keep those tiers strictly separate; do not promote this 16-bit source checkpoint to proof of actual generator chronology or physical producer identity.

K04's selected masked coupon bytes and K08's exact final inscription remain missing. Original accepted components are K01/K02/K03/K05/K06/K07 only; **combined recovery remains INCOMPLETE and false**.
