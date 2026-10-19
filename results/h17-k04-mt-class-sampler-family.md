# K04: exact terminal-selector family discriminator

**Agent 4, 19 October 2026, 06:02 UTC.** This is a *source-conditioned producer-model exclusion*, not a recovered coupon or K04 slot. Selected ACK row129 and the original acceptance commitments were excluded throughout. Reproducer: [`agents/agent4/k04_mt_selector_family.py`](../agents/agent4/k04_mt_selector_family.py).

## Anchored observations

Source: the original `evidence/print/spool-reconstruction.log` with SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Reuse Agent 23's source-only 42 MT recurrence witnesses and Agent 6's fixed-point reconstruction, without changing either. The 12 complete immediately pre-payload outputs and seven directly preceding complete rejection candidates are independently tabulated in [Agent 6's class-gate report](h17-k04-mt-ternary-class-consumption.md).

For these 12 ordinary rows, the *highest three tempered output bits* are exactly `0` for LABEL, `1` for STORES and `2` for RECOVER. All seven complete earlier outputs in the same contiguous pre-payload runs have top-three values `4,5,6,7`. These are observations conditional on the inferred shared MT stream/index groups; they do not authenticate the historical printer-generation implementation.

## New producer-model consequence

The standard CPython `Random._randbelow(n)` chooses `k=n.bit_length()`, repeatedly takes `getrandbits(k)`, and rejects any `r >= n`. Standard `Random.choice` delegates to `_randbelow(len(seq))`. Code references: [CPython random.py](https://github.com/python/cpython/blob/main/Lib/random.py). An ordinary `choice` over exactly three unique CLASS labels uses **two** upper output bits. In this retained sample, both LABEL and STORES give 2-bit value `0`, while RECOVER gives `1`. Hence **no deterministic mapping from that two-bit return value to all three distinct recorded labels exists**. The seven earlier reconstructed draws also cannot all be interpreted as rejected values for an ordinary three-item choice.

Under the *explicit assumption* that each one of the seven earlier full outputs belongs to the same immediately terminating rejection loop, and that the selected return value deterministically determines CLASS, exhaustive `n=2..4096` application of the documented CPython rule leaves precisely 21 integers:
`4,8,16,32,64,128,256,512,513,1024,1025,1026,1027,2048,2049,2050,2051,2052,2053,2054,4096`.
The **smallest** compatible standard sampler is `_randbelow(4)`, with observed index map `0→LABEL, 1→STORES, 2→RECOVER` and unseen index 3 unspecified. A three-class custom `getrandbits(3)` rejection loop accepting 0/1/2 and rejecting 3..7 is also compatible. For `n=8`, accepted indices partition as `{0,1}→LABEL`, `{2,3}→STORES`, `{4,5}→RECOVER` in this sample; other indices are unsampled. Larger candidate samplers show why the *three-bit trace alone* cannot prove a unique historical source implementation.

**Actionable implication:** a seed/state search that hard-codes `rng.choice(("LABEL","STORES","RECOVER"))` as the terminal pre-payload CLASS operation is inconsistent with the source-reconstructed outputs in the same-record interpretation. Use the custom three-bit threshold-3 model or an explicitly tested larger sampler/lookup model. The historical order of CLASS and DEST draws and their shared-generator identity remain unestablished.

## Target scope and limits

The experiment is source-only and prehash. The selected row129 has no recovered word, the two connected index groups around rows43/44 still have a hidden gap, and no output byte or accepted K04 component is derived by this model exclusion. The alternate possibility that this terminal draw governs another correlated field must remain open. Class/rejection observations were selected by available MT inversions, so an iid p-value would overstate the independence of the evidence. K04/K08 **MISSING**, original combined verifier **INCOMPLETE**.

**Next discriminating crack:** recover an independent producer statement (CLASS sampling width/order or four-outcome meaning), or a pre-payload output in an intact row previously unavailable to inverse closure with top-three bits equal to 3. Its semantics would distinguish a custom threshold-3 sampler from the lowest surviving standard `_randbelow(4)` interpretation. A grounded downstream producer model must predict intact held-out tail outputs before producing row129 bytes.
