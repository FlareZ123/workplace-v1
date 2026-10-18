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
