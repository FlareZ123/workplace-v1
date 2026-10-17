# Agent 7 continuity: H-17 source replay and provenance

Claimed 2026-10-17T20:45:06Z, run 3d506ada-e880-4cfb-908f-3c241c9cc440. Actual invocation mode draw was 7 (normal). Increased COUNTER from 4 to 5. Lease held unless the genuine 70-minute timestamp condition is met.

## Work and independently validated conclusions

- Extracted user's supplied local ZIP into /mnt/data/H17 and rebuilt all six source-derived accepted REC8 components, K01/K02/K03/K05/K06/K07, via a read-only Python standard-library script.
- Used original `verify.py` and `acceptance.json` unchanged. Verifier result: 6 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false. The resulting candidate exactly matched `results/h17-candidate.json`.
- Recorder independent replay: TRP2 schema 2, 88 records total, four CRC32 rejects; matching latch latest sequences 300–303. Telemetry latest revisions 2 for all eight kept words. Transfer latest attempts 2 for AX-7782 chunks 0–7.
- K04 independently traced ESC-N -> PS-261003-0417, RECOVER attempt 2 ACK; payload A9A9DC5731A5E2AE879C47215C2559D5 XOR mask 8556C8CB6140A7F9A5123AC7571BEE1C = 2CFF149C50E54557228E7DE60B3EB7C9, SHA-256 11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b, **NO_MATCH** against unchanged K04 target. Source warns ACK is not recovered-buffer integrity confirmation.
- K08: email 11 rejects commissioning and standby labels; email 20 differentiates original exact caption from paraphrases; note N23 references Emily's final words without quoting them. No authority chain authenticates an exact candidate in surviving export.
- No outside systems, mailboxes or operating equipment were accessed for recovery.

## Repository deliverables

- `results/replay_h17.py`: committed new standard-library source-to-candidate replay (repository resource inputs, read only). Commit 168a092da6f5aad8cda60b06f5f8e3b209319724. This version is closely based on a successfully executed, more verbose local script; future agent should run it in a checkout to independently verify.
- `results/h17-evidence-audit.md`: intermediate values, original evidence dependencies and constraints (commit 7a1b455f235c7d37f3934731ec1d157835a1e233).
- `results/README.md`: updated human-readable entry and reproduction command.
- Transient local work files /mnt/data/H17/work/replay_h17.py, replay-output.json, verifier-output.json, and /mnt/data/H17/candidate.json. Do not rely on them persisting in next invocation. Script in GitHub has same derivation logic.

## Remaining research

K04 and K08 cannot be responsibly promoted without new authoritative preserved evidence or a defensible specific error hypothesis. Original physical ESC-N coupon/media with integrity proof or an authenticated exact keeper caption would unlock the missing checks; neither is supplied. The original archive intentionally notes trimmed export and lack of completeness certification.

No per-commit CI workflow should be created (repo README rule). Inspect any relevant agent2 or Critic messages before pursuing overlapping work. Never rewrite acceptance.json or modify preservation evidence.