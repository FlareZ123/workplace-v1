# K04: recursive MT recovery and pre-payload rejection fingerprint

Agent 31, 19 October 2026. Original source computation. K04/K08 still unresolved.

Source: original evidence/print/spool-reconstruction.log, SHA-256 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083. Reproducer: agents/agent31/k04_mt_recursive_peel.py. It imports Agent 23's original-source 42-witness group builder. Selected ESC-N attempt2 row129 is completely withheld, and no acceptance commitment or K04 mask is read.

## 35 additional complete hidden words by fixed-point MT inversion

The existing single-pass inverse-twist reconstruction (results/h17-k04-mt-inverse-hidden-outputs.md) derived 30 complete hidden untempered MT output words in separate row-index groups. Iterating inverse-twist and forward recurrence until no new bits can be added now yields **65 complete unobserved words**, or **35 newly completed 32-bit outputs**. In the group with row43 start at position zero, new full words at offsets 397, 398, 399 are 8D81DC41, 3D1796E7, 441DEC53. They immediately follow the observed row96 block (indices 393..396), near the second K04 hidden ancestor gap. The existing row44 group reconstructed 27D820C7 and 0ACF4761 at offsets -2, -1; the recursive method supplies more distant missing words there.

Implementation check: the original 42 recurrence groups are fixed using the unwithheld original source. The program individually removes each of 264 intact words within multirow groups. It can reconstruct 84 of the 264 words entirely, with **84/84 exact matches and zero mismatches**. Because row-group discovery precedes withholding, this checks mathematical propagation and is not a genuinely independent blind prediction or a proof that one physical generator produced every row.

## New binary rejection/acceptance fingerprint

Temper every full reconstructed MT output immediately before an ordinary printer payload. The high two output bits, equivalent to Python Random.getrandbits(2), are **0 or 1 at all 12 reconstructed ordinary predecessors**:

row3=1, row34=0, row4=0, row13=0, row44=0, row14=0, row45=0, row74=0, row28=0, row30=0, row38=1, row93=1.

For six of those rows, the second-to-last draw is also reconstructable and its top-two-bit value is **2 or 3 at all six**:

row34=2, row4=2, row44=3, row45=3, row38=2, row93=3.

For row4, a third-to-last reconstructed draw has value 3, giving the exact terminal sequence **3, 2, 0**. This is the acceptance/rejection signature of a two-way rejection sampler with k=2 bits: values 2 and 3 are rejected, values 0 and 1 accepted. CPython Random._randbelow_with_getrandbits(2) uses that rule. Nominal chance of 19 such independent half-probability classifications is 2^-19, but source-dependent group selection and analysis choices prevent interpreting that as a calibrated p-value. The record does not identify the historical RNG implementation or an observable binary metadata category.

This is a **specific new producer-consumption hypothesis**. It may explain variable skipped draws without assuming a constant overhead across rows. It does not identify a seed or recover K04.

## Next discriminating crack

Investigate a two-way rejection-sampled draw as the final RNG operation before each regular payload, identify its historical role or a source-observed correlate, and model earlier draw consumption. Check whether that mechanism jointly explains the known row43→44 distance of at least 11, synchronized row96→97 distance of one more, and tail row130→131 distance exactly four. The two hidden gaps still contain the indispensable recurrence ancestors of all four selected row129 words. A model should predict an intact held-out tail output before trusting any selected K04 value. The current finding does not close those gaps. No source record, original verifier or commitment was changed.

## Follow-up: the sampler's choice count is not uniquely identified

An immediate identifiability check is essential: for CPython Random._randbelow(n), **any power-of-two n** has exactly the same *accept/reject* predicate on the high bit of the underlying 32-bit output, because k=n.bit_length() and samples in the upper half of the k-bit range are rejected. The twelve successful predecessors and seven earlier rejected outputs therefore support **rejection sampling with an approximately half-range acceptance gate**, not a uniquely recovered binary-category selection.

Applying the exact CPython getrandbits(k) predicate to all 12 terminal draws and all 7 earlier reconstructed draws for every integer n in 2..999 leaves candidate n values **2, 4, 8, 16, 32, 64, 128, 256, 512, 513**. The two-way n=2 hypothesis is simplest, but n=4 and larger powers of two are observationally equivalent on these selected positions. Even n=513 survives this bounded sample. Do not hard-code n=2 or infer a visible binary field solely from the fingerprint. The actual discriminating experiment must use an independent producer clue, a source-observed choice outcome, or new reconstructed skipped words that break these equivalents.
