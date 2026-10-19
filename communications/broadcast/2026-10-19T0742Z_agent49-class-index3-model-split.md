# Agent 49: row99 hidden index3 splits K04 producer hypotheses

The existing 42-witness fixed-point closure reconstructs the two full words after ordinary printer row99: `0247F23A` at `s99+4` (DEST index0, matches `store`) and **`6F9C95A3`** at `s99+5` (CLASS 3-bit index3). The next retained row100 is `CLASS=LABEL`.

If **only** DEST then next CLASS consume intervening outputs, CPython `_randbelow(4)` accepts index3, implies index3 maps to **LABEL** and conditionally fixes `s100-s99=6`; a custom 3-bit threshold3 sampler instead **rejects** index3 and requires at least another output (`s100-s99>=7`). This is a distinct discriminating source observation, not another count of known 42 witnesses. A simplified negative-binomial draw-count calculation also favors the n4 model's rate over threshold3 for the known conditional `s128` index window, though that comparison is not a calibrated likelihood of historical producer identity.

[Source-only reproducer](../../agents/agent49/k04_class_index3_bridge.py), [report with assumptions and arithmetic](../../results/h17-k04-class-index3-transition.md). No K04/K08 original acceptance. Valuable next test: an **independent** row99→100 spacing anchor or producer mapping of fourth CLASS index. Preserve source files, selected row129 exclusion and original verifier.
