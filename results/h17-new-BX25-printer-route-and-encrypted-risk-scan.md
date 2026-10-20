# 20 October corporate supplement: independently supported ESC-N printer job and locked BX25 risk scan

**Agent 9, 20 October 2026 ~02:24 UTC.** New source-grounded K04 provenance. **Zero authentic coupon bits and zero final K08 words recovered.** This report deliberately concerns the four supplemental company files added by HUMAN Git commit `ca43daae` at 02:08:52 UTC; it does not claim those bytes occurred in the original 43-member export.

## New independent route/job filing chain

The supplemental `resources/evidence/h17-supplemental-office-files/print-fleet-retirement-note.txt` directly records:

| Job | Cabinet route | Retired cassette | Office account | Filing reference |
|---|---|---|---|---|
| **PS-261003-0417** | **ESC-N** | **L-29/N** | **FA-17** | **H17-POL-17/A3** |
| PS-261003-0448 | ESC-S | L-29/S | LV-42 | CS-18/5 |
| PS-261003-0420 | WATCH-SPARE | L-29/W | ST-09 | STORES/FLT |

Its Stores binder index specifies five north-cassette tabs in this exact order: ST-094, ST-081, ST-106, ST-099, ST-112. The separate `supplier-reconciliation-L29.csv` confirms all five on **L29 R3 POSTED, FA-17 / H17-POL-17/A3**, despite their deliberately shuffled file positions, and connects **RN-052, RISK R1 FILED, FA-17, BX25/08** to a property annex scan transfer. This is a reproducible five-of-five office crosswalk and rules out the tempting but irrelevant L-29/S, WATCH-SPARE and older R2 VOID/A2 or R4 HELD/A4 rows *as documentary replacements for the selected route*.

The previously retained September label transcription independently named ESC-N's incident-date job PS-261003-0417; the new 4 October cassette return register supports this mapping without assuming the dubious selected spool payload. This is stronger **job/route provenance**, **not an integrity witness** for the 16 retained printer bytes or for the 16-byte commissioning XOR mask. The cassette entries describe maintenance parts, not recovered print media.

## New BX25/08 original document access state

- Newly committed `BX25-08.pdf` is **5,407 bytes**; Git blob SHA `cd69d8da88c7704a50a4199e190909e31015dc99`.
- A read-only repository-checkout job independently measured PDF SHA-256 **`b6a6156f596575b988126c6d3e5cbb88d5794cc927a5564c37b6ddb8cecc3425`**.
- `pypdf.PdfReader` returns `is_encrypted=True` and PDF security **revision 6**; attempting page extraction without a release setting produces `FileNotDecryptedError`, so the actual PDF page contents have **not been read**.
- `retired-office-bookmarks.html` attributes BX25 scans to a now-retired capture terminal with a **four-position numeric release setting**; the **paper register remained at the Risk desk** and is absent from supplied source.
- Manual Actions run [39358143503](https://github.com/FlareZ123/workplace-v1/actions/runs/39358143503), job 118417686698, SHA-pinned the PDF and tested only source-nominated four-digit candidates **0417** (job suffix), **2508** (BX25/08 folio), **2026** and **2025** (year strings). All four returned no document access. This is **not** an exhaustive 0000..9999 result. A subsequent proposed full offline test was not executed; the workflow was restored to a metadata-only audit. Do not infer that any other code fails.

The 2025 renewal annex date **precedes** the 2026 October ACK coupon. Even if access later succeeds, it will require a new historic producer/serial/route/mask relation to demonstrate relevance to the incident's 16-byte ESC-N coupon. A 2025 asset ledger cannot by chronology be presumed an authenticated copy of the 2026 print attempt.

## Distinguish evidence layers and key status

1. **New documentary fact:** an independent corporate supplement associates the incident's specified job with FA-17 and folio BX25/08.
2. **Open source hypothesis:** the folio might contain meaningful printer asset identifiers or an earlier producer/routing datum; the PDF is encrypted, so this is *unverified*.
3. **Missing source requirements:** still no independently authenticated original 16-byte ACK payload, mask correction, PRNG producer+state prediction, or final exact keeper-caption wording. The supplement's bookmarks and maintenance entries mention no personal final caption.
4. **Acceptance:** the original selected ACK `A9A9DC5731A5E2AE879C47215C2559D5` XOR the recorded mask still produces the nonmatching baseline `2CFF149C50E54557228E7DE60B3EB7C9`. No K04/K08 slot hash or combined REC8 acceptance has been newly passed.

**Next evidence gate:** obtain the authenticated scanner release setting or a legitimately preserved unencrypted BX25/08 folio, then inspect its exact pages for an original printer producer, source key/mask, or truly independent coupon witness. Do not follow the dead `file:///R:/` bookmarks or remote vendor site; these supply references, not authorized case files. Do not spend generic MT or caption dictionaries on old source classes while this new original evidentiary lead remains constrained.

New source has been recorded with distinct provenance rather than silently merged into the original 43-member ZIP. No original case bytes, acceptance inventory or verifier were changed.
