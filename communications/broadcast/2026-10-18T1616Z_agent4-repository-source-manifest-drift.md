# Agent 4: a deliberate source-tree deletion affects 43-file manifest checks

**Sender: Agent 4; 18 October 2026, 16:16 UTC.** The repository maintainer removed `resources/AGENT_PROMPT.txt` in commit `dc04788`, then the Critic reconciled the front-door README. Against the original `results/h17-source-blob-manifest.json`, a current-main recursive Git tree comparison finds **42 remaining `resources/` blobs**, all **42 exactly matching their original expected Git SHA-1**, and just one missing original path (`AGENT_PROMPT.txt`); no altered or unexpected resource blobs.

The **user-supplied original ZIP remains 43 files** with SHA256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`. This is a deliberate change to the Git research copy of an instructions file, not evidence of newly corrupted incident data, and it does not change the six-PASS/two-MISSING key status. Historical original 43/43 equivalence observations were valid when written, and this explicit dated delta is now in `results/h17-export-equivalence.md` and `results/README.md`.

**Actionable caveat:** `results/check_h17_source_manifest.py` retains an intentionally immutable 43-file original-export baseline; when run against updated default `resources/`, it should flag that one missing member. Keep both original ZIP and historical manifest unchanged. If your experiment requires complete source coverage, run it on the original 43-member ZIP extraction and distinguish the repository's current 42-file copy. Do not restore the removed instructions file against maintainer intent.

No authenticated K04 coupon or K08 final caption resulted from this Git provenance audit.
