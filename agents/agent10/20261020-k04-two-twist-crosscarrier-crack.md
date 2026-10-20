# Original-source two-twist K04 cross-carrier cracking probe (20 October 2026)

**Agent 10. Disposition:** no new selected K04 bits or K08 exact words. This is a new, bounded **source-facing** cross-carrier hypothesis check, rather than a p=955 coupon target-rank exercise. The tested donor topology excludes selected printer spool row129 before *any* state inference, and never uses K04/K08 acceptance commitments, mask or desk nonce. A complete source-pinned local Python run was executed in the present invocation; its 306-line standalone program is in the invocation workspace `/mnt/data/h17case/k04_two_twist_crosscarriers.py` (not yet a permanent repository file).

## Verbatim original anchors and mechanism

Original printer `evidence/print/spool-reconstruction.log` SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`, 132 intact nonselected 16-byte source rows (528 32-bit little-endian, untempered MT state outputs). Independently preserved TRP2 `evidence/recorder/trip-recorder.raw` SHA256 `5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba` (84 CRC-valid 32-bit controls, four explicitly invalid), RC-17 original scan `evidence/procedures/RC-17-scans.txt` four-byte footers, and `evidence/transfers/transfer-audit.jsonl` SHA256 `32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf` containing original 16-bit checkpoints.

The source-only relation `X[t+624] = X[t+397] XOR twist(X[t], X[t+1])` yields, after two twists, with `F(w)=twist(0,w) & BFFFFFFF`, this authentic 31-bit identity:

`(X[u+850] XOR X[u+396]) & BFFFFFFF = F(X[u]) XOR F(X[u+227])`.

The `F` mapping is invertible on 31 source bits. Existing original intact printer quartets (rows 4/35/58/118, 5/36/59/119, and 9/40/63/124) confirm the identity. The new question is whether a *missing fourth* word predicted from three authentic printer inputs occurs in a separately recorded TRP2/RC-17 32-bit field, thus joining formerly disconnected stream-index groups. A second experiment tests two consecutive inferred absent words against consecutive 16-bit AX checkpoints under retained source orders. Any match would first need a defensible source producer/stream-index and a prospective withheld intact original prediction before it could affect the selected coupon.

## Exact source-only experiment

1. Parse source rows and discard row129. Search all 25 exact ordinary one-twist three-source words and join their relative MT positions. Add the three known original two-twist relative equations, preserving all original values. This forms 88 disjoint row-index groups.
2. For every indexed `+454` observed pair (31-bit two-twist C/D anchor) and independent intact printer B or A donor in another group, derive the missing fourth A/B low31 and compare against all CRC-valid TRP2 controls and original RC-17 four-byte footers in both byte orientations. For each indexed `+227` observed A/B pair and an intact C or D in another group, predict the fourth C/D state bits except bit30, and compare the same separately retained sources; explicitly mark bad-CRC TRP2 controls when included. A source match would indicate an unexplained long-index alignment rather than direct K04 recovery.
3. For consecutive printer pairs at indexed `+227` or `+454`, pair a second consecutive source run from another index group and derive two consecutive absent-state terms by the same equation. Compare *both* tempered upper 16 bits simultaneously against all consecutive original CHUNK checkpoints, each in three natural orders (file, seq/attempt, attempt/seq) and two 16-bit orientations.
4. Test against *withheld actual retained printer words*: for each quartet position A/B/C/D separately, infer it from the other three original known words, assert the proper 31-bit/31-bit-with-bit30-missing equality. Four roles PASS. Four separate two-step adjacent control pairs PASS. A real-source positive is a method check, not a blind holdout or new historical donor.

| Original-source measurement | Observed |
| --- | ---: |
| Unselected intact printer words | 528 |
| Exact direct three-word recurrence witnesses | 25 |
| Row-index groups after three original second-order quartets | 88 |
| One missing word inferable wholly within groups from three known source words | 25 |
| Original CRC-valid TRP2 control records | 84 |
| Pair-indexed cross-source A / B / C / D assignments | 7,670 / 7,667 / 31,258 / 31,256 |
| **New 32-bit external-control matches** | **0** |
| AX candidate stream views and 16-bit values | 24 / 384 |
| Two-step A / B / C / D assignment counts | 3,455 / 3,452 / 13,846 / 13,845 |
| **Two-halfword original AX source matches** | **0** |
| Authentic withheld printer-word controls | **4/4 PASS** |
| Authentic adjacent two-step controls | **4/4 PASS** |

Counts are candidate assignments, not independent random variables. The one-word output's 31-bit/bit30 omission is handled exactly; both endian options are tested. The transfer test insists on two simultaneous original checkpoint halfwords and no rearrangement of their relative two-step order.

## Information gain and stop rule

This specifically eliminates the scanned straightforward **two-twist raw-control-copy** family and pair-consecutive AX high16 bridge; it discovers **no** original donor that joins missing target-ancestor indices, and contributes **zero** observed coupon bits. Source timestamps and output order still do not authenticate a common PRNG. Its positive controls establish algebra and source-parsing fidelity only. Earlier first-order crosscarrier tests did not report this four-term second-order source-join geometry, but this result must remain below discoveries until there is new observed target information.

Do **not** inflate this miss into a rejection of an actual physical common producer or all MT index placements; do not repeat further unindexed donor permutations or hypothetical p955 bit-rank tables. Original K04 acceptance remains missing, K08 final words missing, combined not accepted. No original evidence, nonce, mask, acceptance hash or verifier modified.
