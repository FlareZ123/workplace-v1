# K04 printer tail: metadata-only generator models fail a pre-hash functional-key test

**Agent 42, 19 October 2026.** This report excludes some generic metadata-to-payload models against the *observed spool bytes*. It does not supply original K04 bytes, authenticate source integrity, or change the six-of-eight REC8 acceptance status.

## Original-record anchor and discriminatory prediction

Original 43-member case ZIP, `evidence/print/spool-reconstruction.log` (existing source SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`). The 128 regular `+00:00` entries each have a distinct job number, so a proposed formula `PAYLOAD=F(JOB)` cannot be contradicted by two regular rows *regardless of the function's mathematical form*. The five `Z`-timestamp RECOVER-tail entries provide a concrete independent cross-cohort discriminator because two jobs recur.

A deterministic formatter that accepts only `JOB` as input predicts the same 16 output bytes for every row using that job. Any extension using `JOB`, `CLASS`, `STATE`, `DEST` but omitting `ATTEMPT` likewise predicts equal output for the two observed `PS-261003-0417` `RECOVER / REQUESTED / bench` rows. This prediction can be checked entirely against source bytes, without considering K04's acceptance SHA256 or inventing a seed.

## Original spool witnesses

| Physical source line | JOB suffix | ATTEMPT | CLASS | STATE | DEST | PAYLOAD |
| --- | --- | --- | --- | --- | --- | --- |
| 119 | 0417 | 1 | LABEL | ACK | bench | `E1E60D5F6B6DD2225FA6D5A2A63AD932` |
| 130 | 0417 | 1 | RECOVER | REQUESTED | bench | `CD3E4F216ADB2FB180DA2AA90B33F7A4` |
| 131 | 0417 | 2 | RECOVER | ACK | bench | `A9A9DC5731A5E2AE879C47215C2559D5` |
| 132 | 0417 | 3 | RECOVER | REQUESTED | bench | `44D53DFC29D7943A95D89371DA58EC64` |
| 122 | 0420 | 1 | STORES | ACK | desk | `31C9714DD36DB2677BB9006670A9DFFD` |
| 134 | 0420 | 2 | RECOVER | ACK | bench | `432475F72A62DB39F3D5693E2C937FA4` |

Three relevant *observed-value* falsifiers, each independent of REC8 targets:

1. `F(JOB)`: four different source payloads for job 0417 and two for job 0420, so no single-valued mapping exists on these rows.
2. `F(JOB,ATTEMPT)`: spool lines 119 and 130 have the same job and attempt 1, yet different payloads.
3. `F(JOB,CLASS,STATE,DEST)`: lines 130 and 132 have the same job, class RECOVER, state REQUESTED, destination bench, yet distinct payloads. Thus a model using any subset of those four metadata fields, without ATTEMPT, cannot explain all source rows.

## Exhaustive functional-key test on named non-time fields

Grouped all 133 complete original spool entries by `JOB` and every subset of `ATTEMPT,CLASS,STATE,DEST`. A grouping is *conflict-free* only if every row with the same grouping tuple has exactly the same `PAYLOAD`. Source selection and K04 acceptance SHA256 were excluded from the test.

| Proposed input fields | Distinct conflicting tuple groups |
| --- | ---: |
| JOB alone | 2 |
| JOB + ATTEMPT | 1 |
| JOB + CLASS | 1 |
| JOB + STATE | 3 |
| JOB + DEST | 1 |
| JOB + CLASS + STATE + DEST | 1 |
| JOB + ATTEMPT + CLASS | 0 |
| JOB + ATTEMPT + STATE | 0 |

The **only minimal conflict-free combinations containing JOB**, among those named metadata fields, are `(JOB,ATTEMPT,CLASS)` and `(JOB,ATTEMPT,STATE)`. Their extensions also have zero observed conflicts. Timestamp was deliberately excluded because each timestamp uniquely identifies a line, making a timestamp-key model vacuously fit any bytes.

The earlier [printer cohort identity audit](../../results/h17-spool-cohort-identity-audit.md) already identified JOB/ATTEMPT reuse; this experiment extends it to the **minimum input-field requirements for all deterministic metadata-only formatter models**, including arbitrary cryptographic functions. It explains why job-only HMAC/digest models are ruled out without needing a larger algorithm search.

## What this does and does not predict

This is a **model-class falsification conditional on observing the spool bytes correctly**. The custodian expressly disclaims individual payload integrity, so observed source conflicts could theoretically themselves reflect faulty bytes or mixed logs. If the historical printer used a job-only deterministic function and the output differs today, that would motivate a source-corruption hypothesis. The test cannot identify which value is correct. `ATTEMPT` and `CLASS` or `STATE` merely remove observed equal-input collisions; they do not authenticate a generator, provide generalization across cohorts, or predict the held-out K04 RECOVER ACK.

For actual recovery, a proposed formatter must state an independent provenance mechanism and predict the 0448/0420 RECOVER-tail bytes before looking at K04's digest. The original case does not specify a formatter with such a bridge. No further unsourced PRNG/digest expansion is justified. Original acceptance, ZIP, verifier and source records untouched.
