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


## Checkpoint: K04 retry nonredundancy geometry

Independently extracted the three same-job RECOVER attempt payloads and computed exact pairwise Hamming distances (1,2)=68, (1,3)=62, (2,3)=62; zero byte agreement in same position for each pair. The bitwise-majority center `CDBD5D7529D7A6BA85D803215A31FDE4` has distances (34,34,28), minimizing total edits 96 and maximum radius 34; triangle lower bound from 68-bit-separated pair proves 34 is optimal. **Conditional** on all attempts being altered copies of one common 16-byte payload; records do not claim this, and REQUESTED attempts are unacknowledged. This undercuts near-copy majority-vote assumptions without authenticating K04.

Committed and verified remote artifacts: `results/check_h17_retry_geometry.py` (commit aba090f6), `results/h17-k04-retry-nonredundancy.md` (commit 518e5ead), linked in `results/README.md` (commit 1d27a159), broadcast `communications/broadcast/2026-10-17T233730Z_agent12-k04-retry-nonredundancy.md` (commit a3d976d2). Remote file presence and SHAs confirmed. Local checker tested against unmodified ZIP, same values.

Original lease check measured <70 minutes at the checkpoint. Keep researching, do not release the identity on perceived task completion.

## Checkpoint: packaged source preservation and original-verifier controls

Refined the **local, self-contained** workpack at `/mnt/data/H17_recovery_workpack_2026-10-18.zip`: now 51 members, 86,363 bytes, SHA256 **`cd520cccf52c4770dbaaf4dd33fcd3c21ceb97d46e515733f9d3d17aa1fda888`** (this supersedes the earlier 47K/package hash above). It contains a nested, byte-identical original 43-member ZIP `original/c-energy-group-documents2026.zip`, the same unmodified 43 extracted members, candidate, original verifier output, replay, source SHA manifest, report, a read-only K04/K08 intake validator and test-only acceptance positive/negative controls. Independently re-extracted into a fresh temporary directory, compared all 43 members to the original source, matched nested ZIP bytes, replayed all six accepted slots, rechecked unchanged original verifier, and ran synthetic eight-slot acceptance-path positive and rejection controls. All controls PASS; the **real** candidate remains 6 PASS / 2 MISSING / incomplete.

Added public repository test `results/test_h17_verifier_controls.py` (commit 59f340b4) and explanation `results/h17-verifier-positive-controls.md` (commit 933058b1), linked from `results/README.md` (commit 680d1b53). It never writes synthetic commitments to resources: in-memory dummy K04 bytes `00..0F`, dummy K08 bytes `10..1F`, synthetic SHA digests + synthetic combined SHA cause original `evaluate()` to accept all 8; altered dummy K04 and presenting fabricated values to original commitments both reject. No suggestion that these placeholders are original key material. Local equivalent self-test script was actually run on current ZIP; public port reuses unmodified verifier and expected repo paths.

Read the new Critic broadcast `communications/broadcast/2026-10-17T2356Z_Critic_actionable-research-gate.md`: do not run more speculative mutation radius/synonym classes without a specific source feature; treat original printer media/caption as *evidentiary condition*, not an executable external-acquisition plan. Prior source audits/confirmed chronology discrepancies remain unchanged. Continue source-supported local inference and independent quality checks, avoid merely making more speculative workpacks. Experimental PRNG/hash/spool-bit carrier probes produced no positive evidence and are not promoted.

At the last measured actual clock check, 2026-10-17T23:56:35Z, elapsed ~32.7 minutes from immutable 23:23:53Z lease, below the 70-minute checkpoint release threshold. Retain identity lease and continue productive investigation.
