# Agent 14: H-17 direct-carrier evidence search

Identity claimed 2026-10-17T23:34:00.750Z, invocation counter advanced 16 to 17. Repo: FlareZ123/workplace-v1.

## Verified baseline

Original REC8/1 acceptance is still 6 PASS (K01/K02/K03/K05/K06/K07), K04 and K08 MISSING, combined INCOMPLETE/accepted false. See results/h17-candidate.json and results/h17-verify.json. Strong source-provenance context and bounds in results/README.md and results/h17-source-rule-consistency.md. Other agents already tested massive K04 bit flips, word replacement/reassembly, retry mosaic and K08 draft-fragment grammars; do not duplicate these.

## My investigation

Expanded direct-source carrier extraction over the entire local 43-member ZIP rather than only spool job fields and crew notes. Reproducible read-only script at results/check_h17_all_carriers.py; report results/h17-all-file-carrier-bound.md; synthesis updated in results/README.md.

All 43 original files tested: 108,021 raw 16-byte sliding windows and 432 decoded windows from 32-hex-character runs for K04: 0 matches to fixed XOR/SHA256 acceptance. Across 42 valid UTF-8 source files (trip-recorder.raw excluded only from text), 618,316 contiguous normalized 1–40-word spans for K08: 0 matches to fixed nonce HMAC/truncated-component SHA256 acceptance. Positive-control scanner runs, using synthetic targets derived from actual ACK payload and N01 caption, locate both carrier types.

These are finite, source-grounded negative scopes. They do not rule out damaged/split/alternate-encoded coupon or original caption paraphrase absent from export. Preserve originals and unchanged verifier. Avoid inferring impossibility from a negative test.

## Next useful lines

- Seek evidence-based alternate encodings only if an observed artifact supports one; avoid arbitrary brute-force searches.
- If pursuing source-sufficiency, focus on exact carrier format, reported corruption mechanisms, internal consistency of spool, and archival provenance anomalies rather than K04 random payload preimages.
- For K08, look for a genuinely authenticated exact final-caption quotation/other local carrier rather than expanding improbable sentence grammars.
- Check communications/broadcast/ for Critic warnings and agent overlap.
- At every persistent checkpoint compare actual clock to the lease claimed_at. After >=70 min, preserve state, delete lease as final action; before threshold, continue productive research.
