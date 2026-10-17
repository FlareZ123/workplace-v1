# H-17 source-rule consistency certificate and intake gate

**Agent 11, 17 October 2026.** This is an independent replay of the supplied 43-member local export, without modifying the case evidence or the original acceptance checker. It deliberately separates documentary selection, derived bytes, accepted values, and unproven repair hypotheses. Six accepted components remain K01/K02/K03/K05/K06/K07; K04/K08 remain null.

## K04: unique documented reduction and contradiction

The incident-date printer route is explicit in `resources/evidence/archive-labels.ini`: ESC-N = `PS-261003-0417`. `mail/16.eml` selects the last ACK for that exact job and disclaims ACK as an integrity certificate for the retained buffer. `spool-reconstruction.log` records:

| UTC, 3 Oct 2026 | Class | Attempt | State | Meaning |
|---|---|---:|---|---|
| 16:45 | LABEL | 1 | ACK | Earlier different-class entry; not the last ACK |
| 18:01 | RECOVER | 1 | REQUESTED | Unacknowledged |
| 18:02 | RECOVER | 2 | ACK | **Selected by the written rule** |
| 18:03 | RECOVER | 3 | REQUESTED | Unacknowledged |

For the selected attempt:

- Retained payload: `A9A9DC5731A5E2AE879C47215C2559D5`.
- Written XOR mask: `8556C8CB6140A7F9A5123AC7571BEE1C`.
- Deterministic output: `2CFF149C50E54557228E7DE60B3EB7C9`.
- SHA256(output): `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`.
- Original K04 commitment: `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

**Observed result: NO_MATCH.** This establishes an inconsistency between literal execution of the recorded K04 source-reduction rule and acceptance of that resulting component, conditioned on the printed transcription being accurate. It establishes neither the correct missing bytes nor a specific corruption mechanism.

As a secondary closed-corpus check, a separate read-only replay extracted all **133** complete 16-byte PAYLOAD fields in the supplied spool log (52 LABEL, 41 STORES, 40 RECOVER). For each, it applied the **same original XOR mask** and compared the component SHA256 with the untouched K04 target: **0 matches**. Thus simply choosing another complete retained spool field cannot satisfy the original rule. This check does not cover reconstruction from damaged fragments, nontrivial transforms or unavailable original media. Independent related tests are documented in [the provenance audit](h17-evidence-audit.md).

### Chronology is an evidentiary limitation, not a corrective rule

The `mail/16.eml` Date header is **2026-10-03 07:49 UTC**, while its discussion of the "later REQUESTED entry" corresponds to a spool record timed **18:03 UTC** the same day (10 h 14 m after the header). The ACK was 10 h 13 m after the email timestamp. The records supply no authenticated correction for the email clock, header, spool timestamps or historical order. This makes the email a questionable *contemporaneous independent witness* for the later printer event; its text nevertheless states the selection rule. Do not silently shift timestamps or infer a different payload from this anomaly.

## K08: a valid validator without an authenticated value

The signed keeper caption is described in `mail/11.eml`, `mail/20.eml`, and `crew/noticeboard-and-desk-notes.txt`; none quotes and identifies the final chosen words as an authenticated final caption. N02/N06 are drafts, N17 is standby, N18 is commissioning, and N23 points to missing final words in a desk margin. Exact normalization and HMAC derive a verifiable 16-byte component **only after** a candidate phrase is specified. No available text asserts the final phrase verbatim.

A large negative phrase search changes no provenance: a guessed phrase with a valid hash would be an accepted mathematical component, but the local record as currently preserved cannot specify one deterministically. Prior bounded scans are in [the K08 coverage report](h17-k08-textual-coverage.md).

## Permitted local-carrier scope

The independently examined supplied ZIP contains 43 files and matches repository `resources/` byte-for-byte according to [the blob audit](h17-export-equivalence.md). [The ZIP audit](h17-secondary-evidence-audit.md) found no ordinary ZIP comments, inter-record gaps, trailer or nonzero DEFLATE padding bits. The separate normal-agent check by Agent 10 found `private/` contains only `.gitkeep` and original evidence files had no intervening repository revisions. No relevant source file outside the 43-member evidence set was thereby demonstrated.

This is **negative coverage evidence**, not a proof that all possible hidden encodings or reconstruction procedures are impossible. The custodian expressly calls the export trimmed and payload integrity unverified.

## Decision gate for subsequent research

Promote K04 from null only after: (1) a source-supported correction or new exact original coupon/buffer, (2) a reproducible reduction using the unchanged XOR mask, and (3) a K04 slot hash PASS. For K08 require an independently sourced exact caption, or explicitly label a phrase as only a hash-accepted guess until provenance is resolved. Once both pass, rerun the unmodified eight-slot verifier and require combined PASS and accepted true.

Reject a new brute-force family unless its candidate grammar is anchored in an observed source feature and has a specific falsifiable mechanism. Neither the 133-source check nor the time anomaly licenses altering source files, commitments or verifier.

**Current measured outcome:** 6 individual PASS, K04 and K08 MISSING, combined INCOMPLETE, accepted false. See [reproducible source-to-slot reader](replay_h17.py) and [canonical candidate](h17-candidate.json).
