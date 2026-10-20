# Source-history gate: no omitted H-17 witness in tracked Git resource revisions

**Agent 48, 20 October 2026 ~06:10 UTC.** This is an **incremental 20 October refresh** of already documented historical-file acquisition checks by Agent41/5/25 (18 Oct, `results/h17-critical-source-repository-history.md`) and Agent47 (18 Oct, `results/h17-git-source-lineage.md`). Its distinct updated scope is the new human four-file supplement plus the 20 October `START_HERE` revision; the original source-history negative is **prior art**. It is a bounded negative on Git history, **not** a recovered K04/K08 component.

## Prior art and update scope

Earlier investigators already used the GitHub path-history API to establish that original K04/K08 and route/acceptance evidence had **one initial import commit**, and that private/ had no historical tracked witness. This follow-up does not duplicate those observations as a new result. It records the specific *post-release* three-tree byte-level delta so later agents need not wonder whether the 20 October corporate files changed an old original.

## Source and method

Use the authenticated repository's read-only GitHub REST endpoints:
- `GET /repos/FlareZ123/workplace-v1/commits?path=resources&per_page=100`
- `GET /repos/FlareZ123/workplace-v1/commits?path=private&per_page=100`
- `GET /repos/FlareZ123/workplace-v1/git/trees/{ref}?recursive=1` for historical refs `5e03668c3652af8f06f6ee0871eca4ccf90ed59e` (initial human import), `ca43daaec3cdb158030464456868214cb8ac2dbc` (new corporate release) and `main` (as observed after Agent48's 06:00 UTC claim).

All three tree responses returned `truncated=false`; no GitHub repository files or histories were edited by this test. Compare *tracked file paths and Git blob SHAs*, rather than filenames or case-insensitive source-content searches.

## Exact observable differences

The `resources/` history has **four** commits: initial human import `5e03668` (17 Oct 19:29 UTC), `dc04788` cleanup (18 Oct 16:04 UTC), human corporate supplement `ca43daa` (20 Oct 02:08 UTC), and `8beda66` START_HERE scope revision (20 Oct 02:50 UTC). Original printer, crew and records-custodian source paths each have **one** tracked modification, the initial import. `private/` has only the initial import, with `.gitkeep` as its only current tracked file.

Historical tree inspection gives **43** `resources/` files at `5e03668`, **46** at `ca43daa`, and **46** at the observed `main`. Between initial and current, precisely four files were added:
- `resources/evidence/h17-supplemental-office-files/BX25-08.pdf`
- `.../print-fleet-retirement-note.txt`
- `.../retired-office-bookmarks.html`
- `.../supplier-reconciliation-L29.csv`

Exactly one resource path was removed: `resources/AGENT_PROMPT.txt`; exactly one surviving original path has a changed blob SHA: `resources/START_HERE.md` (source-scope guidance). **Every originally imported `resources/evidence/` path has the same blob SHA in the current tracked tree.** No historical tracked path named the missing `R:/Records/INDEX/IR-261003-H17.txt`, a final caption, or an additional ESC-N coupon.

## Decision and limits

The same initial-source revision negative was already established on 18 October. **The incremental observation** is that, after the 20 October human supplement, no previously imported evidence blob changed, and all new material is exactly the known four corporate files; the new `START_HERE` revision changes access scope only. The new corporate PDF was the only PDF addition; its existing released-page and object audits remain controlling. This refresh preserves the **already closed tracked resource revision archaeology**, not human paper archives, external sources, unreferenced/dangling Git objects, source text hidden within original files, or future human releases.

**Target information gained:** selected K04 coupon bits **0/128**, final K08 exact words **0**. No original acceptance checks were rerun. Do not revisit these same four resource commits absent a changed source history; pursue an independently preserved attempt-2 ESC-N witness, evidence-linked producer rule reaching the target, or verbatim Emily margin.
