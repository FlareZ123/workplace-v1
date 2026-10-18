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

## Consolidated acceptance

Once both new source-derived values pass their individual unchanged slot commitments, populate only K04 and K08 in the preserved six-slot candidate, and run the original offline `verify.py`. Record all eight per-slot states, the combined digest, and the final accepted flag. **Until the combined verifier accepts, describe the envelope as incomplete.** Store source material and its SHA-256 fingerprints separately from analytical scripts and preserve the existing source ZIP without mutation.

Existing status, checks and uncertainties: [recovery report](h17-recovery.md), [secondary audit](h17-secondary-evidence-audit.md), [replay](replay_h17.py), [source integrity manifest](h17-source-blob-manifest.json).
