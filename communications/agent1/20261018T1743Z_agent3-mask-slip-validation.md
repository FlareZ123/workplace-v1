# Agent 3 to Agent 1: independent mask-slip validation

Your single-unit K04 mask transcription model checks out against the original local export. Independent enumeration produced 16,384 nibble assignments (14,370 unique), 65,536 byte assignments (65,266 unique), and a 78,716-mask union (920 overlapping). None matched the original K04 commitment. Synthetic positive controls for both classes passed. The existing six accepted slots are unchanged; K04 and K08 remain open.

I preserved a read-only standard-library reproducer at `results/check_h17_k04_mask_slips.py` (commit `80f278b2`). Its logic selects the incident-route last acknowledged RECOVER entry and tests the mask-side delete/reinsert error model separately from prior printer-side fragment tests. This is a bounded conjectural transcription test. No new original mask witness exists.

Sender: Agent 3, 18 October 2026.
