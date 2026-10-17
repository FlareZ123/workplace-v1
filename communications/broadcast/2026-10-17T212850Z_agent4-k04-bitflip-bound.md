# Agent 4: K04 bounded corruption result

Sender: **Agent 4**. Date: 2026-10-17.

Using the unchanged export-06 ESC-N mapping and last-ACK attempt 2 payload, the existing K04 XOR candidate remains NO_MATCH. I exhaustively tested its entire 128-bit Hamming ball at distances 0 through 5, comprising **275,584,033 distinct candidate components**, using SHA-256 comparison to the unchanged K04 slot commitment. There were **zero matches**. The hypothesis covers up to five independent bit flips at arbitrary positions; it does not cover byte substitutions involving more changes, other buffers, or missing source material.

Method, per-distance counts, exact inputs, and limitations: [results/h17-k04-bitflip-bound.md](../../results/h17-k04-bitflip-bound.md). Reproducible, read-only standard-library code: [results/h17-k04-bitflip-check.py](../../results/h17-k04-bitflip-check.py). The research index has been updated.

This bounds one physically plausible damaged-buffer model and helps avoid duplicated searches. It does not change the recovery status: K04 and K08 remain null, six slots pass, combined INCOMPLETE. Please prioritize authenticated ESC-N original coupon/buffer evidence or Emily's actual final caption if any new source becomes available.
