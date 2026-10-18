# Agent 3 continuity: independent preservation-copy integrity review

Claimed 2026-10-17T21:05:42.977Z as run `h17-agent3-2026-10-17T21-05-42-977Z`. Random mode draw 2 (normal). Bumped shared COUNTER from 5 to 6 and verified lease existence.

## Main finding

The uploaded `c-energy-group-documents2026.zip` is **byte-for-byte identical across all 43 members** to the repository's `resources/` tree at review. Computed standard Git blob SHA-1 from each ZIP file and compared with recursively listed `main` Git tree blob IDs; every path and object ID agreed. Detailed hashes and method: `results/h17-export-equivalence.md`, linked in `results/README.md`, and broadcast in `communications/broadcast/2026-10-17T211238259Z_agent3-export-integrity.md`.

ZIP SHA256 a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec; manifest SHA256 728d3dfa8c8e6bdcc3f5010cb0cc217a57cd430d705645659d2794bc4ab97343. Source-copy divergence cannot explain unresolved K04 or K08.

## Verification and limitations

- Copied accepted six components from public candidate into local `candidate.json`; ran unchanged ZIP `verify.py --candidate candidate.json --json`: K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false.
- Confirmed spool job PS-261003-0417 has ACK of LABEL at 16:45 and requested RECOVER at 18:01, ACK RECOVER at 18:02 (attempt 2), requested RECOVER at 18:03. Existing XOR result 2CFF149C50E54557228E7DE60B3EB7C9 fails K04 acceptance. The print log warns ACK not payload-integrity certificate.
- Enumerated 405 raw/masked/reversed-masked hashes from 16-byte contiguous windows in hex runs across original evidence; no K04 match. This is only a narrow negative test.
- Keeper caption absent as authenticated final exact wording. `mail/11.eml`, `mail/20.eml` and crew notes describe rejected labels, drafts and paraphrases; slot K08 HMAC can authenticate candidates but not invert missing language.

## Next valuable work

Source-driven recovery remains blocked by K04 payload integrity and K08 exact final caption provenance. If independent archival artifacts appear, test slots then combined commitment without modifying acceptance or verify.py. Avoid ungrounded brute-force guesses. Existing fully read-only derivation: `results/replay_h17.py` (Agent 7). No per-commit CI.

The invocation's original identity lease remains held; release only upon 70-minute elapsed checkpoint under prompt.md.

## Mid-run additions (17 October, after first checkpoint)

- New exact HMAC/SHA slot checker at `results/check_h17_caption.py`; reference coupon checker independently added by Agent 8 at `results/check_h17_coupon.py`.
- Exhaustive source-preserving K08 sentence-deletion trials: N02 8,191, N06 2,047, N10 33,554,431, N13 4,194,303, N20 first sentence 524,287: **38,283,259 NO_MATCH**; C implementation `results/k08-subsequence.c`.
- Two contiguous spans from different selected Emily notes joined via six source-inspired connectors: **3,823,524 NO_MATCH**; `results/k08-two-spans.py`. Total 42,106,783 bounded new K08 tests, documented under `results/h17-evidence-audit.md`. These are hypotheses, not authenticity evidence.
- All 201,830 raw-byte window K04 trials negative; same-job 4-byte word-mosaic of all four PS-261003-0417 rows: 256 combinations no match; 768 endian/4byte word order forms no match.
- Local long-running K04 aligned 4-byte whole-word corruption scan launched 2026-10-17T21:18:15Z, four subprocesses (PIDs initially 988,989,990,991), one for each offset 0,4,8,12, complete 0..2^32 replacement range each; source `results/k04-wordscan.c`, locally compiled OpenSSL variant and output at `/mnt/data/H17-agent3/work/scan-pos-*.log`. **Still running when this checkpoint was composed; do not report a result before log/pid verification.**
- Separate short same-job byte-mosaic search (3 RECOVER attempts, 3^16 combinations) launched 21:32:17Z, local binary `/mnt/data/H17-agent3/work/k04-mosaic` and log. Verify completion before including conclusion.
- Agent 4 independently excluded entire K04 Hamming-distance ≤5 class (275,584,033 candidates), see `results/h17-k04-bitflip-bound.md`; no identity overlap with our 4-byte arbitrary-word scan.
- Apparent chronology caveat: `mail/16.eml` dated 07:49 UTC 3 Oct speaks as if 18:03 UTC REQUESTED entry has already occurred. Added cautious note to `results/h17-evidence-audit.md`; it is not evidence of a corrected payload.

