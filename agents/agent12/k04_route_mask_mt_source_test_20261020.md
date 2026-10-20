# K04 source mask as a possible independent MT ancestor/future witness (20 October 2026)

**Agent 12; original-data, source-only, target-oriented hypothesis test.** The K04 route rule records an actual 128-bit `masked_component` in `resources/evidence/recovery-routing.json` independently from the printer export. Ask whether this four-word 128-bit source field is itself a consecutive MT19937 output run and can therefore serve as an already-surviving **independent state donor**, potentially escaping the known 128-bit printer-only target nullspace. This is a *hypothesis* about origin, not a sourced fact: the original routing file calls the field an XOR mask and never identifies its producer.

## Prospective test without target leakage

Read the 16 routing-mask bytes as four 32-bit tempered words, trying both direct/reversed word order and both big-/little-endian serialization. Untemper with the standard MT19937 map. Read each of the 133 original printer spool payload records except the **selected RECOVER ACK** `JOB=PS-261003-0417 ATTEMPT=2 STATE=ACK`, which is wholly excluded prior to inference. Exactly **132** nonselected four-word runs remain; no K04 digest, selected coupon content, mask-XOR result, K08 text or verifier acceptance is used.

The exact recurrence `X[t+624]=X[t+397] XOR twist(X[t],X[t+1])` gives a strong two-equation fingerprint among contiguous three-word slices of an early run, two-word slices of a middle run and two-word slices of a future run. For **all 8,646 chronologically ordered pairs** of nonselected spool runs and the four mask interpretations, test mask in **each of the three roles** (early, middle, future), allowing valid within-run offsets 0..2. An exact hit requires **two consecutive full 32-bit equations**, rather than a weak one-word coincidence.

## Controls and observed result

The same two-equation matcher discovers **seven actual exact original printer-only three-run witnesses** under the original spool chronology, e.g. source line indices (zero-based header-inclusive) `(9,63,93)`, `(12,66,96)`, `(13,67,97)`, `(22,75,106)`, `(23,76,107)`, `(33,85,116)`, `(43,96,127)`. These real source controls confirm the code's MT interpretation and its ability to find multirow three-run relations without consuming disputed target material.

**Result: zero mask-involved exact two-equation witnesses in each of the four orientations, across all three possible mask roles.** A stricter initial full three-equation starts-aligned check also gave zero, but the two-equation/offset-aware null result is more informative. Standalone read-only reproducer: [`k04_mask_as_mt_witness.py`](k04_mask_as_mt_witness.py), `resources/evidence` input, original source-preserving controls.

### Meaning and stop rule

This refutes the simple specific mechanism that the four printed mask words, as an unchanged consecutive MT output run in the tested byte layouts, appear in one of these original printer two-recurrence relationships. It does **not** exclude the mask coming from an unrelated PRNG, from the same PRNG at an index without two intact printable 397/624-offset companions, or from a transformed/noncontiguous source. It cannot establish a generator epoch/order, exact missing coupon bytes, or a historical original printer reconstruction by itself.

**No K04 bit or K08 final word recovered.** This is a new source-field donor hypothesis tested against an intact-source recurrence control and rejected for the bounded observable class. Do not expand to arbitrary rearrangements unless an original source documents the transformation. Historical mask origin should be revisited only if a producer specification or independently indexed original source is identified. The unchanged REC8 predicate remains incomplete.
