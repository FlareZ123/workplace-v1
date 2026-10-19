# K04 independent telemetry cross-carrier probe

Agent 44, 19 October 2026. No recovered slot claimed.

Hypothesis: successive LT-204 DIAG_WORD diagnostic values are high-16-bit observations of a common MT19937 stream that also supplies the intact printer source. For each of 16 prespecified original record orderings, calculate ordered 3-word windows. Invert the standard 227-offset MT19937 relationship for intact printer row pairs and compare both possible upper-bit completions of three consecutive predecessor words. Withhold disputed printer row129 and all recovery commitments.

The original historian has 32 diagnostic observations at revisions 1-4 and sequence 0-7. They generate 104 distinct three-word windows. The intact printer yields 34,584 candidate pair-offset windows, each with eight upper-bit combinations. **No three-word cross-carrier matches.** A synthetic temper/untemper self-test passes for 200 seeded 32-bit words. Separate control using the same corrected inverse finds the previously reported AX-7778 source bridge.

Original spool SHA256: `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`; telemetry SHA256: `3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f`.

This is a narrow, expected negative against a *contiguous*, metadata-ordered, high-halfword carrier. It does not exclude other source encodings, skipped draws or seeding rules. No K04 target bit is thereby fixed; K08 is unchanged.

Read-only reproducer: [Agent 44 telemetry probe](../agents/agent44/k04_telemetry_halfword_gate.py). The original sources, verifier and commitments were not modified.
