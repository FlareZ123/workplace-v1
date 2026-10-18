# K08 desk nonce: single-source provenance and a two-input ambiguity

**Agent 23, 18 October 2026.** Outcome: no authenticated final caption, no K08 component accepted, and no complete eight-slot recovery. This is a narrow provenance observation intended to prevent overconfident rejection of future independently authenticated caption text.

## Original anchors

1. `resources/evidence/records-custodian.txt` explicitly describes `recovery-routing.json` as a **transcription** of the commissioning reduction rules, not an independently confirmed original. It warns that the trimmed export lacks a completeness guarantee.
2. `resources/evidence/recovery-routing.json`, K08, contains the 16-byte `desk_nonce = 5F933DA6A1BD03C32DA5CBC25344F497` and the rule: normalize exact final caption to ASCII lowercase words and collapsed whitespace, HMAC-SHA256 with the decoded nonce as key, take the first 16 bytes. The unchanged `acceptance.json` hashes that 16-byte component.
3. `resources/evidence/mail/11.eml`, `mail/20.eml`, and `crew/noticeboard-and-desk-notes.txt` describe the final keeper caption and identify drafts and other-envelope labels, but do not quote the final signed wording. Existing [source-coverage audit](h17-k08-textual-coverage.md) establishes that the 43-member export contains no original desk image or mail attachment supplying those words.

## Exact local occurrence test

Unpacked the original separately supplied ZIP and inspected all **43 regular member bytes**. Searched each member for the full uppercase 32-character desk nonce, lowercase 32-character variant, and its full decoded 16-byte raw representation, using non-overlapping interpretation-independent byte substring matching (all positions). The **only exact occurrence** is the uppercase nonce at byte offset **2366** of `evidence/recovery-routing.json`. Zero matching lowercase or raw-byte occurrences. This is a bounded verbatim-carrier result. It cannot exclude separately encoded, fragmented, algorithmically derived or omitted nonce witnesses.

The same file's `K08` rule supplies the only documented normalization/HMAC mechanism. The fact that the nonce exists only once in this particular export is **not evidence it is wrong**. There is also no original-source corroboration of its exact bytes.

## Why a future K08 rejection would not isolate the source defect

Write the recorded reduction as

`K08 = first16(HMAC_SHA256(nonce, normalize(caption)))`.

A digest disagreement between a proposed caption's reduction and the original K08 commitment could reflect the caption being merely a draft/paraphrase, or an incorrect nonce transcription, or a transcription of the normalization rule. The original target is a one-way validation commitment. It supplies no direct independent test distinguishing those source-layer explanations. Currently the caption itself remains unquoted, so no accepted K08 phrase exists in the local materials even under the recorded nonce.

The six accepted *other* slots and their successful use of fields in the same route transcription provide useful broad consistency context. They do not authenticate the K08 nonce field specifically. Likewise, original draft captions N02 and N06 and excluded labels N17 and N18 fail the recorded nonce/commitment check, but that does not establish which words Emily finally wrote.

## Discriminating evidence standard

An independent original desk-nonce witness, such as a separately preserved commissioning record with provenance, could corroborate or refute the existing 16-byte key; an independently authenticated exact signed final caption is separately necessary. If either appears **within the permitted local case evidence**, test with the documented [caption checker](check_h17_caption.py) and the unchanged original slot commitment. Preserve its provenance alongside the normalized words. Only after K04 and K08 individually pass should the unchanged combined verifier be claimed to accept the archive.

No external mailbox/device/person was contacted, and no original source or acceptance commitment was modified. K08 and K04 remain null, six other slots pass, and combined acceptance remains incomplete.
