# Agent 34 continuity

**Run:** 18 October 2026 UTC, normal mode (initial random draw 6). Lease first claimed 02:26:37 UTC; do not refresh it. Counter incremented from 33 to 34.

## Research state

- Original supplied ZIP and GitHub `resources/` contain the same 43 case members according to the pre-existing source equivalence audit; local re-extraction inspected `START_HERE.md`, `records-custodian.txt`, routing, 20 emails, 24 numbered crew notes, printer records, original verifier, and original acceptance JSON.
- Independently executed the original ZIP's unchanged `verify.py` on the canonical candidate: K01, K02, K03, K05, K06, K07 PASS; K04 and K08 MISSING; combined INCOMPLETE, accepted false.
- Wrote a read-only local `evidence_recheck.py` using original `archive-labels.ini` and routing rules. Exact-job last ACK RECOVER route `PS-261003-0417` attempt 2 at 18:02Z, spool line 131; payload `A9A9DC5731A5E2AE879C47215C2559D5` XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C` gives `2CFF149C50E54557228E7DE60B3EB7C9`. Its SHA-256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b` mismatches the unchanged K04 target. All 133 complete retained spool payloads XOR fixed mask also give zero K04 matches, independently confirming already published source-rule consistency.
- K08 crew notes N02/N06 are drafts, N17/N18 explicit decoys, N23 says final caption is in missing margin; neither `mail/11` nor `mail/20` quotes final exact words. Neither missing slot has authenticated original evidence in the 43 member export.
- Sampled easy hypotheses that first spool payload was SHA256/MD5/SHA1/BLAKE hash of documented route labels or early outputs from a short list of obvious Python Random seeds; none matched. These were exploratory sanity checks, not meaningful exclusions.
- Audited ZIP container metadata (no comments or extra fields) but existing `results/h17-secondary-evidence-audit.md` has a far stronger complete forensic study, so no redundant results report was published.
- Created a self-contained **local** working package at `/mnt/data/H17-archive-recovery-working-package.zip`, 48 files, with original 43 files plus candidate.json, verification.json, read-only evidence_recheck.py, recheck-result.json, and work-log.md. Test extraction passed CRC, original verify (expected return code 1, six passes), independent recheck (return 0). SHA256 package `77f45e767ccccf88d274094163b783f3d2d1d842e4a3aa0ae36ea80d46e87411`. This is a conversation artifact, not a persistent repository file.

## Priority / remaining uncertainty

The authoritative open question is source-supported recovery of the original K04 coupon and exact K08 final caption. Existing repository `results/README.md` and `results/h17-source-sufficiency-matrix.md` already summarize broad negative tests. No further exhaustive unconstrained permutation/brute-force is warranted absent a concrete provenance model. The original case rules explicitly disallow external mailbox/device contact; keep candidate null for both until each original SHA256 commitment passes unchanged. Do not treat a plausible phrase, printer ACK, or README solvability statement as authentication.

## Paths

- Primary inventory: `results/README.md`.
- Verified partial candidate: `results/h17-candidate.json` and `results/h17-verify.json`.
- Reproducible original reductions: `results/replay_h17.py`.
- K04 source contradiction: `results/h17-source-rule-consistency.md`.
- K08 source gap: `results/h17-k08-textual-coverage.md`.
- Explicit research gate: `communications/broadcast/2026-10-18T0106Z_Critic_evidence-priority-enforcement.md`.

## Incarnation 18 October 2026, 19:51 UTC (normal draw 3)

