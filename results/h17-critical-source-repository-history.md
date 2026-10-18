# H-17 critical-source repository-history boundary

**Agent 41, 18 October 2026 UTC.** This is a repository provenance check, not a new recovered K04/K08 component.

## Observed source and question

The original case export contains `resources/evidence/recovery-routing.json` (K04 mask, K08 nonce), `resources/evidence/archive-labels.ini` (printer routing), `resources/evidence/print/spool-reconstruction.log` (K04 retained payload), `resources/evidence/crew/noticeboard-and-desk-notes.txt` (K08 drafts), `resources/evidence/mail/16.eml`, `resources/evidence/mail/20.eml`, `resources/acceptance.json` and `resources/verify.py`.

Given the independent finding that K04/K08 are unresolved, I tested the specific hypothesis that a **previous tracked version** of one of those files in the shared workplace repository might contain a differently copied parameter or omitted final phrase.

## Method and result

Using the connected repository API on `FlareZ123/workplace-v1` (default branch `main`), I queried the `commits?path=...` history for each of the eight identified files and for the enclosing `resources/` directory, with a page size of 100. I also listed the repository branches.

**Observed:** every path, and `resources/` as a whole, returns only the initial tracked commit `5e03668c3652af8f06f6ee0871eca4ccf90ed59e` dated `2026-10-17T19:29:10Z` (`cmt v1`). The branch listing returns only `main`. No subsequent tracked modification to `resources/` is visible in the reachable branch history as queried.

## Interpretation and limits

The ordinary **current repository file history** offers no prior revision of the route transcription, recovered spool, desk notes, or acceptance checker to compare as a missing-evidence witness. This narrows one repository-based source-history hypothesis only. It does **not** prove that the historical appliance, printer, mailboxes, or original paper contained no earlier or independent copies. It does not certify the retained printer ACK bytes or the exact final caption. Git object history outside reachable refs and external historical records were not searched, and there is no authorization to contact external systems for original case material.

The original-source analysis and ZIP byte-equivalence reports remain in `results/h17-recovery.md`, `results/h17-export-equivalence.md`, and `results/h17-secondary-evidence-audit.md`. The unchanged outcome is six original slot commitments PASS, K04 and K08 MISSING, combined INCOMPLETE, accepted false.

**Actionable implication:** do not spend more research effort hunting a prior `main` revision of these resources unless repository history or a new local source actually changes. Focus on source-supported local evidence for the two missing originals.
