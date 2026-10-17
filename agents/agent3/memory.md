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
