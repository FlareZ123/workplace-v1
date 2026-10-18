# H-17 K04 printer reconstruction: two source cohorts and job/attempt collision

**Agent 15, 18 October 2026.** Read-only census of original `resources/evidence/print/spool-reconstruction.log` (133 complete entries) against the original routing and acceptance. The [reproducer](check_h17_spool_cohorts.py) checks the serialized form of every entry, record count, sequential job/time identities, and K04's unchanged slot commitment.

## Observed distinction

- **128 regular entries**, job IDs `PS-261003-0300` through `PS-261003-0427`, occur every five minutes from **07:00 to 17:35 UTC** on 3 October. All use an offset-style timestamp ending **`+00:00`**, `ATTEMPT=1`, `STATE=ACK`. Classes: 52 LABEL, 41 STORES, 35 RECOVER.
- **Five later entries** at 18:01, 18:02, 18:03, 18:24 and 18:25 UTC use the literal **`Z`** timestamp suffix. All five are `CLASS=RECOVER`; three ACK and two REQUESTED. These contain the three K04 candidate attempts plus the ESC-S and WATCH-SPARE records.
- Two job IDs recur across this cohort boundary: `PS-261003-0417` and `PS-261003-0420`. The composite identifier `(JOB=PS-261003-0417, ATTEMPT=1)` **collides**: line 119 at 16:45 is LABEL/ACK; line 130 at 18:01 is RECOVER/REQUESTED. Consequently, `JOB + ATTEMPT` alone is not a unique spool event key. Time, class and state disambiguate these records.

The reproducible selection remains unchanged. For incident-date ESC-N, the original route names job `PS-261003-0417`; `mail/16.eml` calls for the last acknowledged RECOVER payload of that exact job. Line 131 at 18:02, attempt 2, is the unique matching ACK/RECOVER row. Its payload `A9A9DC5731A5E2AE879C47215C2559D5` XORed with mask `8556C8CB6140A7F9A5123AC7571BEE1C` yields `2CFF149C50E54557228E7DE60B3EB7C9`. The unchanged K04 SHA-256 check is **NO_MATCH**.

## Evidentiary consequence

The perfect timestamp-format segregation and cross-cohort identity reuse show **two distinct serialized record populations** inside the one reconstructed text file. This is an observation about representation, not proof of separate physical devices, a particular logger, forged records, corrupted bytes, or a reconstructible random generator. A single exporter could have combined differently formatted material. It would be unjustified to infer a corrected coupon by applying a common error model to unrelated rows without additional independent source evidence.

The earlier 133-payload scan already found no matching K04 coupon under the original XOR mask; the new observation does not overturn that negative result or recover missing bytes. Its practical value is to caution against treating every row as an exchangeable, independently corroborating retry of the selected 18:02 coupon. The original custodian separately warns that the ACK field reports dispatch acknowledgement rather than integrity of the retained payload.

For the distinct `mail/16.eml` chronology anomaly and K08 text sufficiency boundary see [source-rule consistency](h17-source-rule-consistency.md) and [source-sufficiency matrix](h17-source-sufficiency-matrix.md). Original status remains **six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted=false**.
