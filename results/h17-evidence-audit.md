# H-17 REC8 provenance and evidence-sufficiency audit (Agent 7)

Date: 17 October 2026. Scope: the supplied export 06 and unchanged `resources/acceptance.json` / `resources/verify.py`. This is historical records recovery only. No facility equipment, remote mailbox, or operational service was accessed.

## Independent replay

I extracted the supplied ZIP, implemented a standard-library source-to-slot reader, and independently derived K01,K02,K03,K05,K06,K07. All six pass the original slot SHA-256 commitments; the supplied verifier reports 6 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false. Local canonical candidate is identical byte-for-byte to `results/h17-candidate.json`. The reusable repository script `results/replay_h17.py` reconstructs these fields directly from `resources/evidence/` and prints selection intermediates and the K04 rejection. It is read-only and does not change source evidence.

| Slot | Discriminator | Replayed intermediate |
| --- | --- | --- |
| K01 | Signed WN-14 ink sheet from mail 03/06, confirmed in 14 | A=049AAB2E; B=1CDE7A82; C=CD7C6023; D=4303C91A |
| K02 | LT-204 DIAG_WORD, GOOD/HOLD, 21:13:40–21:13:48 UTC, highest revision/seq | U16BE bytes E1A5E474BAD7E853A2E8C71D3317D507, revisions 2 at each seq |
| K03 | PTW-417 signed CLOSED AS_LEFT; witness order B,D,A,C | SG-D7DAD6BC\|SG-9714519B\|SG-7DAD0AD4\|SG-BE8E87FD; rev 2 each |
| K05 | TRP2 schema 2, archive node/event and time window, CRC32 | 88 records; 4 invalid CRC; latch sequences 300,301,302,303; words FF8B7820 0A56E858 6DCDA00E F01E4572 |
| K06 | Authorized RC-17 revision C and SERVICE_ORDER | DRAIN=5DBF40EE; ISOLATE=52FAAED9; PURGE=A536D332; VERIFY=6CF0D95A |
| K07 | Gabriel's AX-7782 receipt and non-dry-run COMMIT | Eight latest CHUNK attempts 2; checkpoints 8947CEDCB9CC73BAB7E87BE63302C5C9 |

## K04: traceability versus payload integrity

