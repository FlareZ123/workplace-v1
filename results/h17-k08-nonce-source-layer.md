# K08: independent witness gap for the transcribed desk nonce

**Agent 5, 18 October 2026 UTC.** A source-layer sufficiency audit, **not a recovered K08 value**. The original six components still pass, K04 and K08 are unresolved, and the original combined checker remains incomplete.

## Primary-record evidence

1. `resources/evidence/records-custodian.txt` explicitly identifies the route sheet as a **transcription** of commissioning reduction rules. It appoints the original acceptance commitments as the final authority on proposed component bytes.
2. `resources/evidence/recovery-routing.json` gives K08 nonce `5F933DA6A1BD03C32DA5CBC25344F497`, ASCII normalization, and the HMAC-SHA256 truncation rule. In the **original 43-member ZIP**, this complete 32-character hexadecimal nonce occurs **once**, in this route file. A bytewise census of the same 43 members found **zero** occurrences of those 16 decoded nonce bytes as contiguous raw bytes.
3. `resources/evidence/mail/20.eml` says the normalization rule and desk nonce are on the route sheet, **without quoting their exact bytes or syntax**. That corroborates the existence and location of a rule, not its exact literal value. `mail/11.eml` and `crew/noticeboard-and-desk-notes.txt` N23 refer to Emily's chosen personal caption or final margin without quoting the final words. The quoted N02/N06 drafts and N17/N18 alternate-envelope labels fail the existing original K08 commitment tests.

The census used the **unchanged** 43-member archive (SHA-256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`), a case-insensitive literal search for the 32 hex characters, and an exact raw 16-byte search in every member. It makes a **verbatim-carrier** claim only. An unknown encoded nonce, missing historical original, or merely partial representation cannot be excluded by this test.

## What the original acceptance check can establish

For exact historical caption `P`, historical nonce `N` and historical normalization rule `R`, the stated reduction is

`K08 = HMAC_SHA256(N, normalize_R(P))[0:16]`,

followed by comparison of `SHA256(K08)` to original `acceptance.json` K08 commitment `285eb6b4196d21eaf47e251449e61e0bce28749881ccc5a065ca733b0c3fd747`.

The provided record contains an **observed transcription** of `N` and `R`, with no independent byte-for-byte witness for either, and descriptions/drafts rather than an exact identified `P`. Therefore a future historically authenticated final phrase that fails the recorded nonce/rule check would reveal an inconsistency but **would not, from that failure alone, identify the faulty layer**. Plausible alternatives include misidentified exact phrase, incorrect route transcription of nonce, incorrect rule transcription, or a combination. This does **not** assert any such error happened. The route may be perfectly correct; no competing nonce or revised reduction is promoted.

The original untouched verifier's acceptance standard is separate: **all eight slot SHA-256 commitments PASS, combined SHA-256 PASS, and `accepted: true`**. A candidate that passes those checks is computationally accepted even if an independent historical source for the personal caption/nonce is unavailable. An unconfirmed historical source attribution requires its own evidence.

## Falsifiable next-source questions

- **Nonce transcription:** A separate locally preserved contemporaneous nonce/rule witness, if one is identified, predicts an exact literal comparison with the recorded `desk_nonce` and normalization. The currently checked export has no second verbatim instance of the nonce.
- **Final caption:** A locally authenticated verbatim final margin or equivalent contemporary quotation would determine normalized words. Then a deterministic K08 derivation can be attempted with the recorded rule, and the untouched commitment tested.
- **Layer disagreement:** If such independent witnesses ever conflict, report which layer differs before testing source-backed alternatives. Do not infer an arbitrary replacement nonce or caption from a failed hash alone.

This source-quality observation complements [the K08 textual source audit](h17-k08-textual-coverage.md) and [the K04 multi-layer ambiguity analysis](h17-k04-multiple-source-ambiguity.md). It introduces **no new candidate, no recovered historical quotation, and no relaxation of REC8 acceptance**. Original case material, commitments, and verifier were left unchanged.
