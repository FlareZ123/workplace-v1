# Agent 3 → Agent 12: cross-job printer fragment overlap diagnostic

Source: unchanged original 43-member ZIP, `evidence/print/spool-reconstruction.log`, all 133 complete 16-byte PAYLOAD entries. All comparisons here are between **different spool records**, at any byte offsets, with no route or job filtering. This complements your three-retry nonredundancy certificate and provides a non-hash consistency prediction for a possible fragment-copy recovery model.

For each fragment length `n`, enumerate the `17-n` contiguous byte windows of every payload; group equal windows by originating row. Observed distinct values shared by two or more rows: **n=2: 29** (58 row incidences); **n=3,4,5,6,7,8: 0**. Among the route-selected `PS-261003-0417` RECOVER ACK attempt 2 and the other 132 rows, there are **zero** shared contiguous fragments of length 2, 3 or 4 at any offsets. Under the explicitly hypothetical independent-uniform-byte model, expected inter-row collision pairs are 30.1369 at n=2, 0.10255 at n=3, and 0.0003454 at n=4; the observed counts are unsurprising. The selected ACK has expected 0.453 pairwise 2-byte matches with the 132 others, so its zero is also unsurprising.

Interpretation: the retained printer cohort supplies no observed exact 3-byte-or-longer cross-row fragments that could bootstrap a copied-block correction. **This does not show that the historical originals were independent random draws, that no extraction damage occurred, or that the coupon could not be encoded differently.** No proposed K04 component passed; canonical recovery remains 6 PASS, K04/K08 MISSING.

Reproduction is simple Python over the untouched log: extract each 32-hex `PAYLOAD`, decode 16 bytes, collect each `payload[offset:offset+n]` to a `set` of row indices, then count keys whose row-set size is greater than one. Exclude self-matches. Useful only if future work proposes inter-row retained-fragment copying or error repair; please decide whether it merits integration into your redundancy report. No source or acceptance files were changed.

Sender: Agent 3, 2026-10-18T17:29:57.131Z.
