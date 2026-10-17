# Agent 9: H-17 REC8 reconstruction continuity

Identity claimed: 2026-10-17T22:02:15Z, run_id `h17-agent9-20261017T220215Z`. Required actual RNG result **7** selected normal mode. Incremented shared COUNTER from 9 to 10 before identity claim; lease was created and confirmed via GitHub fetch. Do not update the original lease timestamp. Retain identity until actual clock minus claimed_at reaches 70 minutes at a checkpoint; at that time follow final-state push then lease release rules.

## Confirmed case status

Uploaded 43-member ZIP extracted locally into `/mnt/data/h17-agent9`. Original case `verify.py --candidate candidate.json --json` reports K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, passed 6, combined INCOMPLETE, accepted false; nonzero verifier process exit is expected for incomplete candidates. Recovered known accepted source-derived six values in `results/h17-candidate.json`, script `results/replay_h17.py`, reports `results/h17-recovery.md` and `results/h17-evidence-audit.md`.

K04 incident-date ESC-N maps to PS-261003-0417, last acknowledged RECOVER is attempt 2, payload A9A9DC5731A5E2AE879C47215C2559D5. XOR with 8556C8CB6140A7F9A5123AC7571BEE1C produces baseline 2CFF149C50E54557228E7DE60B3EB7C9 (fails original target). K08 final caption verbatim absent from drafts, crew note N23 and mail 11/20 descriptions; other agents checked explicit labels. Unacknowledged spool payloads and paraphrases cannot be silently promoted.

## New independently tested bounded K04 class

I tested a retained-bitstream-boundary alignment hypothesis: all left/right bit slips by k=1..23 bits with all k-bit boundary replacements, XOR against original mask and SHA256 compared with unchanged target. Counts: k1..20=4,194,300; k21=4,194,304; k22=8,388,608; k23=16,777,216; total 33,554,428 candidates. Each range returned NO_MATCH. A positive synthetic witness validated enumeration at k3. Note byte-aligned k8/k16 overlap earlier byte slips. This excludes only a precise bit-boundary class, not arbitrary corruption or missing primary evidence.

Committed read-only source-derived Python checker `results/check_h17_bit_slips.py`, scope and reproducibility `results/h17-k04-bit-boundary-slip.md`, linked from `results/README.md` and broadcast `communications/broadcast/2026-10-17T221104Z_agent9-K04-bit-slip.md`. Source code locally tested from original ZIP as `/mnt/data/h17-agent9/work/check_h17_bit_slips.py`, SHA256 35d89a4cda7e3e840bc5ac47fa7d085ef6441ce30cdde4fcf5d3bdcf56821fab. The read-only checker accepts extracted case path, max bit shift and optional min bit shift, and limits each run to at most 23 bits; tested chunks 1-20, 21, 22, 23.

## Next best work

Seek only independently authenticated ESC-N coupon/printer media/buffer and exact original keeper caption/quotation from preservation sources; local export explicitly warns it is trimmed. Re-run original slot checks then combined only after receiving such evidence. Avoid duplicating agent 3/4 expensive word, bitflip and byte-mosaic negative searches or 70M+ failed generic phrase splices. Preserve original resources and commitments unchanged. No per-commit GitHub Actions workflows.
