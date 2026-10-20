# H-17 K04: new 20 October office records independently narrow the route ambiguity; BX25 remains an unread target-bearing candidate

**Agent 46, 20 October 2026, ~02:23 UTC.** Original archival assignment: recover K04 from *surviving local evidence* without touching the original verifier or commitments. The human's GitHub commit `ca43daaec3cdb158030464456868214cb8ac2dbc` adds **four genuinely new corporate files** that postdate every earlier 43-file negative carrier audit. This report is an exact source-to-target discrimination, not a recovered K04 payload or K08 phrase. PDF decryption/review belongs to Agent 9; see coordination in `communications/agent9/`.

## New independent, typed source joins

1. **Printer job -> logical lane -> physical cassette -> account / filing.** The original 04 Oct 2026 09:18 UTC `print-fleet-retirement-note.txt` records one full row `PS-261003-0417 ESC-N L-29/N FA-17 H17-POL-17/A3`. This independently corroborates the old `archive-labels.ini` incident-date ESC-N/job mapping, which had previously been supported chiefly by a custodian transcription and mail16's non-job-specific north-coupon description.
2. **Physical cassette -> posted supplier receipts.** The new `supplier-reconciliation-L29.csv` carries `ST-094, ST-081, ST-106, ST-099, ST-112` as precisely five `L29/R3, POSTED, FA-17, H17-POL-17/A3` lines. They match **all five** `L-29/N` tab tickets from the fleet binder index, without changing their order or discarding duplicates by index alone. The similarly named `ST-099/R2` is `VOID, FA-17, H17-POL-17/A2`; `ST-112/R4` is `HELD, FA-17, H17-POL-17/A4`. Thus the R3/A3 choice is specifically corroborated by independent accounting selection, rather than merely by the job number.
3. **Account -> historic scan transfer.** The one `RN-052, RISK, R1, FILED, FA-17, BX25/08` row ties the corresponding FA-17 family to BX25/08. The bookmarks describe BX25 as **2025 risk-property renewal folios** migrated by an old scanner. These are typed, temporally distinct associations, not evidence that the PDF has a 2026 RECOVER coupon.
4. **Negative controls.** `PS-261003-0448` is `ESC-S -> L-29/S -> LV-42 -> CS-18/5 -> RN-053 / BX25/12`; `PS-261003-0420` is `WATCH-SPARE -> L-29/W -> ST-09 -> STORES/FLT -> RN-047 / BX25/03`. These alternative routes are genuinely distinct and do not independently authenticate the selected ESC-N bytes. They give a source-derived falsifier for accidental account/folio cross-joins.

## Source-layer impact, and limits

**Actual gain:** The K04 *job-to-logical-route* ambiguity is materially narrowed by newly preserved, separately administered office records. An assertion that ESC-N was actually routed to ESC-S or WATCH-SPARE must now account for both the incident-label transcription **and** the return/account filing and matched vendor ticket series. The new records do not corroborate the selected 18:02Z attempt-2 print **payload**, its extraction checksum or the 16-byte XOR **mask**. They have no K08 final caption wording.

**Crucial 2025/2026 cut:** BX25/08 is indexed as a **2025** risk/property annex, while the incident RECOVER attempt-2 printer output occurred **3 October 2026**. A prior-year asset annexe could directly corroborate *equipment identity, original printer model, serial/seed recipe, routing, hardware, or commissioning mask* if its actual pages say so. It cannot automatically be treated as a contemporary copy of a later incident-specific 16-byte buffer. Any claim of direct coupon integrity from BX25 requires verbatim content and a date/provenance explanation.

**Read barrier:** `BX25-08.pdf` is an original committed encrypted PDF (blob `cd69d8da88c7704a50a4199e190909e31015dc99`); the bookmarks attest that the old desk scanner used a **four-position numeric release setting** and retained its paper key register at the Risk desk. Agent9's manual CI read attempt tested `0417,2508,2026,2025` without unlocking the PDF. Decryption is a separate finite local investigation, and presently **its contents have not been read**. Do not infer its text from its filename or commit hash.

## Predeclared tests if the permitted local PDF becomes legible

- If BX25/08 shows `FA-17` plus `H17-POL-17/A3` and a printer serial/model, compare this *withheld original detail* against the current spool/fleet records. A dated cross-document full serial/model agreement would justify testing a specific producer or commissioning rule; a mismatch means the new accounting link alone is not an identity proof.
- If it specifies a literal **mask or exact reduction recipe**, check both against the retained transcribed route sheet, holding the original K04 commitment and selected ACK outside the rule-selection step. A verified independent original mask is target-bearing; an unauthenticated guess is not.
- If it explicitly contains a 2026 **RECOVER attempt-2 buffer**, record document provenance/timestamps first; then decode its exact 16 bytes and only then apply the unchanged original K04 digest check. Because the indexed annexe dates from 2025, this would require an extraordinary source-specific temporal explanation.
- If it is merely 2025 property schedules/finance, close BX25 as **route-family provenance only**; do not start new seed dictionaries, arbitrary MT donor rankings, or K08 caption-guessing from accounting words.

**Recovery state at this checkpoint:** newly authenticated K04 coupon bits **0/128** and new exact final K08 words **0**. The six earlier accepted components are unaffected. This report improves route provenance, and deliberately makes no claim to an eight-slot accepted key.

## Reproduction / source references

- `resources/evidence/h17-supplemental-office-files/print-fleet-retirement-note.txt`, date and full job/return matrix.
- `resources/evidence/h17-supplemental-office-files/supplier-reconciliation-L29.csv`, `ST-094/081/106/099/112` and `RN-052/053/047` rows, including R2 VOID and R4 HELD negative controls.
- `resources/evidence/h17-supplemental-office-files/retired-office-bookmarks.html`, Risk/BX25 links and old-scanner release-note caption.
- `resources/evidence/h17-supplemental-office-files/BX25-08.pdf`, encrypted original awaiting a successful *permitted local* release.
- Prior source-layer ambiguity: `results/h17-k04-multiple-source-ambiguity.md`.
