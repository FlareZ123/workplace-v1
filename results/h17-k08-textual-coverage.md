# H-17 K08: source coverage and explicit desk-caption tests

**Agent 4, 17 October 2026.** This source review targets the remaining keeper phrase, independently of K04. It does not supply a new authenticated caption. K08 remains null.

## Surviving source coverage

The 43-file export contains 20 mail messages, each MIME type text/plain and none multipart; the messages have no embedded attachments. The export includes no retained photograph or other image file despite crew-note references to photographs. ZIP archive comment, member comments, and member extra-field metadata are empty, and the archive has neither prefixed nor trailing bytes outside its ZIP structure. This rules out several places an overlooked local caption might have been preserved in this particular file set. It says nothing about the inaccessible original mailboxes, paper margins, photographs, or omitted export material.

Key source links:

- **mail/11.eml:** Emily explicitly rejects commissioning and standby envelope labels and describes a final phrase about people making room after a long watch, with water outside and night nearing its end.
- **crew/noticeboard-and-desk-notes.txt:** N02 is a first draft; N06 is a second desk draft; N17 and N18 are excluded envelope labels. N10, N13 and N20 describe themes. N23 refers to words in Emily's margin that were finally placed on the envelope, without quoting those words.
- **mail/20.eml:** Gabriel warns that plausible paraphrases do not establish the exact chosen wording and confirms the preserved bundle was trimmed.
- **records-custodian.txt:** The absence of a gap marker does not certify completeness; the phrase is a keeper's personal caption, distinct from the other two envelopes.

## Explicit source-wording rejection tests

For each quoted N02/N06/N17/N18 line, take the phrase after its explanatory colon; apply the K08 normalization in recovery-routing.json (lowercase ASCII letters/digits/whitespace, punctuation replaced with spaces, collapsed whitespace); compute HMAC-SHA256 using the provided desk nonce and take the first 16 bytes. Compare SHA-256 of those 16 bytes with the unchanged K08 slot commitment in acceptance.json. This is the same rule used by the existing read-only caption checker.

| Source | Normalized exact line | Derived 16-byte component | Commitment |
|---|---|---|---|
| N02 first draft | a good watch leaves the room ready for the next pair of hands | BF889359B0303F2B2B2FD96AE841210B | NO_MATCH |
| N06 second draft | the little lamp stays on until the corridor has gone quiet | 0C3B326D0324BF93F55D4A3EEAB26CDE | NO_MATCH |
| N17 standby label | leave the light on for the next watch | F020BA8A3084A95B56EB4E6DBCCAE7F6 | NO_MATCH |
| N18 commissioning label | back before the first boat | A3100AE1ABB9C8D58315D9EBF326978B | NO_MATCH |

These are source-identified phrases rather than reconstructed final wording. Their rejection confirms four plausible decoys are inconsistent with the commitment; it cannot exclude an unobserved phrase. The earlier [broad span check](h17-recovery.md) tested many contiguous textual spans and also found no hit, under that test's defined candidate class.

## Disposition

The published nonce and nested HMAC/SHA-256 checks authenticate a proposed exact normalized phrase; they do not yield that phrase from a description. An original signed margin, desk/envelope image or verbatim contemporaneous quotation would be needed to establish final wording. Keep K08 null; retain the six accepted components and preserve the original commitments. No facility equipment or external communications were accessed for this test.

## Separate desk-note custody from signed register custody (Agent 25, 18 October)

`evidence/mail/14.eml` (2 October, 14:38 UTC) authenticates the WN-14 ink groups for K01 and separately states that Emily's **desk notes were placed under the folder rather than inside the controlled-copy sleeve**. David explicitly kept the photographs and galley captions from being filed as engineering-procedure pages. That is a source-backed custody distinction: the existence and proximity of desk material do not transfer the signed WN-14 copy's evidentiary status to the personal wording used for K08. It is compatible with an omitted or unpreserved final desk-margin original, but it does **not** prove when or how the final margin was lost.

Cross-check `evidence/crew/noticeboard-and-desk-notes.txt` N23, which acknowledges final words in Emily's margin without quoting them, and `mail/20.eml`, which notes that bundle 06 is trimmed and warns against replacing exact chosen words with plausible paraphrases. The surviving export has a notes **transcription** and contextual statements rather than the signed or photographed final margin itself. The unchanged K08 original commitment remains unfulfilled. This is a provenance observation, not a new phrase or candidate family.
