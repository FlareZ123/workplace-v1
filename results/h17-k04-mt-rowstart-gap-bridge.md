# K04 MT19937: recover row-start predecessor-bit witnesses and cross-tail gap bridge

Agent 23, 19 October 2026. **A new source-only constraint class and K04 target-spacing bridge; no K04 acceptance PASS.** Source: original 43-member local export, `evidence/print/spool-reconstruction.log`, SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Reproducer: [`agents/agent23/k04_mt_rowstart.py`](../agents/agent23/k04_mt_rowstart.py), runnable with the unmodified original ZIP. Selected row 129 is **withheld entirely** from discovering recurrence witnesses; neither commitments nor K04 mask are loaded.

## Technique

For an unknown 32-bit untempered MT19937 output `x[k]` directly **before** the first observed 32-bit word `x[k+1]` in any record, the recurrence

`x[k+624] = x[k+397] XOR twist(x[k], x[k+1])`

depends on only **one unknown bit** of `x[k]`: its high bit. The other 31 bits do not enter `twist`. Test both high-bit possibilities against all later fully observed middle/end words. This is different from the 25 within-record witnesses, which use fully known adjacent source words. It does **not** assume the preceding record ends directly before the next record; an inter-record draw gap may intervene.

The unchanged 133-record spool gives **25 previously reported within-record witnesses plus 17 new first-word (missing-predecessor) witnesses**, counting each exact matching triple once; no selected-row word participates. Examples in zero-based `(record, word)` coordinates, with inferred predecessor high bit:

- `(row 43, bit 1) -> (96,3) -> (128,0)`
- `(row 44, bit 0) -> (97,2) -> (130,3)`
- `(row 45, bit 1) -> (98,2) -> (132,2)`

The solver includes all 42 witness triples and chronological row-start lower bounds `s[r+1]-s[r]>=4`; the difference constraints are **jointly feasible**, unlike interpreting certain previously observed cross-record triples as evidence of adjacent records. Conditional on all observed relations reflecting a single stream, the new first-word equalities yield:

`s128 = s43 + 623`

`s130 = s44 + 620`

`s131 = s44 + 624` (also independently obtained from a within-record witness).

Thus **`s131-s130=4` exactly**: rows 130→131 contain no intervening MT draws. For the hidden selected row129, monotonic placement between rows128 and130 gives

`s128+4 <= s129 <= s130-4`.

Substitution yields **`11 <= s44-s43 <= 65`**, where the upper value is the tight all-witness difference-constraint bound. Define `g[r]=s[r+1]-s[r]-4`, the skipped draws after a four-word record. The especially useful exact identity is:

`g128 + g129 = (s44-s43) - 11`.

This links the number of invisible generator draws surrounding the **selected K04 attempt-2** directly to an earlier regular-cohort transition. If that earlier distance is eleven, rows128→130 are contiguous; if it is larger, the excess must be allocated across the two tail gaps. The selected row start's tight source-relative interval changes from the previous **916..971** to **917..971**, or 55 integral possibilities, under the shared-stream model and the expanded witness set.

## Correction to cross-record adjacency readings

A previously observed exact match `twist(x43[3],x44[0]) XOR x97[2] = x130[3]` was interpreted conditionally as implying `s44=s43+4`. This inference is **not valid from the equality alone**. `twist(a,b)` depends on only the highest bit of `a`. The high bit of `x43[3]` may equal the unobserved predecessor's high bit for `x44[0]`, even with many skipped outputs. Under that interpretation the recurrence is anchored at **`s44-1`**, and the new cross-tail bridge shows **`s44-s43>=11`**. An adjacent-record assumption `s44-s43=4` would contradict the jointly feasible 42-witness placement. This is a model-choice discrimination, not a finding that any spool bytes are corrupt.

The 12-byte conditional K04 reconstruction communicated by Agent 42 on 19 October assumed `s44-s43=8`. That exact branch is ruled out *if* the new first-word witness set and single-stream assumptions are valid. The original K04 hash remains untouched, and no guessed byte is promoted as accepted.

## Limits and next attack

The first-word witnesses are data-discovered and their exact MT matches do not independently prove a single historical PRNG instance or the absolute stream origin. The effect of treating source-cohort records as one stream remains conditional, while the finite identities and feasibility checks are reproducible. They constrain the missing draw budget without reconstructing the four withheld 32-bit words. The selected target's required preceding 32-bit words lie in the unobserved interval between rows43 and44 under the bridge equations, suggesting a **hidden-gap state reconstruction** or source-supported consumption rule before another K04 hash search. Seek a predictive model for `s44-s43` and the split `(g128,g129)` that also predicts intact tail words. Preserve source bytes, original acceptance commitments and verifier unchanged. K08 remains unresolved.

## New geometry: every selected word's immediately preceding MT input lies in a hidden regular-cohort gap

Write `q=s129`, and let `j=0..3` select the four words of the withheld ACK. The standard recurrence uses `x[q+j-624]`, `x[q+j-623]`, and `x[q+j-227]` to predict `x[q+j]`. The exact boundary identities give `s128=s43+623` and `s130=s44+620`, so chronological four-word records enforce

`s43+627 <= q <= s44+616`.

Consequently, for **every** `j=0..3`,

`s43+4 <= q+j-623 <= s44-4`.

That particular `x[q+j-623]` is in the unobserved word interval **after row43's fourth word and before row44's first word**. Thus **no selected 32-bit word can be predicted using one ordinary MT twist recurrence fed exclusively by fully observed earlier source words**, regardless of where the selected ACK is placed in its allowed stream-index window. This is a purely symbolic obstruction under the same conditional 42-witness model, requiring no acceptance hash, brute-force candidate enumeration, or assumed seed.

The obstruction identifies a precise cracking target: recover the unseen 43→44 gap outputs (at least seven words), or infer selected words by a multistep inversion/seed model that does not require direct access to the gap. It also explains why treating a cross-record `twist(x43[3],x44[0])` match as evidence of immediate adjacency would produce artificially optimistic K04 predictions.
