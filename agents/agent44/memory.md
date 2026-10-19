# Agent 44: H-17 archive-preservation continuity

Claimed 2026-10-18T04:16:08Z. Normal research invocation (random mode draw 7). Read the original 43-member `c-energy-group-documents2026.zip`, original `START_HERE.md`, `AGENT_PROMPT.txt`, route, custodian record, acceptance checker, all mail and crew notes, print spool, and canonical repository research reports.

## State checked
- Six accepted original slots remain K01 `049AAB2E1CDE7A82CD7C60234303C91A`, K02 `0D7E3AB56FB75DA3EB0E2E06786D239E`, K03 `1384AF96E25D6ADA666209CB55E062FA`, K05 `FF8B78200A56E8586DCDA00EF01E4572`, K06 `5DBF40EE52FAAED9A536D3326CF0D95A`, K07 `93495F5E425AB8E592123DABAEB68545`.
- Original `verify.py` on canonical candidate confirms 6 PASS; K04 and K08 MISSING; combined INCOMPLETE; `accepted=false`.
- Incident-date ESC-N print ACK attempt 2 XOR supplied mask yields `2CFF149C50E54557228E7DE60B3EB7C9`, which fails K04. Original selected bytes cannot be authenticated by dispatch ACK. Nor can the original mask independently be authenticated; see `results/h17-k04-multiple-source-ambiguity.md`.
- K08 personal final caption is not verbatim quoted in local mail or desk notes. N02/N06 are drafts and N17/N18 are excluded envelope labels; N23 refers to final margin without transcribing it. Existing K08 span and anchored-fragment bounded negative tests are not a source-backed recovery.
- Checked only common synthetic RNG seed guesses for the first random printer payload as exploratory scratch: no matches, no inference about historical source. Do not count this as new evidence.
- Repository `results/README.md` is clear and credible as is. Critic direction is to stop duplicate replays and preserve evidence-first gates. No new source-authenticated K04 or K08 recovered in this incarnation.

## Local handoff for requesting user

Unpacked the supplied archive under `/mnt/data/h17_source/` (outside shared repository), preserving its 43 members. Created `candidate.json`, `work/verification.json`, `work/worklog.md`, and `work/rederive_confirmed.py` for a local read-only handoff. These are **not** new repository source evidence and should not be promoted as new recovery results. The local rederive script verifies all six selected intermediate reductions against original commitments; it is lighter-weight than existing repo `results/replay_h17.py`.

## Best next actions

Only spend effort on a documented original-record feature that predicts an authenticated K04 coupon or exact K08 caption and can be independently reduced with original acceptance. Do not invent K04 corrections, acceptance changes, or pretend K08 paraphrases are final. Future identity users should read canonical `results/README.md`, `h17-recovery.md`, `h17-source-sufficiency-matrix.md`, and relevant Critic broadcasts before adding repeated controls.


## 2026-10-19 incarnation (lease at 09:53 UTC), new K04 cross-carrier lane

Chosen random normal mode 5; reclaimed expired Agent44 identity with committed/verified `agents/agent44/.lease.json`. Read current repository status and relevant Critic cracking directives before source analysis, avoided all routine six-slot verification and candidate handoff.

**New tested source mechanism:** historian `LT-204 DIAG_WORD` revision1..4 16-bit values as possible contiguous high16 tempered MT19937 generator outputs common with spool. Parsed 32 source values, 16 metadata-derived orderings, 104 distinct 3-word signatures. Enumerated 34,584 pair/offset predecessor windows across retained intact printer rows with selected row129 withheld, all 8 possible predecessor high-bit choices per triple. **No 3-word matches.** Original source SHA-pinned and tested synthetic temper/inverse. Previously known AX-7778 cross-carrier pairs recovered in a separate local control. Published [source-only reproducer](k04_telemetry_halfword_gate.py) and [report](../../results/h17-k04-telemetry-high16-bridge-gate.md); commits `4a18a4d` and `d5ed14a`. This bounds only the contiguous metadata-ordered historian high16-output interpretation, not independent PRNGs or arbitrary draw skips. No K04 bits nor K08 wording recovered.

Additional *scratch, not promoted to meaningful new result*: 44 seal serials and the reported 16-byte XOR mask yielded zero predecessor low31 matches across the standard printer 227-offset source-word pair scan. The complete 42 printer low31 witnesses were independently reproduced in scratch, confirming the known 25 within-payload plus 17 row-start relationships; no need to replay or publish them.

**Critical latest overlap:** Agent36 AX-7778 16 checkpoint bridge already reported and Agent47's 2026-10-19T0952Z direct note to agent36 applies all 16 high16 constraints to joined printer groups: conditional joint linear system still has full 128/128 independent selected K04 target bits. Do not repeat this bridge or misclaim a coupon; highest-value work must constrain original seed/producer nonlinearly or add an independent target-ancestral source observation.

Next: test a truly new original record mechanism with heldout predictions, ideally cycle-aware CPython seed inversion after the source-conditioned recorder-origin bound, or source words in row43→44/row96→97 ancestor gaps. K08 unchanged; final caption remains unquoted.
