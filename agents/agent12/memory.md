# Agent 12 continuity: independent REC8 replay and source-scope audit

Claimed 2026-10-17T23:23:53Z with run ID `f3f03be5-a5d5-467a-b40c-ae1bed843dbd` after an actual cryptographic RNG draw returned **4** (normal research mode). Incremented root COUNTER 14 -> 15 as required, and confirmed the new remote lease. The `claimed_at` timestamp must remain unchanged. Do not release the lease before a checkpoint clock comparison reaches 70 minutes. Repo README forbids per-commit workflows.

## Independent local reproduction

Extracted the uploaded 43-file export ZIP into `/mnt/data/energy`, SHA256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`. Wrote a new self-contained standard-library read-only replay at `/mnt/data/energy/work/reproduce.py` (not yet a repository artifact). It derives the six source-backed values directly, asserts their SHA-256 slot commitments, and leaves K04/K08 null. Original unchanged `verify.py` returns six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false (exit 1). Reproducer verifies CRC32 of TRP2 records, timestamp conversion to UTC for K02, highest revisions/attempts, original PTW serial order and service order.

Values: K01 `049AAB2E1CDE7A82CD7C60234303C91A`; K02 `0D7E3AB56FB75DA3EB0E2E06786D239E`; K03 `1384AF96E25D6ADA666209CB55E062FA`; K05 `FF8B78200A56E8586DCDA00EF01E4572`; K06 `5DBF40EE52FAAED9A536D3326CF0D95A`; K07 `93495F5E425AB8E592123DABAEB68545`. K04 written-rule XOR candidate `2CFF149C50E54557228E7DE60B3EB7C9` yields SHA256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b` versus target `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`: NO_MATCH. K08 final caption remains unidentified and should not be replaced by an unconfirmed paraphrase.

Built `/mnt/data/H17_recovery_workpack_2026-10-18.zip`, SHA256 `47a3c70d80c0a6e0091e72f0cdae09fe59b51b951039699e317dbf6d2a0f6bbc`, containing all 43 unaltered original members, `candidate.json`, standard-library reproducer, saved original-verifier JSON, source SHA256 manifest, and explanation. Extracted this package in an independent temp directory; checked CRCs, all 43 source member byte contents against original ZIP, replay-vs-candidate equality and the original verifier output (six PASS, incomplete). This local workpack is user-deliverable; path is invocation-local and future agents cannot rely on its continued presence.

## New source scope

Compared shared repo results, Critic communications and memories; prior deep negative K04/K08 scans are exhaustive only within named error/phrase families. Current `private/` contains only `.gitkeep` per Agent 10/11. GitHub repository currently has a single `main` branch, zero releases, zero PRs and zero issues at time of audit; no alternate branch or linked issue source carrier was surfaced. `/tags` fetch was connector-rejected and cannot be asserted empty. Normal 43-member ZIP metadata has uniform 2026-10-04 11:40 member timestamp and mode 0600; archive order is lexicographic, supporting prior ZIP structure results, but this does not prove completeness.

An exploratory test checked 133 spool payloads against simple deterministic MD5/SHA-1/SHA-256/SHA-512/BLAKE2s digests of job/attempt/time strings and several small-seed Python Random constructions; no positive identification. This is weak negative evidence, intentionally not published as a substantive result or permission to infer the generator. Worker-agent request failed with concrete 404 UNAVAILABLE and yielded no external review.

## Best next steps

Prioritize a source-supported mechanism or authenticated original carrier rather than increasing brute-force breadth. The dated spool, keeper margin and antecedent emails leave K04/K08 unverifiable; do not alter source evidence or acceptance commitments. If an independently sourced original coupon or verbatim final caption appears in future, use existing result checkers and rerun the unchanged combined verifier. Existing public source reproduction: `results/replay_h17.py`; current status: `results/README.md`. Continue investigating only falsifiable underexplored local carriers.

