# Agent 10 continuity

Claimed at 2026-10-17T22:19:46Z; normal-mode run, initial RNG=7. Keep this original lease timestamp unchanged. Repository README prohibits per-commit CI.

Current REC8 result: K01,K02,K03,K05,K06,K07 individually PASS the original acceptance SHA-256. K04 and K08 are unresolved (null); offline combined INCOMPLETE, accepted=false. I independently replayed the source reduction and original verifier against the separate 43-file uploaded ZIP in local Python. The repository baseline candidate and results/README.md agree.

K04: last ACK RECOVER attempt 2 of incident-date ESC-N job PS-261003-0417 yields XOR output 2CFF149C50E54557228E7DE60B3EB7C9, which fails the untouched K04 commitment. Explicit custodian warning: reconstructed spool bytes lack independent integrity verification. K08: the authenticated final keeper caption is not quoted in preserved drafts/notes; HMAC/SHA tests guesses only.

Contributions: results/check_h17_k04_word_reassembly.py and results/h17-k04-word-reassembly-bound.md test 331,776 cross-attempt 32-bit fragment recombinations (with per-word reversal), all NO_MATCH. This is complementary to Agent 9's within-ACK variable-fragment permutations. A message was sent to communications/agent9/2026-10-17T222751Z_agent10-fragment-study.md.

Provenance observation: mail/13.eml dated 2 Oct 09:56 UTC retrospectively labels AX-7782 final even though transfer-audit COMMIT is dated 3 Oct 20:55:10 UTC. Mail/16 dated 3 Oct 07:49 anticipates print attempts at 18:02 and 18:03 UTC. These are unresolved chronology inconsistencies and do not invalidate accepted K07 bytes or explain K04 hash mismatch.

Critic response: I inspected permitted repository private/ on current main. It contains only a 1-byte .gitkeep and no case evidence. The local workspace initially held only prompt.md plus the same 43-member ZIP. I broadcast this narrow finding at communications/broadcast/2026-10-17T224430Z_agent10-private-scope.md. Do not conflate 43-member ZIP sufficiency with every possible source, but this particular private branch is closed.

Local workpack `/mnt/data/h17-recovery-workpack.zip` includes candidate, verifier result, independent read-only source-to-slot program, bounded K04 test and chronology report. It was re-extracted alongside original source and replayed successfully. This is a per-invocation local path, not a stable repository path.

Priority next: source provenance and meaningful alternate local carriers, not unrestricted hash sweeps. Preserve input evidence. Before each checkpoint use the runtime clock to compare elapsed time with the lease claimed_at. At 70 minutes release only after all useful commits are pushed; lease deletion must be the final repository mutation.
