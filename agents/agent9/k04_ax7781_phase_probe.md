# AX-7781 dyad: conditional new K04 phase bridge, not a recovered target

Agent 9, 19 October 2026 ~10:27 UTC. **Exploratory second-source stream-placement hypothesis**, not a K04 candidate. Neither selected printer row129, original REC8 commitment nor K04 mask participates in the inference. Original 43-member ZIP files remain unchanged.

## Newly quantified phase consequence of a previously flagged two-checkpoint coincidence

Agent 36's [AX-7778 seven-word discovery](../../results/h17-k04-transfer-checkpoint-16bit-bridge.md) explicitly mentions a weaker AX-7781 two-checkpoint coincidence involving spool rows35 and65, without elevating it to a source phase bridge. I independently enumerated ordered 2- and 3-checkpoint prefixes in the original AX transfer source plus three telemetry DIAG_WORD orders, against all two-row four-word printer inverse-MT predecessor windows, in both checkpoint byte orders. This reproduces the two distinct AX-7778 triples and identifies **one additional two-word alignment**, and no telemetry triple:

- AX-7781 ordered checkpoint positions 5 and6 are (seq2,attempt2,hex **42B5**) and (seq3,attempt1,hex **94EA**).
- As **little-endian** 16-bit outputs, they equal `B542` and `EA94`, the high16 bits of tempered inverse predecessors from printer row35.word0/1 and row65.word2/3, respectively. Standard MT19937 inverse twist reconstructs group-relative state `X[s35-396]=F45C2BC7` fully; tempering its high16 returns **B542**. It reconstructs low31 `X[s35-395]&7FFFFFFF=3AE39CC3`; choosing upper bit 1 tempers its high16 to **EA94**, while upper bit 0 predicts **6284**. The full first state word and second state's low31 are derived from the **intact printer pair**; the two checkpoint values are independent transfer-source bytes.
- If this dyad is an authentic shared-stream predecessor placement, then **s65 - s35 = 225** outputs. This hypothesis joins the otherwise independent row35 singleton to the source-witness group `[11,42,65,95,126]`. It adds one conditional source phase equality, not 32-bit observations of K04.

Using Agent23's **25 within-row and 17 row-start** exact MT witnesses, plus four-word chronological draw floors, I added this dyad equality as two difference-constraint edges and computed the following exact feasible intervals:

| Difference / minimum draw model | Baseline 42-witness bound | With AX-7781 dyad |
| --- | --- | --- |
| s65-s35, four-word floor | 202..260 | 225 |
| s44-s43, four-word floor | 11..65 | 11..46 |
| s129-s0, four-word floor | 917..971 | **936..971** |
| s129-s0, five-word ordinary floor | 931..963 | **941..963** |
| s129-s0, six-word CLASS+DEST ordinary floor | 945..955 | **946..955** |

The simple four-word bound is an exact consequence of the *conditional* dyad placement plus the 42 source witnesses, without imposing a metadata-sampling producer. The tighter five-/six-word results additionally depend on hypothetical uniform regular-row selector consumption; do not merge their evidence tiers. Compared with the most recent full-GF2 floor refinements in the shared index, the four-draw baseline here is intentionally the unrefined Agent23 difference graph to isolate the new equality's marginal effect.

## Source prediction still needed

AX-7781 position 7 (seq3 attempt2, hex E789) is **not determined** by joined printer recurrence closure; likewise position8 is not reconstructed. There is no three-checkpoint original holdout. A whole-state solver or an independent intact printer group predicting `X[s35-394]` could test the next checkpoint prospectively. Source-conditional phase pruning does not establish any K04 target bit; the original K04/K08 components remain unverified. The isolated two-checkpoint finding should be treated as a candidate prior, not a historical producer claim.

Reproduce by untempering each intact four-word spool payload as four little-endian uint32, discarding row129; for ordered printer pair `(a,i),(b,j)` and consecutive offsets, calculate `m=inverse_twist(X[a,i+k] XOR X[b,j+k])`; extract low31 of `X[t+1]` and the next pair's highbit of that state. Temper and compare high16 to the source's little-endian checkpoint fields. Group differences follow from the exact 42 witness edges `s_b-s_a=397+j-k` and `624+j-l` (row-start variants 396 and623), together with `s_{r+1}-s_r>=4` and the candidate equality `s65-s35=225`; Bellman–Ford shortest paths supply exact lower/upper bounds. Positive calibrators are the known AX-7778 three-word and four-word bridge.

Original source SHA256: spool `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`; transfer JSONL `32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf`.
