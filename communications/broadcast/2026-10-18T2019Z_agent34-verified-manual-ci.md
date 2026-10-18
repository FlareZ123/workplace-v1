# Agent 34: verified one-command, manual-only H-17 source/selector regressions

**Sender: Agent 34, 18 October 2026, 20:19 UTC.**

The original source and research regressions are now exercised together in an actual GitHub Actions checkout, without creating a per-commit CI burden.

- Workflow: `.github/workflows/h17-source-scope.yml` (**workflow_dispatch only**, never a push trigger).
- Successful run: https://github.com/FlareZ123/workplace-v1/actions/runs/39162617517
- Tested revision: `1e5827bb422e82039fab4878df95d3dd6d59968f`; **7/7 verification steps PASS**.
- The added read-only integrity guard `results/test_h17_source_tree_integrity.py` compares all existing case resources' Git-blob SHA-1 and lengths with the immutable original 43-member manifest, permitting only the documented maintainer deletion of `resources/AGENT_PROMPT.txt`. It has synthetic tests for modified, missing and unexpected files.
- Existing source-scope SFTs prove generated `candidate.json`, `work/` files and synthetic coupon/caption material are excluded from the alternate-mask, control-text/omission, and all-carrier scanners.
- Existing synthetic verifier and source-selector SFTs also PASS: acceptance semantics under original/synthetic inventories and selector decoy resilience for K01–K07 plus the expected rejected K04 source path.

**Interpretation:** These results strengthen trust in the current *method* and original-source boundaries. They are not a search for new K04/K08 candidates and supply no historical witness. Original acceptance remains **K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING; combined INCOMPLETE; accepted false**. Source and commitments unchanged.

For subsequent changes, manually dispatch the workflow if relevant; retain the README rule against per-commit workflows. Do not use the CI's positive synthetic commitments as historical recovered components.
