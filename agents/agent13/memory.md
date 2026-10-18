# Agent 13 continuity: H-17 archive recovery

**Claimed:** 2026-10-17 23:31:45 UTC. **Mode:** normal research. Source of truth: supplied 43-member export and repository resources, unchanged acceptance commitments.

## Work verified this incarnation

- Reproduced the six confirmed slot values and original offline verifier outcome: K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false. Local package generated: `h17-recovery-submission.zip` (conversation output) with candidate, verifier result, notes and retry diagnostic.
- Independently examined `resources/evidence/print/spool-reconstruction.log` (SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`). For exact incident ESC-N job PS-261003-0417, three RECOVER attempts all disagree at each of 16 corresponding positions. Distances: attempts 1:2 = 68 bits, 1:3 = 62 bits, 2:3 = 62 bits. All 16 byte positions differ pairwise, no unanimous positions.
- Deeper bit-level audit: only 32/128 bits unanimously agree. Pairwise distances (68,62,62) imply every hypothetical common source must differ by at least 34 bits from some attempt (triangle inequality), and a per-bit-majority center exhibits radius exactly 34 with distances (34,34,28). Its masked K04 component `48EB95BE4897014320CA39E60D2A13F8` is NO_MATCH. Conditional bound only: there is no evidence attempts are identical coupon content. Report and script updated with this proof.\n- Selected ACK attempt 2 remains `A9A9DC5731A5E2AE879C47215C2559D5`. With fixed XOR mask, written-rule K04 is `2CFF149C50E54557228E7DE60B3EB7C9`, SHA-256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`, which fails original target.
- Reproducer: `results/check_h17_retry_divergence.py`. Detailed scoped report: `results/h17-k04-retry-divergence.md`. Linked in `results/README.md`; broadcast `communications/broadcast/2026-10-17T2340Z_agent13-esc-n-retry-provenance.md`.
- Confirmed that `private/` currently contains only `.gitkeep`, agreeing with Agent 10 prior scope audit.
- Incremented repo `COUNTER` from 15 to 16 as required, then claimed agent13 by pushed lease.

## Limits and highest-value next investigation

- The new disagreement result **does not** prove corrupted bytes or rule out different coupon content per retry; it closes the assumption that retained retries reproduce stable position-wise bytes. Do not turn its statistics into conjectural source correction.
- Original final K08 desk caption remains not authentically quoted. Existing extensive corpus, span and grammar checks found no accepted phrase. No credible new source or hash inversion route identified by this incarnation.
- Strong baseline docs: `results/README.md`, `results/h17-source-rule-consistency.md`, `results/h17-evidence-audit.md`, `results/h17-k08-textual-coverage.md`. Critic broadcast `communications/broadcast/2026-10-17T224013Z_Critic_sufficiency-falsification.md` emphasizes sourcing a genuinely new carrier or source-grounded mechanism before more computational guesses.
- Seek independent integrity witness for K04 original printer coupon and an authenticated verbatim K08 final caption among genuinely permitted local carriers. Case prohibits contacting external systems or people; do not propose those as executable within current export.
- Keep candidate K04 and K08 null unless original slot commitment passes with defensible provenance. No complete key yet.

## Incarnation 18 October 2026, 15:28 UTC onward

Actual cryptographic mode draw 8, normal mode. Invocation counter 98->99 (commit abd6e57d); claimed Agent 13 at 2026-10-18T15:28:33.947409Z, run agent13-f1d7fa69-1ee8-4efe-a18c-4fcc2281a43f, claim commit cf921107. Do not refresh lease time; mandatory elapsed check after persistence checkpoints.

Re-read original local 43-member ZIP, source constraints, custodian, route, email/crew notes, relevant spool and source sufficiency audits. Independently authored a read-only ZIP-native Python reducer for user handoff. Fresh reduction and the *unchanged original* bundled verify.py reproduce K01 K02 K03 K05 K06 K07 PASS, K04 and K08 MISSING, combined INCOMPLETE, accepted false. Source-selected ESC-N ACK2 diagnostic component 2CFF149C50E54557228E7DE60B3EB7C9 still fails original K04 hash, with ambiguities across source mask, job mapping, reconstructed payload; K08 final caption not authentically quoted. No new authenticated source or accepted component found.

Created and extracted/validated invocation-local handoff /mnt/data/H17_recovery_handoff.zip (not persistent across future invocations), containing unchanged original ZIP, acceptance/checker, replay, six-slot candidate, audit, provenance notes, nine-member digest manifest. All manifest hashes, original source equality, repeat reducer output and original verifier result passed extraction test. It is a user deliverable, not a new research result; intentionally did not add duplicate shared public finding. Central results/README.md already appropriately summarizes six-of-eight, contradiction, source-layer uncertainty and existing bounded negatives. Investigated remaining maintenance/procedure/recorder metadata for missing carriers; no new direct witness identified. Future work requires source-authenticating local evidence or deterministic provenance mechanism, not more free-form phrase guessing.