`evidence/archive-labels.ini` specifies incident-date logical ESC-N → `PS-261003-0417`. `mail/16.eml` specifies last ACK of the exact job. `print/spool-reconstruction.log` has RECOVER attempt 1 REQUESTED (18:01), attempt 2 ACK (18:02), attempt 3 REQUESTED (18:03); an earlier attempt 1 CLASS=LABEL is excluded. Payload at attempt 2 is `A9A9DC5731A5E2AE879C47215C2559D5`. XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C` yields candidate `2CFF149C50E54557228E7DE60B3EB7C9`, whose SHA-256 is `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`. Target K04 commitment is `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`. Thus NO_MATCH.

`records-custodian.txt` explicitly states spool payloads were not all independently validated, and ACK confirms dispatch receipt rather than recovered-byte integrity. No independently authenticated original coupon or checksum is provided. The mismatch leaves source corruption, missing evidence, or an unrecognized reduction ambiguity open. Earlier exhaustive bounded candidate-neighborhood searches in `results/h17-recovery.md` exclude their tested classes only.

**Chronology caveat (Agent 3):** `mail/16.eml` bears `2026-10-03 07:49 UTC` while it speaks in past tense about a later unacknowledged REQUESTED entry, which the identified spool job records at `2026-10-03 18:03 UTC`. That creates an apparent timing inconsistency unless the message was anticipatory or its timestamp/content was subsequently transcribed incorrectly. It does not establish which printer payload is correct, and the unchanged commitment remains decisive. Preserve this uncertainty rather than treating the email as independent contemporaneous verification of the later buffer data.

### Same-job byte-fragment mosaic (Agent 3, 17 October 2026)

The original spool log contains three `CLASS=RECOVER` payloads for exact job `PS-261003-0417`: attempts 1 (REQUESTED), 2 (ACK), and 3 (REQUESTED). If extraction inadvertently mixed bytes from those retained fragments, a source-constrained test is to select each of the 16 byte positions independently from one of the three corresponding attempt bytes. I enumerated all **3^16 = 43,046,721** distinct selection assignments (not necessarily distinct output strings where source bytes coincide), XORed each selected 16-byte payload with the original K04 mask, and SHA-256 checked the result against the unchanged K04 slot commitment. **NO_MATCH for every selection.** The reproducible OpenSSL C source is [`k04-byte-mosaic.c`](k04-byte-mosaic.c), with the three source payloads and unchanged expected hash embedded for exact replay.

This rules out the specified single-job, same-position three-attempt fragment-mixing hypothesis only. Neither unacknowledged attempt is automatically authentic; no broader byte corruption, missing media, or other spool reconstruction is excluded.
### Boundary slip of 1–3 bytes in the last-ACK payload (Agent 3)

The source identifies printer data as retained-fragment output without an independent checksum. A distinct corruption hypothesis is that its 16-byte reconstruction was shifted **left or right by 1, 2, or 3 whole bytes**. For a left slip, discard the first `k` recorded payload bytes and exhaustively append all possible `k`-byte suffixes; for a right slip, prepend all possible `k`-byte prefixes and discard the last `k` recorded bytes. For each construction, apply the unchanged XOR mask, compute the 16-byte slot SHA-256, and compare with original K04 commitment.

The six exact classes comprise `2 × (256 + 65,536 + 16,777,216) = 33,686,016` assignments. **Every one returned NO_MATCH.** The reproducible source is [`k04-slipscan.c`](k04-slipscan.c), using a single-block OpenSSL SHA-256 transform for speed. A positive control with an independently hashed two-byte left-slip and reconstructed suffix `1234` correctly returned `FOUND` before running the original unchanged target.

This excludes simple 1–3 whole-byte boundary slips with only the exposed retained payload bytes fixed. It does not exclude nonlinear reconstruction, multiple insertions/deletions, arbitrary damaged data, or missing original media.
## K08: authentic caption missing

`mail/11.eml` excludes commissioning caption “Back before the first boat” and standby caption “Leave the light on for the next watch”; `mail/20.eml` explicitly distinguishes Emily's final wording from preferred paraphrases. `crew/noticeboard-and-desk-notes.txt` offers draft captions N02 and N06, reflective descriptions N10, N13, N20, N23, and the excluded labels N17/N18. N23 refers to the words she *finally* put on the envelope but does not quote them. No surviving source in this export explicitly identifies a final caption with authoritative exact wording. The nonce and normalization/HMAC procedure test a proposed phrase; they do not recover unrestricted missing text. An authentication link from description/draft to final phrase is absent.

## Disposition

Retain K04 and K08 as JSON null. For K04, seek a verified original coupon, printer media/buffer copy with provenance or independent payload checksum. For K08, seek Emily's signed/final margin or desk-card photo, or a contemporaneous exact quotation. Rehash any newly supported bytes against unchanged `acceptance.json`, then test combined commitment. The six-slot evidence does not establish eight-slot recovery.

Local extracted case inventory SHA-256: `acceptance.json` = `681739241b757b471acca4c0fef9d9d97e9493883887736d5db3b92bfb0c137f`; `verify.py` = `01cedbfa08a28b388f8ab09b96c9c562a920d8ae9a7cc582ba3c79d138681cd0`.

## Additional bounded K08 draft-recombination tests (Agent 3, 17 October 2026)

To test whether the missing final wording was merely a *deletion or cut-and-paste reduction* of the surviving Emily notes, I exhaustively enumerated two defined classes using the original K08 HMAC/slot-SHA rule and unchanged target:

- All nonempty, original-order word subsequences of the cited sentence in N02, N06, N10, N13, and N20 (N20's first sentence only): **38,283,259** candidate phrases, no match. The code is [`k08-subsequence.c`](k08-subsequence.c), with separate runs for note IDs 2, 6, 10, 13, and 20; each phrase uses only words from that note.
- All pairs of contiguous word spans selected from **different** notes among the same five, concatenated in either note order with one of six fixed joiners (single space, `and`, `while`, `as`, `when`, `until`): **3,823,524** candidate phrases, no match. Reproducible read-only Python code: [`k08-two-spans.py`](k08-two-spans.py).

The exact cumulative tested count for these classes was **42,106,783**. This excludes only the enumerated deletion/recombination grammars; the caption could include original wording not in these notes, synonyms, a different word order, or other unpreserved material. These negative tests strengthen the conclusion that no verified phrase has been recovered; they do not prove that the correct phrase is impossible to reconstruct.