- Claimed identity with lease `d8fccae7-3b3b-41f1-8bf6-855c2d2243d1`, original claim `2026-10-18T19:51:47.158692Z`. Do not refresh this timestamp.
- Consulted latest repository front door, current `results/README.md`, 18:24 Critic direction, K04 source-layer ambiguity/cohort/chronology studies, K08 source and nonce studies, and all 20 original mail bodies. No new K04/K08 witness emerged from this independent inspection.
- Re-extracted the original 43-member user ZIP, checked the canonical six-slot `results/h17-candidate.json` against the **original unchanged** `verify.py` and `acceptance.json`. Independently observed K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false, exit code 1.
- Independently recomputed ESC-N ACK2 XOR: `A9A9DC5731A5E2AE879C47215C2559D5 XOR 8556C8CB6140A7F9A5123AC7571BEE1C = 2CFF149C50E54557228E7DE60B3EB7C9`; resulting SHA256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b` differs from original K04. This merely reproduces established result.
- Local case-text search confirms ESC-N appears only in labels/routing/mail16, its job ID only in labels and four spool lines; the mask is only in routing. K08 margin is described in N23 and final words remain unquoted. No other original-source correction mechanism was established; no new negative candidate enumeration or partial handoff package was produced.
- Preserve the public six-slot fixture, source-layer uncertainties and unchanged acceptance commitments; don't elevate descriptive chronology or a generic XOR/mutation/text-search model to source authentication. Reassess only when a local, discriminating source relation arises. No substantive public result meriting a separate `results/` entry from these checks.

### Source-scope reproducibility contribution, 20:04–20:08 UTC

- New manual-dispatch-only `.github/workflows/h17-source-scope.yml`, no per-commit triggers, runs existing 3 generated-file exclusion regressions; first run `39161628617` on commit `93c97004...` was green, each test executed and exited OK.
- Added `results/test_h17_source_tree_integrity.py` to compare all present `resources/` bytes against the existing original 43-member Git-blob manifest, permitting only the known maintainer deletion of `AGENT_PROMPT.txt`. The test includes synthetic extra-path, content mutation and missing-source controls; source files themselves stay untouched.
- Second workflow run `39161858326` on commit `3e063d2e...` was green: source fingerprint integrity plus all three source-membership regression steps PASS; 42 current repository resources remain byte-consistent with original manifest.
- Sent direct communications to Agent 8 at `communications/agent8/2026-10-18T2005Z_agent34-source-scope-ci-validation.md` and `2026-10-18T2008Z_agent34-source-integrity-gate-green.md`.
- This only improves trust in scanner source boundaries, not recovery. Do not expand it into another "missing component" report. K04/K08 still unresolved; six accepted bytes unchanged.

### Broadened verifier/selector reproducibility, 20:17 UTC

- Independently inspected pre-existing `results/test_h17_verifier_controls.py`, `results/test_h17_remaining_source_decoys.py`, and `results/test_h17_replay_decoys.py`; retained tests use synthetic in-memory commitments/source perturbations without modifying evidence. These cover original REC8 incomplete status plus genuine accepted/invalid synthetic verifier paths and selector decoy behavior for K01-K07 (including the K04 failed path).
- Extended the *same manual-only* `.github/workflows/h17-source-scope.yml` to invoke the above tests after source-tree fingerprint and source-scope checks, and renamed display to `H-17 read-only recovery regressions`.
- CI run `39162617517` on commit `1e5827bb422e82039fab4878df95d3dd6d59968f` finished **SUCCESS** at 20:17:40 UTC; all seven step checks green. URL: https://github.com/FlareZ123/workplace-v1/actions/runs/39162617517 . The expanded suite is for method integrity, not a new K04/K08 recovery.
- Independently reread the 20 original mails, full numbered crew notes, galley/stores, maintenance and spool tail; found no new original-record authenticated missing coupon/caption. Reject adding unsupported K08 caption guesses or pseudo-random printer models. Worker independent-review interface unavailable (404), so no worker result was relied upon.

- 20:20 UTC: Announced seven-step manual CI in `communications/broadcast/2026-10-18T2019Z_agent34-verified-manual-ci.md` and added one discoverability paragraph to `results/README.md` (commit `311ae8ce`) with green-run link, preserving clear boundary from K04/K08 recovery.
