# H-17 REC8/1 missing-evidence intake plan

**Scope:** incident-preservation historical archive only. This is a records request, with no authority to contact facility systems, change controls, or retrieve material from restricted incident areas.

The local export 06 passes exactly six component commitments. K04 and K08 remain null. The acceptance inventory is a byte validator; it cannot reconstruct missing original source by itself.

## K04: exact ESC-N coupon/media evidence

Find a **separately preserved original or integrity-checked record** for incident-date logical route ESC-N, job `PS-261003-0417`, RECOVER attempt 2 acknowledged at `2026-10-03T18:02:00Z`. Prioritise the printed coupon photograph/scan with its 16-byte RECOVER field, an independently captured device buffer accompanied by a trustworthy checksum, or a cryptographically authenticated independent replica. Preserve complete bytes, attempt/job labels, original timestamps, acquisition method, and custody history. The existing dispatch-log ACK alone is insufficient to authenticate the copied `A9A9DC5731A5E2AE879C47215C2559D5` payload, which fails the K04 commitment after the required XOR.

On receipt, isolate the new source and compute its file SHA-256. Check its exact 16 payload bytes using [check_h17_coupon.py](check_h17_coupon.py) against the unchanged route-sheet mask and the untouched `acceptance.json`. Record the resulting uppercase K04 component and the acceptance state. An accepted hash is a byte check; retain independent provenance information.

**Conditional second-source check:** The mask in `evidence/recovery-routing.json` and the job map in `evidence/archive-labels.ini` are both transcriptions without independent original witnesses. Consequently, an authenticated original coupon might *still* fail the commitment if the retained mask or route mapping is inaccurate. If a newly authenticated coupon fails, preserve that observation without altering its bytes, and look within the permitted case materials for independent original mask and routing evidence. Conversely, a different mask that makes the retained spool bytes pass cannot by itself authenticate the spool reconstruction. This source-layer ambiguity is established in [the K04 analysis](h17-k04-multiple-source-ambiguity.md); it must remain explicit at intake.

## K08: exact final keeper caption

Seek Emily's final desk-margin original or an independently authenticated image of the envelope/caption as actually used, or a contemporaneous verbatim quotation identifiable as the final H-17 incident envelope. Preserve the exact sequence of words, provenance, date, and image/transcription method. The survived N02/N06 drafts and N17/N18 commissioning/standby labels are distinct from the final phrase. N23 states that exact final words were written in a margin yet does not reproduce them. Narrative descriptions in mail 11/20 provide theme without wording.

Use [check_h17_caption.py](check_h17_caption.py) to apply the recorded ASCII normalization, desk nonce, HMAC-SHA256 and original K08 slot digest. Retain the original unnormalized text or image, because normalization collapses punctuation and capitalization. Keep guessed captions separate from provenance-backed text.

**Conditional nonce-provenance check:** `desk_nonce` also appears only in the uncorroborated routing transcription, as documented in [the shared commissioning-parameter audit](h17-common-commissioning-parameter-risk.md). If authenticated final caption wording later fails the recorded K08 HMAC/slot check, keep its original wording intact and independently assess the nonce and reduction-rule transcription before rejecting that new historical witness. A proposed alternate nonce that makes some plausible caption pass the hash does not alone authenticate the historical nonce or caption. No such alternate is established in this export.

## Specific newly indexed records-locator lead (20 October 2026)

The separately supplied office-profile bookmark file `resources/evidence/h17-supplemental-office-files/retired-office-bookmarks.html` names an **incident desk export index** at the original Windows mapped-drive URI `file:///R:/Records/INDEX/IR-261003-H17.txt`. This is a concrete potential original **source-locator**, first called out by Agent 39 on 20 October, distinct from the now-classified 2025 property folio `BX25/08`. **The target index file itself is not in the 43-member export or the current shared source set, and no K04 payload bytes or K08 margin words have been observed at this locator.** The bookmark header calls itself a September-cached profile while the filename identifies a 3 October incident, so neither its creation chronology nor the physical target content can be inferred merely from the link.

If the records custodian **already possesses an authorized preserved copy** of this exact index, acquire that copy through ordinary records custody, with its original modification timestamps, file hash and a nonmodified transcription of all referenced paths. Check for a dated, explicitly indexed *3 October 2026* ESC-N attempt-2 media witness or an original final keeper-margin quotation; a generic desk index, unrelated document name or later explanatory note gives no new REC8 bytes. An `R:` file URI is a locator on a historical Windows drive, **not a web URL or permission to access an unrelated file share**. The live portal's sign-in and password logging provide no authority for this route. This prioritizes one concrete missing document without asserting its existence, contents or REC8 acceptance. [Original locator observation](../agents/agent39/memory.md).

## Consolidated acceptance

Once both new source-derived values pass their individual unchanged slot commitments, populate only K04 and K08 in the preserved six-slot candidate, and run the original offline `verify.py`. Record all eight per-slot states, the combined digest, and the final accepted flag. **Until the combined verifier accepts, describe the envelope as incomplete.** Store source material and its SHA-256 fingerprints separately from analytical scripts and preserve the existing source ZIP without mutation.

Existing status, checks and uncertainties: [recovery report](h17-recovery.md), [secondary audit](h17-secondary-evidence-audit.md), [replay](replay_h17.py), [source integrity manifest](h17-source-blob-manifest.json).
