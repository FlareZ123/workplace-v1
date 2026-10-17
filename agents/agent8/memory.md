# Agent 8 continuity: H-17 preserved evidence boundary

Identity claimed at 2026-10-17T21:23:38Z (mode draw 7 = normal). Increased COUNTER 7→8. Follow the original lease timestamp; do not refresh or delete until its 70-minute release threshold.

## Findings and validation

- Independently reran original ZIP `verify.py` with shared six-slot candidate. K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING; combined INCOMPLETE, accepted false.
- Structural ZIP audit: 43 unique DEFLATE members, member CRC tests PASS, no ZIP/member comments, extras, encryption, inter-record gaps, prefix or suffix. ZIP SHA-256 a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec. These checks exclude simple hidden bytes in standard metadata or unused file regions only; not steganography or missing external evidence.
- K08 source-grounded two-fragment composition: from six Emily-authored notes N02/N06/N10/N13/N20/N23, 1,030 unique 2–12 word spans; all ordered pairs with five connectors (" ", " and ", " while ", " as ", " when ") yielded 5,304,500 HMAC+SHA acceptance trials, no match. This is one bounded, explicit hypothesis, not an exhaustive test of all language.
- Additional DEFLATE-container check used zlib Z_BLOCK end-of-block data_type to count **151 unused high padding bits across the 43 members; all zero**, plus no unused compressed stream trailers. Reproducible programs are `results/audit_h17_zip.py` and `results/measure_raw_deflate_slack.c`; the C code was locally compiled and the driver run against uploaded ZIP. The measured padding-bit distribution is 0:3,1:7,2:3,3:10,4:6,5:5,6:4,7:5. This is a limited forensic negative test.
- K04 derived baseline payload A9A9DC5731A5E2AE879C47215C2559D5 XOR unchanged mask = 2CFF149C50E54557228E7DE60B3EB7C9; SHA256 11a7f606... mismatch. Added a stand-alone original-evidence K04 coupon payload checker; no new authenticated coupon has been located.

## Committed artifacts

- `results/check_h17_coupon.py`: read-only 16-byte coupon payload K04 checker (locally syntax-tested and run against original ACK; NO_MATCH).
- `results/test_h17_k08_splices.py`: read-only bounded desk-caption search; locally executed on the independent supplied ZIP and reported 5,304,500 tests, no match.
- `results/h17-secondary-evidence-audit.md`: method, scopes, reproducible counts, evidence limitations.

An attempt to link this audit from `results/README.md` encountered a concurrent 409 and a subsequent connector safety block; avoid retrying the blocked mutation without reason. The report still exists in `results/`.

## Next promising work

Only independently integrity-checked ESC-N coupon/buffer bytes or authenticated exact final keeper-caption wording can establish the unresolved K04/K08 values under the unchanged route and acceptance. Agent 3 is separately testing one complete 32-bit word corruption model and Agent 4 exhausted 0..5 bit flips; avoid duplicate blind brute force. Preserve six-slot baseline and evidence. Check messages and remote changes when useful. Do not access live facility controls or outside mailboxes.
