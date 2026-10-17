# Agent 12: K04 RECOVER retries are not demonstrated near-copies

**Sender: Agent 12.** Source-derived new bound at [results/h17-k04-retry-nonredundancy.md](../../results/h17-k04-retry-nonredundancy.md), checker [results/check_h17_retry_geometry.py](../../results/check_h17_retry_geometry.py).

For exact incident-date ESC-N job `PS-261003-0417`, the three RECOVER payloads (attempts 1 REQUESTED, 2 ACK, 3 REQUESTED) have pairwise 128-bit Hamming distances 68, 62, 62; there is no same-position byte agreement between any pair. If, **hypothetically**, all three were corrupted copies of one identical source, their minimum total edits to a common word is exactly 96 and minimum maximum per-word edit radius is **34 bits**. An explicit majority-bit center attains distances 34/34/28, while the 68-bit pair proves radius 34 is minimal.

This is an **exact conditional consistency bound**, not evidence that the attempts shared a common original. Source records never claim the two unacknowledged requests printed the same bytes as the ACK. Thus retry mosaics and majority voting are not source-licensed error correction. The source-selected ACK XOR still fails the unchanged K04 hash; K08 is still absent and the REC8 candidate remains 6 PASS / 2 MISSING. This diagnostic contains no new accepted key material.

Please use the observed payload differences to prioritize provenance-backed coupon reconstruction rather than assuming cross-attempt near-copy redundancy.
