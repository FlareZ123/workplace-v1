# Agent 46: H-17 preservation-recovery investigation

Run claimed `2026-10-18T04:26:10.559Z`. Normal mode (random draw 3). Read the original `README.md`, Critic evidence-first and redundancy interventions, `results/README.md`, major K04/K08 sufficiency reports, and the supplied identical 43-member ZIP.

## Status and direct verification

No new K04 or K08 original value was recovered. The frozen six-component `results/h17-candidate.json` was run against the supplied unmodified `verify.py` and `acceptance.json` after extracting the original ZIP locally. Result: `K01/K02/K03/K05/K06/K07 PASS`, `K04/K08 MISSING`, `combined INCOMPLETE`, `accepted=false`, checker exit 1. The selected 18:02Z K04 spool ACK XOR the transcribed mask is a known SHA mismatch, and the final K08 margin phrase remains unquoted.

Local user handoff built under `/mnt/data/h17-candidate.json`, `/mnt/data/h17-verification.json`, and `/mnt/data/h17-derivation.md`. Those paths are local invocation artifacts, **not** repository resources and need not persist across invocations.

## Supplemental ZIP metadata test (minor bounded negative observation)

Parsed all 43 ZIP local-file headers and compared each to its central-directory entry: no mismatches in filename bytes, minimum extraction version, general flags, compression method, DOS date/time, CRC32, compressed/uncompressed sizes, or extra fields. All 43 entries have identical ZIP modification timestamp `(2026,10,4,11,40,0)`, creator OS `0`, flags `0`, create/extract version `20`, internal attribute `0`, external attribute `25165824`; filenames are lexicographically sorted. This is a bounded metadata consistency observation beyond the prior published ZIP audit's no-comments/no-extra/padding findings. It does **not** recover hidden source data or establish complete absence of steganography. Avoid promoting it as substantive key progress or adding another index item solely for this negative test.

## Research direction

The preserved local export lacks an independently authenticated ESC-N original payload or mask correction, and lacks Emily's verbatim final keeper caption. The existing local search bounds and source-layer ambiguity have been well studied. Prioritize an original-source anchor and independently discriminating mechanism before any more candidate-grammar/bitflip explorations. Preserve six accepted slots unchanged. Avoid repetitive replays/workpack production absent changed inputs.

Relevant shared references: `results/h17-k04-multiple-source-ambiguity.md`, `results/h17-k08-textual-coverage.md`, `results/h17-source-sufficiency-matrix.md`, `results/h17-secondary-evidence-audit.md`, and `communications/broadcast/2026-10-18T0129Z_Critic_stop-duplicate-replay.md`.


## 19 October 2026 new incarnation: calibrated K04 long-seed algebra and shifted-origin pivot

**Claim:** executed cryptographic random mode draw 6 (normal); reclaimed Agent46 through remote lease commit `fdac69812a25cb46807bfddf00deb3a3656d2504` using immutable original claim time `2026-10-19T06:52:05.953265Z`. No lease refresh; stop/release only at measured 70 minutes. Original source selected printer row129, K04 mask and all REC8 commitments consistently withheld from discovery.

**Novel constructive results** preserved in top-level `results/`:
- `h17-k04-sixth-window-352bit-seed-inversion.md`, script `agents/agent46/k04_seed_six_window.py`: Agent4 source-control joins supply four additional 227-apart complete MT output pairs in row28/59/80/111 group, yielding one additional initialized-state key word. True synthetic 352-bit `random.Random` numeric seed recovered exactly; 63,916 full source phase assignments all rejected by intact heldout row34 final output.
- `h17-k04-seventh-window-384bit-seed-inversion.md`, script `agents/agent46/k04_seed_seven_window.py`: extra two-initial-state-word boundary from CRC-good TRP2-anchored row7/38/91/121 group enables *third* `init_by_array` inverse seed-word bridge. True synthetic 384-bit integer seed recovered exactly; original data yields 65,444 conditional phase assignments with 11/12 words but no complete assignment satisfying third bridge. This is **not** a general seed-class exclusion.
- `agents/agent46/k04_cross_carrier_seed_windows.py`: original 42 spool witnesses reconstruct 30 complete 227-pair runs of length >=2. After three source-backed TRP2/RC17 group bridges, 35 runs, including new row7/38 pair windows at group-relative 1 len3, 397 len3, 624 len4; row9/40 relative2 len2; row28/59 relative-1 len4 and 623 len3.
- Manual-only workflow `.github/workflows/h17-k04-extended-seed.yml`; verified runs 39213550554 (n11/n12 two-stage undercoverage), 39213740700 (pair windows), 39214281409 (352-bit synthetic PASS, source negative), 39215008099 (384-bit synthetic PASS, source no completed assignments). Added results to `results/README.md`, and sent Agent8 two messages `communications/agent8/2026-10-19T0706Z_agent46-new-windows-seed-bridge.md` and `...0707Z_agent46-new-227-pair-runs.md`.

**Critical new confounder:** Agent48 `results/h17-k04-shifted-seed-prefix-constraint.md` uses independent recorder 28 and spool witnesses to derive `s0>=292, s10>=396, s13>=420` if the recorder and spool share one chronological MT stream. Under that premise row13's 5-pair group CANNOT lie in first MT output cycle, so my six/seven-window original-source first-cycle negative families represent narrower printer-first-cycle counterfactuals. Synthetic algorithms remain generally valid and new window discovery remains constructive. Explicit caveat appended to both reports. Messaged Agent48 at `communications/agent48/2026-10-19T0721Z_agent46-shifted-origin-followup.md`.

**Cycle-aware pivot:** only row3 five 227-pairs may remain inside first output cycle, from an unknown pre-spool RNG prefix; it directly supplies just 2 of 3 words for a 96-bit numeric seed, not 3 (corrected `agents/agent46/k04_shifted_seed_96bit.py`; synthetic fragment calibration PASS, source 393 two-word assignments, 1 word underdetermined). Agent48 already excluded 32/64bit seeds over all 393 phases; do not repeat those. A new `agents/agent46/k04_shifted_seed_smt.py` uses Z3 32-bit exact bitvectors across the original row3 four-initial-word window and TRP2-bridged row7 two-word window, trying to solve repeated missing 96-bit seed word. GitHub Actions run 39216033528 completed; synthetic positive itself timed out after20s and 29 bounded original source phase pairs timed out at1.8s each, **zero SAT or UNSAT**. This is currently a computation failure, with no exclusion whatsoever. Do not rerun the same Z3 model naively. Official Z3 documentation consulted for `BitVec,LShR,Solver.set(timeout)`.

**Current promising immediate follow-up:** `agents/agent46/k04_seed_pair_deficits.py` reveals 32-bit masks around cross-source group7 and group28 227-pair runs to identify whether one absent pair can be completed with authentic existing source bits, giving a direct third key fragment and avoiding nonlinear Z3. It has been added before SMT in the latest manual workflow dispatch run 39216297301; retrieve its paired `PAIR` lines via `mcp__GitHub_Actions_MCP__get_job_logs` after run completes. Avoid unnecessary broad negative scans, duplicate six-slot package and source/commitment edits. K04/K08 still missing.

