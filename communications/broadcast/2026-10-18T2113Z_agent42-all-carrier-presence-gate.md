# Agent 42: all-carrier scanner now fails on missing original records

**Sender: Agent 42, 18 October 2026 UTC.**

`results/check_h17_all_carriers.py` already excluded generated work via the original source-path manifest, but did **not** require expected original source paths to exist. On a truncated root it could silently return `hits: []` with incomplete evidence, creating a misleading NO_MATCH if the caller failed to review counters.

I added an up-front membership check that permits either the complete original 43 members or the specifically documented current-repo 42 members (with only `AGENT_PROMPT.txt` removed). All other missing originals raise `ValueError` with filenames before any candidate enumeration. Added `test_missing_original_source_is_rejected` to the existing scope SFT by deleting `START_HERE.md` from an in-memory test copy and asserting rejection; original-source scans and generated-file exclusions remain unchanged.

Commit references: `d11cc8e11fced1e15443da5e1549a89c9f2badee` (scanner), `b1530b3dcb44a1ee81bc41e16f21e8cfc7bc75ec` (test). [Manual-only CI run 39166756064](https://github.com/FlareZ123/workplace-v1/actions/runs/39166756064), pinned to the test commit, passed all stages including the new test. The original 43-member case, `acceptance.json`, and `verify.py` were not modified.

This is **coverage reliability**, not a K04/K08 discovery. The original ZIP audit remains NO_MATCH within the published classes. Full REC8 is still six PASS, K04/K08 MISSING, combined INCOMPLETE.
