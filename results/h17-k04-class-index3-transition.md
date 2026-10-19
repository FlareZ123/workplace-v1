# K04 source-only row99→100: index 3 separates two sampler mechanisms

**Agent 49, 19 October 2026. Conditional model discrimination, no accepted K04 or K08 component.** Reproducer: [agents/agent49/k04_class_index3_bridge.py](../agents/agent49/k04_class_index3_bridge.py). Original printer row129 is withheld and original commitments are not consulted.

The published 42-witness fixed-point MT closure places ordinary row99 at relative position 621 of the group containing earlier intact rows15 and69. It reconstructs two consecutive **complete** generator words immediately after row99's four-word payload:

| Relative draw | Untempered state | Tempered output | Source interpretation |
| --- | --- | --- | --- |
| `s99+4` | `FA3CA1BF` | `0247F23A` | Upper two bits 0, matching original row99 `DEST=store` |
| `s99+5` | `A58E3D83` | **`6F9C95A3`** | Upper three bits **3**; original next row100 has `CLASS=LABEL` |

The published CLASS model recognizes observed accepted indices 0=LABEL, 1=STORES and 2=RECOVER. Its fourth outcome remains unknown. If the producer drew DEST after each four-word payload, CLASS before the next payload, and consumed **no unrelated generator outputs between those two selectors**, the retained row99/100 evidence is a sharp discriminator:

- Standard CPython `_randbelow(4)` calls `getrandbits(3)` and **accepts** value 3. In the strict two-sampler model, `s100-s99=6` and **index 3 must map to LABEL**. This joins two previously separate row-index groups.
- A custom `getrandbits(3)` sampler accepting only indices 0,1,2 **rejects** value 3. Under that mechanism, the post-row99 hidden word is a rejected CLASS draw and the gap is **at least seven**, requiring another output before row100. It cannot be the six-draw branch.

A read-only candidate-spacing screen over gaps 6..50, enforcing each sampler's accepted/rejected prefix and forbidding other draw consumers, gave **exactly one allowed gap, 6**, for the `_randbelow(4)` interpretation. The corresponding index3 mapping is **conditional**: source records do not authenticate the original producer code or exclude intervening unrelated draws. Joining at six yields no further whole hidden words by simple fixed-point closure and does not tighten the existing K04 selected-row range.

## Global draw-count consistency, illustrative

A separate stochastic compatibility calculation uses the previously source-constrained `s129-s0` interval **945..955** under a two-metadata-draw minimum, and additionally assumes a four-draw transition from tail row128 to selected row129. Then `s128-s0` lies in **941..951**. In a minimal 128-ordinary-row model with 128 post-payload DEST calls and 127 next-row CLASS calls, the start-distance distribution is `512 + NB(128,3/4) + NB(127,p)`, with NB denoting the **total number of draws to obtain that many accepted samples**. For standard n4, `p=1/2`; for custom three-bit threshold3, `p=3/8`. A direct exact negative-binomial convolution gives interval masses **0.2065031** and **0.00106649**, respectively. Their ratio is about **193.6**, favoring the standard n4 consumption rate *within those independent, simplified models*.

This likelihood ratio is **not** a calibrated probability of the true historical algorithm: the stream-position interval is conditioned on observed MT matches, and unknown producer draws, fourth-index semantics and tail handling remain unresolved. It is a concrete reason to prioritize n4 indexed-state experiments over equal-effort unconstrained threshold3 searches, particularly to obtain an independent spacing anchor for row99→100.

Neither model yet reconstructs the missing K04 row129 four-word payload. Original artifacts and commitments remain unchanged.
