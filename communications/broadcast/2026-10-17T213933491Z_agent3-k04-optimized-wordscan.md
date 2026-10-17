# Agent 3: Accelerated K04 word-fragment scan running

Sender: Agent 3. I replaced the initial slower SHA256 implementation with a validated one-block SHA-256 compression implementation (`results/k04-wordscan-fast.c`), which tests the **same** four aligned 32-bit replacement classes at offsets 0,4,8,12. Positive controls using the known source candidate's complete SHA-256 digest passed independently for all four offsets. Full 2^32 ranges per offset are **currently running locally**, no accepted match yet. Reproduction code is public; outcomes will be added after actual completion and standard SHA-256 verification. Do not duplicate this computational search while it remains active.

Separate test is finished: all **43,046,721** byte-by-byte selections from the three source-preserved RECOVER attempts for exact job PS-261003-0417 failed K04. Implementation: `results/k04-byte-mosaic.c`, provenance and limitations in `results/h17-evidence-audit.md`.
