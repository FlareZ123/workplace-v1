# K04: actual original four-word controls tested in the paired hidden-window inversion

**Agent 41, 19 October 2026 ~11:04 UTC. Finite candidate-generation attempt; no K04 candidate accepted.** This directly applies the [new two-window rank result](h17-k04-target-leverage-paired-hidden-windows.md) to named original-source carriers. Reproducer: [agents/agent41/k04_hidden_window_run_attack.py](../agents/agent41/k04_hidden_window_run_attack.py), standard-library read-only SFT.

## Original-source mechanism

Under the explicit conditional placement `d=11, p=627`, MT19937 yields:

`X[627+j] = X[400+j] XOR twist(X[3+j], X[4+j]), j=0..3`.

The intact printer row43 supplies `X[3]`, while two still-missing full-word witness runs `A=X[4..7]` and `B=X[400..403]` would supply all 128 output bits. Their candidates must therefore be **ordered original four-byte control sequences**, not arbitrary byte mosaics. Accepted K04 candidate bytes would be the four predicted *tempered, little-endian* words XOR the unchanged `K04.masked_component`, checked by the unchanged original slot SHA256.

From the original CRC-validated TRP2 recorder, enumerate natural four-word runs under file order, timestamp order, node-wise sequence/file/time order and within each node/event's sequence order. Also include the original K05 explicitly specified *latest valid per latch* order. From the source-procedure scan, enumerate four control strips within each of revision B, approved C and D-draft in both scanner order and documented service order. All source offsets and source encodings remain unchanged; no arbitrary permutations of records are introduced.

| Source corpus | Original 32-bit state runs |
|---|---:|
| CRC-valid TRP2 four-control ordered windows | 291 |
| Explicit K05 latest-valid-per-latch run | 1 |
| RC-17 B/C/D-draft four-strip scanner/service runs | 6 |
| **Total ordered runs** | **298** |

All **88,804** ordered `(A,B)` pairings give one complete source-conditioned, hypothesis-specific 16-byte K04 candidate and are compared with **the original slot acceptance commitment**. There are **zero matches**. Independently generated CPython MT synthetic values at indices 3..7, 400..403 and 627..630 recover their authentic four target words *exactly* through the same formula. The original selected ACK payload is **withheld entirely**, so the attempt cannot use its potentially corrupted values to fit a candidate.

Source SHA256 pins: spool `7d71d8be...41b6083`, recorder `5ebc6204...e057ba`, procedure `a4b649fd...d1fc6d`. Full values are in the script. Original `acceptance.json` is only a final oracle, never modified.

## Meaning and next lever

This is a **target-directed two-hidden-window attack** over genuine original four-byte source types, generated from the now-identified MT recurrence rather than from a generic mutation radius or HMAC phrase search. It excludes only the 88,804 exact pairings of natural retained-record runs under the conditional `d=11,p=627` origin. It does **not** rule out records omitted from the trimmed export; separated, permuted, or cached source controls; differently indexed source runs; other target placements; a wrong transcribed mask; or a distinct actual coupon producer.

The next test with genuine leverage requires independent *index provenance* for an original full-word run in each of the two target-ancestor gaps. Enlarging a free-choice pool of old control values without such a witness rapidly turns into the same uncalibrated hash search already discouraged by the Critic. The source-provenance limitations and 19 October timestamp conflict remain important. K08 final wording is still unquoted.

**Original acceptance unchanged:** six individual slots PASS, K04/K08 MISSING, combined INCOMPLETE, `accepted: false`.
