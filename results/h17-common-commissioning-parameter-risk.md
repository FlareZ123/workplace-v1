# Shared bottleneck: unauthenticated commissioning parameters for both missing slots

**Agent 23, 18 October 2026. Status: six original commitments pass; K04 and K08 remain unresolved.** This is a cross-slot dependency synthesis of [K04 multi-source ambiguity](h17-k04-multiple-source-ambiguity.md) and [K08 nonce provenance](h17-k08-nonce-single-source-provenance.md). It is a source-authentication model, not a proposed recovered component.

## Observed anchors

The custodian calls `evidence/recovery-routing.json` a **transcription** of commissioning reduction rules. Both missing components depend on distinct 16-byte fields in that single original exported document:

| Missing slot | Recorded parameter in that source | Other necessary evidence | Computation |
| --- | --- | --- | --- |
| K04 | `masked_component = 8556C8CB6140A7F9A5123AC7571BEE1C` | Authentic incident ESC-N `RECOVER` payload and correct dated route/ACK selection | 16-byte XOR, then SHA256 slot commitment |
| K08 | `desk_nonce = 5F933DA6A1BD03C32DA5CBC25344F497` and normalization rule | Authentic exact final keeper-caption words | Normalized-caption HMAC-SHA256, first16, then SHA256 slot commitment |

The K04 mask and K08 nonce each occur verbatim in only that routing transcription across all 43 original ZIP member files, when searched as complete uppercase/lowercase 32-nibble hex strings and raw 16-byte strings. Those direct-occurrence checks do **not** prove no other encoded historical witness exists. Neither field is independently validated by a second retained original commissioning sheet.

The K04 source-selected ACK bytes fail K04. The original K08 words are not quoted, so the recorded HMAC path cannot currently reconstruct that component. The first six accepted slots remain strong controls for **their own** routed reductions; their successful hashes cannot certify unrelated individual parameter digits.

## Common evidence failure mode

Both slots have two distinct dependencies: **historical payload/caption authenticity** and **commissioning parameter authenticity**. The unchanged acceptance commitment validates the final 16-byte *result*, but cannot localize a mismatch between the two evidence layers. Treating the XOR mask and HMAC nonce as infallible merely because they appear in a readable routing JSON file can prematurely blame retained media or caption wording. Conversely, unique occurrence does not establish that either parameter is corrupted.

An independent original commissioning page or another locally supported exact mask/nonce witness could test this shared weak point for both unresolved slots at once. A trustworthy original ESC-N coupon or signed final caption would test the remaining, distinct inputs. The discriminating prediction is direct agreement/disagreement on a parameter's complete 16 bytes from an independently authenticated source, before testing a candidate through the original unmodified commitment. A “different parameter” invented to force a match is not evidence.

**Case scope boundary:** `START_HERE.md` forbids collecting external records, contacting devices or people; these witness descriptions are conditions for assessing *new local evidence*, not instructions to leave the preservation export.

## Disposition

No missing component is promoted. The original `results/h17-candidate.json` retains null for K04 and K08; the original `resources/verify.py` remains 6 PASS, 2 MISSING, combined INCOMPLETE, accepted false. A complete recovery requires original-source-provenanced values for both slots that pass each unchanged slot check and then the combined check. Prioritize any locally observed independent commissioning-rule witness over a new unguided search of hypothetical repairs.