## Subsequent checkpoint: full aligned K04 32-bit replacement ranges

- Validated accelerated SHA-256 one-block checker `results/k04-wordscan-fast.c` against the direct ordinary SHA-256 result at all four aligned offsets. Positive controls returned FOUND for known original candidate; original K04 target restored for exhaustive runs.
- Full offsets 0, 4, 8, 12 each enumerated 2^32 replacement words (17,179,869,184 combined), all NO_MATCH. Detailed reproducible findings and runtimes: `results/h17-k04-wordscan-bound.md`, linked in `results/README.md`. Initial slow processes were stopped intentionally once fast implementation was positively validated and replaced; no conclusions based on those incomplete slow scans.
- Completed three-RECOVER-attempt byte mosaic 3^16 = 43,046,721 selection assignments, all K04 NO_MATCH, source `results/k04-byte-mosaic.c`, details in `results/h17-evidence-audit.md`.
- Additional nine unaligned four-byte contiguous windows (positions 1,2,3,5,6,7,9,10,11), each split into four 2^30 replacement segments, **currently executing** under local orchestrator PID initially 2144. Script `/mnt/data/H17-agent3/work/k04-burst4-orchestrator.py`, logs `/mnt/data/H17-agent3/work/burst4-orchestrator.log`, per-chunk atomic JSON `burst4-pos{pos}-part{part}.json`, summary `burst4-summary.json`. It is NOT YET a completed result. Check process and all 36 chunks before reporting a verdict.
- Newly preserved `results/k08-photo-splices.py` tests paired spans of photo/galley/mug captions and Emily drafts; script has **not yet been executed** in local test at this checkpoint. Run after four-byte burst CPU jobs complete.

## 18 October 2026 incarnation (run 35359d46-f82f-496d-8a05-0e83ed0edebd)

- Uniform draw 6 selected normal mode. Incremented shared COUNTER 74 to 75 (commit 6bbe982a) and claimed Agent 3 with current lease (commit 60e3a9cf). Existing agent memories and latest Critic broadcasts read, especially the stop-duplicate-handoffs and evidence-first gates. No original case file, route, commitment, or verifier altered.
- Imported existing accepted six-slot candidate instead of reimplementing source replay. Extracted supplied 43-member ZIP locally, ran its original unchanged `verify.py --candidate ... --json`; exit status 1, 6 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted=false. K04 selected ESC-N ACK attempt 2 XOR remains `2CFF149C50E54557228E7DE60B3EB7C9` and original SHA256 NO_MATCH.
- Checked alternate tracked source refs as a narrowly scoped supplement to Agent 47's existing Git-source-lineage result: GitHub's repository branch-list endpoint displayed only `main` on 18 October 2026; no alternate advertised branch was available to inspect for older original K04/K08 source material. Tags endpoint unsupported and Git tags ref namespace reported Not Found; cannot infer about arbitrary unreferenced objects. This is repository-hosting context, not original historical provenance. It does not resolve either slot and did not warrant a separate result report.
- For this user-facing invocation, created verified local deliverables at `/mnt/data/h17-delivery/`: `candidate.json`, `verify-result.json`, `derivation-notes.md` (atomic locked writes). Such local files do not persist across future invocations and should not be treated as a shared research finding. The 6-slot canonical fixture in `results/` remains authoritative.
- Next useful work: independently source-anchored original printer bytes or a local mechanism reconstructing the authenticated final caption. The user's local case prohibits contacting external mailboxes, personnel and facility devices. Avoid further broad mutations and duplicate workpacks; new tests require source anchor, historical mechanism and a non-hash discriminating prediction. No new accepted component was found.
