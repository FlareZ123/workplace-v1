# H-17 archive recovery: research status

**REC8/1 incident-preservation envelope:** 6 of 8 components pass their individual SHA-256 acceptance commitments. The six values in [the public candidate](h17-candidate.json) (K01, K02, K03, K05, K06, K07) were independently rehashed against the supplied `resources/acceptance.json` on 17 October 2026 and matched. [The recorded verifier output](h17-verify.json) reports `accepted: false`. The combined recovery key remains unverified.

[Evidence selection, byte reductions, unresolved cases, and limits](h17-recovery.md) describe the current work. K04's routed last-ACK spool XOR candidate fails its acceptance commitment, and the source does not certify the copied payload's integrity. K08 lacks an authenticated exact final keeper caption. Neither missing component should be substituted with an unverified guess.

**Reproducibility gap:** the repository preserves the candidate, verifier report, and textual derivations, but currently lacks the executable source-to-candidate derivation script described in Agent 2's memory. Future researchers should commit that script or a reproducible equivalent before treating costly negative searches as independently repeatable.

**Research priority:** establish stronger evidence for K04 and K08 or carefully document the local export's insufficiency. Preserve the original evidence and acceptance hashes. The [Critic review](../communications/broadcast/2026-10-17T204358Z_Critic_evidence-provenance.md) records process concerns and suggested next steps.
