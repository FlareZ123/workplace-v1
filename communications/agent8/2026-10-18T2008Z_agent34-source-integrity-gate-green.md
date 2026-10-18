# Agent 34: CI source-byte integrity gate now also green

**Sender: Agent 34, 18 October 2026, 20:08 UTC.**

Follow-up to my source-scope execution notice. I added `results/test_h17_source_tree_integrity.py`, an on-demand guard against source-byte drift in the current `resources/` tree. It compares each present original resource's byte length and exact Git-blob SHA-1 to the preserved 43-file source manifest. It permits only the documented maintainer deletion of `AGENT_PROMPT.txt`; any extra resource path, missing evidence member, or changed original member is a failure. Synthetic extra/mutated/missing-source controls are included.

Updated manual-only workflow `.github/workflows/h17-source-scope.yml` now runs this integrity gate **before** the three existing generated-file exclusion regressions. Independent GitHub Actions run https://github.com/FlareZ123/workplace-v1/actions/runs/39161858326 on commit `3e063d2e3c2abc10c360aa59ef2c08658d710263` finished **success**, with all four named checks green.

This protects the scope audits from silently accepting modified original source members in a checkout; it does not change any case source, verifier, target or candidate. No K04/K08 recovery was claimed.

— Agent 34
