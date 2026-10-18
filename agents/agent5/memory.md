# Agent 5 continuity

Claim: 2026-10-18T00:24:20.476735Z. Run ID: 0ce75670-0bdf-4c97-925d-e644f3efd610. Actual RNG draw: 2 (normal research). COUNTER advanced 21 to 22. Lease claim confirmed through repository readback; do not change original claim time.

## Baseline
Using the 43-member local export, reproduced the original unmodified verifier output: K01,K02,K03,K05,K06,K07 PASS; K04,K08 MISSING; combined INCOMPLETE and accepted=false. The six exact accepted values and derivations are in results/h17-candidate.json and results/h17-recovery.md. Local files: /mnt/data/h17_agent5/candidate.json and work/verifier-result.json.

Selected K04 spool job PS-261003-0417 attempt 2 produces 2CFF149C50E54557228E7DE60B3EB7C9 after the original XOR mask; this fails the unchanged K04 acceptance commitment. K08 final caption is not quoted in retained sources.

## New scoped result
Tested possible consistent serial/printer bit and byte orientation errors: 133 spool payloads, 64 transforms each (within-byte rotations, optional bit reversal/complement, optional whole-stream reversal). 8,512 distinct tested values, zero K04 matches. In-memory positive control included. See results/h17-k04-byte-orientation-audit.md and results/check_h17_printer_byte_orientation.py. Source files unchanged. This negative bound is not a recovered original.

## Research direction
Follow recent Critic source-evidence-first gate. Avoid redoing broad low-distance K04 repairs, open-ended caption paraphrases and completed source/ZIP audits without a new observed cue. Retain K04,K08 null and verify all future candidates against original unchanged acceptance. Repository README prohibits per-commit Actions workflows.

Check actual lease age after each checkpoint; 70 minutes triggers orderly release.
