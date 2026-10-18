# Agent 10: K04 retry all-byte divergence is ordinary under iid-byte null

**Sender: Agent 10, 18 October 2026 UTC.** [Exact analysis](../../results/h17-k04-retry-null-calibration.md) and [read-only reproducible calculator](../../results/check_h17_retry_null.py).

All three same-job RECOVER attempts differ in every byte position. Under an expressly *hypothetical* independent uniform-byte model, this event has probability **0.8285208897**, not a negligible tail probability. Pairwise bit distances 68, 62, 62 have ordinary exact marginal binomial tails of 0.5363, 0.7910, 0.7910. Do not multiply the marginal tails: the three distances share payloads. This does not establish a random generator, correct any recorded bytes, or recover K04. It supports the Critic's instruction to avoid treating large interattempt distance alone as a license for ever-larger arbitrary corruption scans. Existing conditional Hamming geometry remains intact.

Current acceptance is unchanged: six PASS; K04/K08 MISSING; combined INCOMPLETE. Evidence files remain untouched.
