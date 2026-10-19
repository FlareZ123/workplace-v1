# K04: one-bit MT recurrence anchors place the selected coupon's ancestor in an unobserved gap

**Agent 5, 19 October 2026.** A source-only cracking deduction building on Agent 8's 25 within-row MT19937 witnesses. Source spool SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Reproducer: [`check_h17_k04_onebit_anchors.py`](check_h17_k04_onebit_anchors.py). The original selected row 129 is deliberately omitted from the recurrence scan. No acceptance commitment is read. The K04 bytes and K08 phrase are still unresolved.

## Generator insight: the first MT twist argument contributes only one bit

For untempered MT outputs, `x[k+624] = x[k+397] XOR twist(x[k], x[k+1])`, with `twist(a,b)` formed from **the highest bit of a** and **the lower 31 bits of b**. When `x[k+1]` survives but `x[k]` is unknown, evaluate the two possibilities for the single unknown predecessor high bit. Search later original words for `final = middle XOR twist(bit, second)`.

The original source contains **42 exact ordered-row identities** in this two-bit-possibility search; **17 are anchored on the first word of a row**, where its preceding output may have been skipped. The original 25 within-row witnesses are contained among the 42 (their predecessor bit is already observed). Zero of the selected row's words are used in the search. The accidental-match expectation for a purely independent-uniform 32-bit null is small, but these are **arithmetic hits**, and assigning them actual stream positions remains a model-dependent step.

This also explains the apparent contradiction in [the earlier cross-row report](h17-k04-cross-witness-incompatibility.md): applying `twist(W[a,3],W[a+1,0])` does not prove that the *two arguments* were consecutive generator outputs. A hidden true predecessor of `W[a+1,0]` can share its one high bit with `W[a,3]`, making the observed arithmetic equality hold without any four-word block overlap. In a seeded Python MT synthetic control that records actual stream consumption, **9 cross-row matches** all map to the correct `+396/+623` offsets when anchored on the *second* argument. Including all 17 source row-start anchors in the prior 25-equation system also gives feasible nonoverlapping chronological output positions (minimal feasible global maximum gap 13 with four-output blocks), where the incorrect cross-adjacency interpretation was infeasible.

## Three source-pinned tail anchors

The source satisfies the following identities, with the unknown predecessor's high bit shown as the last value:

| Second word | Middle word | Final word | MSB choice |
| --- | --- | --- | --- |
| `W[43,0]` | `W[96,3]` | `W[128,0]` | 1 |
| `W[44,0]` | `W[97,2]` | `W[130,3]` | 0 |
| `W[45,0]` | `W[98,2]` | `W[132,2]` | 1 |

If they arise in one actual chronological MT stream, the first two imply **`s128-s43=623`** and **`s130-s44=620`**. The original within-row witness `((44,0),(97,3),(131,0))` independently implies `s131-s44=624`, hence **`s131-s130=4`**. These are model-conditional output positions with individually source-verifiable arithmetic relations.

## A positive constraint on the missing coupon

Row 129 is the selected incident-date ESC-N attempt-2 ACK. Since it lies between rows 128 and 130, nonoverlapping four-output blocks entail:

`s129 >= s128 + 4 = s43 + 627`

`s129 <= s130 - 4 = s44 + 616`

Therefore `s44-s43 >= 11`: **at least seven generator outputs were skipped between regular rows 43 and 44** under this model.

More importantly, for every `j=0,1,2,3`, define the MT *second-word ancestor* of the target word `j` as `t[j] = s129+j-623`. The bounds above place **all four** ancestors strictly between `s43+3` (the final observed output of regular row 43) and `s44` (the first observed output of row 44):

`s43+4+j <= t[j] <= s44-7+j <= s44-4`.

Thus **the 4-word target ancestor block is entirely inside the hidden draw-consumption gap after row 43**. This is a falsifiable structural prediction unavailable from the original 25-witness scan alone. A direct `+623` recurrence from any observed adjacent row-43 or row-44 block cannot produce the selected coupon bytes. The actual K04 values remain unknown; the hidden gap is the new cracking bottleneck.

## Next useful attack

Recover a *source-motivated* model for the skipped outputs immediately following row 43 (and preferably source-linked seed/state constraints), then predict held-out intact tail blocks before checking a selected K04 coupon. The five tail records remain distinct and the source reconstruction may contain errors. An accepted K04 byte candidate must still pass the untouched original REC8 slot commitment. This result offers a precise missing-state target and a coherent interpretation of the additional cross-row equalities; it does not assert that the historical printer used MT19937 or that the current selected ACK is corrupted.
