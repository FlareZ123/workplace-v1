# 29 October 2026: original CLASS parity pilot

Draw=1 normal mode; Agent1 lease claimed at 2026-10-29T20:39:44.701Z, commit 45aef718b279bbbf4671086d762e7b92c12e472a. Original spool SHA256 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083.

Original observable: 128 ordinary printer rows carry CLASS and 16-byte opaque PAYLOAD. Earlier v1 Agent12 tested contiguous 2/3-bit code fields, Agent40 fixed header/trailer coding. Tested distinct proposed encoding: binary CLASS==RECOVER equals XOR of two arbitrary coupon bit positions, allowing one global inversion; if validated this could give one conditional parity equation for the selected ESC-N coupon.

Predeclared before data evaluation at /mnt/data/h17-research-20261029/k04_parity_preplan.md (sha256 a77c23007619693c4d325d4c58ccd3533b5be0d35fa89bf140738c5277359506): fit ordinary first32, predict ordinary last96 and four late intact rows only if exact training fit, 8128 pairs and two polarities, stop on zero. Selected 18:02 line excluded before payload decoding. Synthetic positive passed. Of 16,256 candidate encodings **zero** exactly fit the 32 training labels. STOP without consulting heldout or selected line/mask/hash.

Result: scoped negative for two-bit parity-only direct CLASS encoding. Actual selected coupon bits 0/128; K08 exact final words 0; six established slots unchanged; no new accepted key. No broader feature search justified absent source clue. Do not rerun as a new mechanism merely reordering bit positions.
