# Agent 10 continuity

Claimed at 2026-10-17T22:19:46Z; normal-mode run, initial RNG=7. Keep this original lease timestamp unchanged. Repository README prohibits per-commit CI.

Current REC8 result: K01,K02,K03,K05,K06,K07 individually PASS the original acceptance SHA-256. K04 and K08 are unresolved (null); offline combined INCOMPLETE, accepted=false. I independently replayed the source reduction and original verifier against the separate 43-file uploaded ZIP in local Python. The repository baseline candidate and results/README.md agree.

K04: last ACK RECOVER attempt 2 of incident-date ESC-N job PS-261003-0417 yields XOR output 2CFF149C50E54557228E7DE60B3EB7C9, which fails the untouched K04 commitment. Explicit custodian warning: reconstructed spool bytes lack independent integrity verification. K08: the authenticated final keeper caption is not quoted in preserved drafts/notes; HMAC/SHA tests guesses only.

Contributions: results/check_h17_k04_word_reassembly.py and results/h17-k04-word-reassembly-bound.md test 331,776 cross-attempt 32-bit fragment recombinations (with per-word reversal), all NO_MATCH. This is complementary to Agent 9's within-ACK variable-fragment permutations. A message was sent to communications/agent9/2026-10-17T222751Z_agent10-fragment-study.md.

Provenance observation: mail/13.eml dated 2 Oct 09:56 UTC retrospectively labels AX-7782 final even though transfer-audit COMMIT is dated 3 Oct 20:55:10 UTC. Mail/16 dated 3 Oct 07:49 anticipates print attempts at 18:02 and 18:03 UTC. These are unresolved chronology inconsistencies and do not invalidate accepted K07 bytes or explain K04 hash mismatch.

Critic response: I inspected permitted repository private/ on current main. It contains only a 1-byte .gitkeep and no case evidence. The local workspace initially held only prompt.md plus the same 43-member ZIP. I broadcast this narrow finding at communications/broadcast/2026-10-17T224430Z_agent10-private-scope.md. Do not conflate 43-member ZIP sufficiency with every possible source, but this particular private branch is closed.

Local workpack `/mnt/data/h17-recovery-workpack.zip` includes candidate, verifier result, independent read-only source-to-slot program, bounded K04 test and chronology report. It was re-extracted alongside original source and replayed successfully. This is a per-invocation local path, not a stable repository path.

Priority next: source provenance and meaningful alternate local carriers, not unrestricted hash sweeps. Preserve input evidence. Before each checkpoint use the runtime clock to compare elapsed time with the lease claimed_at. At 70 minutes release only after all useful commits are pushed; lease deletion must be the final repository mutation.

## Incarnation 18 Oct 2026, 00:15:13.140 UTC

Mode draw 5 (normal). Successfully reclaimed eligible Agent 10, incremented COUNTER 20→21. Original lease timestamp for this incarnation is 2026-10-18T00:15:13.140Z. Read previously retained scope results and Critic's actionable-research gate. No additional authenticated original K04 or K08 source surfaced; same six slot components independently pass original verifier from the uploaded 43-file ZIP. Local user deliverable `/mnt/data/h17-recovery-partial.zip` has candidate, unchanged verify.py + acceptance.json, verifier JSON and derivation note; this is invocation-local, not a stable repo artifact.

New narrow contribution: `results/check_h17_retry_null.py`, `results/h17-k04-retry-null-calibration.md`, and `communications/broadcast/2026-10-18T0027Z_agent10-retry-null-calibration.md`. Under an expressly hypothetical iid-uniform-byte null, three 16-byte retries being bytewise distinct at every position occurs with probability 0.828520889732. Pairwise Hamming distances 68,62,62 have ordinary exact binomial marginal tail probabilities 0.53626871,0.79100745,0.79100745. This does not prove randomness or integrity; it shows why their divergence alone is not a basis for arbitrary high-radius correction search. The unchanged K04 ACK selection still fails its commitment.

Local exploratory CPython `random.Random` seed and straightforward output-form fingerprint probes found no reproducible match for selected case payloads in small explicit seed sets or seeds 0..99,999 for first `randbytes(16)` output. Negative scope is too weak for a substantive public claim. Agent 15 independently found 128 regular (+00:00) and five special (Z) spool serialization cohorts, making naive common-generator speculation particularly unsafe.

Continue looking for a genuinely source-grounded local transformation or authenticated carrier, prioritize evidence-rich causality over generic SHA256 preimage speculation; retain K04/K08 null until exact commitments match. Check mailbox/broadcast when productive. At each checkpoint measure age from the lease before selecting continuation or release.

## Subsequent checkpoint: cross-slot control and standalone replay

Added `results/h17-chronology-cross-slot-control.md` and broadcast `communications/broadcast/2026-10-18T0040Z_agent10-chronology-control.md`. It uses accepted K07 as a chronology interpretation control: mail/13 is 34h59m10s before AX-7782 COMMIT while K07 passes, and mail/16 is 10h13/14m before associated print events while K04 fails. The anomaly is not unique to K04, so it cannot by itself justify substituting another printer route or ACK. Existing source-rule consistency had independently documented the timing mismatches; this contribution is the explicit cross-slot positive/negative control.

Refined user-local `/mnt/data/h17-recovery-partial.zip` to include original byte-identical 43-member export, source-by-source no-write `replay_from_zip.py`, its audit JSON, unchanged acceptance+verifier, canonical six-slot candidate and derivation notes. Verified replay reconstructs all six from original sources, K04 hash rejects, K08 null, verifier accepted=false. The replay parses K03 signed bay order and K07 final receipt from relevant mail rather than merely hard-coding those values. Local artifact path is per invocation only.

Noted that the source-sufficiency matrix already published the 0.8285208897 all-byte divergence iid-null probability before my independent reproducibility note. Updated `results/h17-k04-retry-null-calibration.md` to acknowledge prior attribution, leaving exact marginal binomial-tail values as the small extension. Initial attempt to write a long chronology result was blocked by a tool safety check; a shorter evidence-grounded version succeeded, no persistent fault or data loss.
