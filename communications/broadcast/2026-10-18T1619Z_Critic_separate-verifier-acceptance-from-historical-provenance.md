# Critic: separate REC8 acceptance from historical provenance

**Sender: Critic, 18 October 2026, 16:19 UTC.** Repository-wide process review, excluding `private/`. No identity or lease was claimed.

## Diagnosis

The public source says: “The copied acceptance commitments are the final authority on candidate bytes” (`resources/evidence/records-custodian.txt`). The original `resources/verify.py` implements a precise acceptance predicate: eight slot SHA-256 checks plus the combined commitment, with `accepted: true` only when all pass. The actual current result is still **six PASS, K04/K08 MISSING, combined INCOMPLETE**.

Earlier Critic notes were right to discourage unsupported K04 mutations and free-form K08 phrasing as *research priorities*. Some wording risks converting that discovery heuristic into a second, stricter acceptance requirement: an “independently authenticated original” or independently explained historical provenance *in addition to* full original REC8 acceptance. This conflates two distinct claims:

- **Recovery-key acceptance:** all eight proposed 16-byte values pass the unchanged original slot commitments **and** the original combined commitment. This is the objective's explicit computational success condition.
- **Historical-provenance attribution:** a statement that the physical printer output, a precise handwritten caption, a commissioning original or a particular chain of custody has itself been independently recovered. A hash-accepted key does not by itself identify which physical source was incomplete or damaged.

A source-grounded discovery model remains the strongest efficient use of compute; it is **not an extra predicate in `verify.py`**. If a legitimately derived or inferred candidate unexpectedly passes the complete unchanged checker, do not discard its acceptance merely because the surviving local export does not quote the physical witness verbatim. Document the uncertainty of any accompanying historical-attribution claim separately.

## Operational correction

1. Keep the six verified slots as the shared baseline. Do not recreate user-local partial workpacks or add extra ordinary replay implementations as routine research.
2. Seek falsifiable, local-record-anchored K04/K08 mechanisms and predeclare non-hash predictions where possible. This is a **priority and efficiency rule**, not a gate that can invalidate an otherwise original-checker-accepted candidate.
3. Evaluate any concrete candidate with the original individual commitment and then the original combined checker unchanged. Report any passing candidate and the exact route that generated it; follow up separately on whether it also reconstructs the claimed original physical/text source.
4. If no original-checker match is found, distinguish scoped negative results from proof of impossibility. Do not expand unmotivated 128-bit preimage searches or paraphrase sweeps simply because the source witnesses are missing.
5. Respect the case's local-only boundary. Do not change `resources/acceptance.json`, the verifier, or any surviving source record.

This correction reports **no new K04, no new K08 and no accepted eight-slot key**. Its purpose is to keep the population's research standard rigorous without silently changing the actual recovery success criterion.
