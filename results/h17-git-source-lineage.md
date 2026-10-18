# Original-source revision lineage in shared Git history

**Agent 47, 18 October 2026.** A bounded provenance test of whether an earlier tracked Git revision supplies a lost K04 print payload or K08 verbatim final caption. **Result: no earlier tracked source revision for the tested paths.** The conclusion concerns this research repository's Git history and is not a claim of source completeness.

## Hypothesis and prediction

A plausible but unverified source model is that a research-side edit replaced an older original recovery source with a damaged transcription. If that happened through ordinary commits in the shared repository, the relevant file would have multiple path-history entries or be present in the immediate parent tree of its import. Those observations would be discriminating independent of any K04/K08 acceptance hash.

## Direct repository observations

On 18 October, GitHub's repository API `GET /repos/FlareZ123/workplace-v1/commits?path=<path>&per_page=100` returned **exactly one commit** for each of these four paths:

| Path | First and only path-history commit |
| --- | --- |
| `resources/evidence/print/spool-reconstruction.log` | `5e03668c3652af8f06f6ee0871eca4ccf90ed59e` |
| `resources/evidence/crew/noticeboard-and-desk-notes.txt` | same |
| `resources/evidence/recovery-routing.json` | same |
| `resources/acceptance.json` | same |

The source-introducing commit is dated 17 October 2026 at 19:29:10 UTC, message `cmt v1`. Its parent `b36cc8a8b34c9a7f3e401f2d210c697dea3b5e68` has a Git tree containing only `.gitkeep`, with **no `resources/` tree**. Thus the shared repository exposes no earlier tracked copy of any of the four files from which to restore a different coupon, mask, caption or commitment.

## Scope and consequence

The source files are an imported, derivative case corpus. This test falsifies the **specific** hypothesis that the main branch's ordinary earlier Git revisions hold a prior version of these four paths. It does not examine dangling Git objects, external repositories, case-generation tools or unavailable physical originals, and does not prove whether the imported export contains all needed historical material. In particular, a Git commit timestamp is a *repository import* time, not an incident-time custody timestamp.

The original 43-member ZIP and current `resources/` bytes were already independently reconciled in [the export equivalence audit](h17-export-equivalence.md). Together the audits rule out a straightforward recovery route through tracked research-repository versions of the existing files. The observed K04 selected payload still fails its original commitment, and the final K08 caption remains unquoted. Acceptance remains **6 PASS, K04/K08 MISSING, combined INCOMPLETE**.

This lineage check is a bounded negative provenance control, not a new component reconstruction. The outstanding priority remains a source-grounded local carrier or reconstruction mechanism for the original K04 bytes and K08 words.
