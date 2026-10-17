# H-17 all-file verbatim carrier search: K04 and K08

**Agent 14, 18 October 2026 (UTC).** **Outcome: NO_MATCH in two specified source-extraction classes.** Six other slots remain accepted. This does not recover K04 or K08, prove impossibility of recovery, or authenticate the absent original coupon/caption.

## Source and motivation

Prior work concentrated on the printer log's complete PAYLOAD fields and on selected Emily-authored notes. This independent audit broadens **source carriers**, rather than generating hypothetical repairs or natural-language paraphrases. It asks whether any of the 43 exported file members contain (a) the exact 16-byte K04 coupon payload somewhere in their bytes or literal hex text, or (b) the exact K08 caption as a contiguous run of words anywhere in a UTF-8-decodable source. It preserves the case's **original** reduction/commitment rules.

Inputs: the byte-identical 43-file local export under resources/ (the original ZIP equivalence audit is in [h17-export-equivalence.md](h17-export-equivalence.md)); resources/evidence/recovery-routing.json supplies the K04 XOR mask and K08 nonce; the unchanged resources/acceptance.json supplies full slot SHA-256 commitments. No independent case information, extra web source, changed evidence or modified verifier is used.

## Exhaustive class definitions

**K04 raw:** For every file, slide a 16-byte window by one byte through the complete original member bytes. XOR that candidate against the route's fixed 16-byte mask, then compare the 32-byte SHA-256 digest of the resulting component to the fixed K04 target.

**K04 ASCII hex:** Within every run of 32 or more ASCII hexadecimal characters in every file, slide a 32-character window by one character (permitting either nibble phase), decode to 16 bytes, and apply the same XOR and SHA-256 test. This includes the complete printer PAYLOAD fields and other source hexadecimal records.

**K08 UTF-8 text:** For each member that decodes as UTF-8, apply the route's ASCII normalization rule (lowercase; replace characters outside ASCII a-z, 0-9, and whitespace with spaces; collapse to normalized tokens). Test every contiguous span of **1 through 40 words** within that file. Compute HMAC-SHA-256 using the original decoded desk nonce, take its first 16 bytes, then compare that component's SHA-256 to the original K08 target. Search scopes are per file; no candidate concatenates words from separate files.

## Measured results

| Checked class | Exhaustive candidate assignments | Acceptance matches |
| --- | ---: | ---: |
| K04 16-byte sliding windows over all member bytes | 108,021 | 0 |
| K04 decoded 32-character sliding windows inside hex runs | 432 | 0 |
| K08 contiguous normalized 1–40-word spans across 42 UTF-8 files | 618,316 | 0 |

One non-UTF-8 member, evidence/recorder/trip-recorder.raw, is excluded from the **text** scan only; its raw bytes remain included in the K04 scan. The candidate counts describe assignments, which can duplicate values, and must not be interpreted as distinct missing original payloads or phrases.

**Positive controls:** with temporary synthetic commitments, the identical extraction/search implementation finds (i) the logged ACK attempt-2 hex payload A9A9DC5731A5E2AE879C47215C2559D5 in evidence/print/spool-reconstruction.log and (ii) the normalized 11-word N01 note fragment 'the sea looks different when you have finally finished your tea' in evidence/crew/noticeboard-and-desk-notes.txt. Both synthetic control hits are located by the search loops. The original acceptance commitments were **never replaced on disk**.

## Reproduce

Run [check_h17_all_carriers.py](check_h17_all_carriers.py) from a checkout with resources/, with the --self-test switch to exercise internal positive-control searches. It is read-only, has no third-party dependencies, and reports exact window/span counts and any matching source offsets. An unpacked ZIP folder can be passed with --root.

## Interpretation and boundaries

No accepted K04 coupon is embedded **verbatim** in any original member as either 16 consecutive raw bytes or a consecutive 32-nibble hex representation, within this scope. No accepted K08 caption is a **single contiguous normalized span of 1–40 words** in any UTF-8-decodable original file.

This does **not** exclude a K04 payload that was damaged, scrambled, encoded in a different representation, split into noncontiguous fragments, or absent from the trimmed export. It does **not** exclude a K08 caption paraphrased from notes, assembled across noncontiguous spans, longer than 40 words, or lost with Emily's desk margin. The K04 selected retained ACK still fails the acceptance target; the missing authenticated final K08 wording remains unquoted. The offline verifier should retain K04 and K08 as null. See [results synthesis](README.md) and [source-rule consistency](h17-source-rule-consistency.md).

This expands a finite class of **direct original-data carrier tests**; it is no substitute for an independently authenticated missing source or a genuine positive recovery witness.
