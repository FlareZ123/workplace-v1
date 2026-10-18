# H-17 mail provenance: one uniform UTC header shift is falsified

**Agent 22, 18 October 2026.** This is a **conditional source-model falsification**, with no new recovery component. It concerns the already-noted anomalies in mail 13/16; the unchanged acceptance status remains six PASS, K04/K08 MISSING, combined INCOMPLETE. It does not imply all email header dates are reliable or that any spool bytes are repaired.

## Hypothesis

A single constant offset Δ applied equally to all mail `Date:` headers would explain why some mail describes later entries in the independent event logs. To give this hypothesis a discriminating source-side test, assume:

1. The mail/13 claim that AX-7782 is the actual final retained custodian handoff was made no earlier than the AX-7782 non-dry-run COMMIT receipt.
2. The mail/16 claim that the later RECOVER attempt was only REQUESTED and never acknowledged was made no earlier than that exact-job REQUESTED record.
3. Mail/20 was sent before the original bundle's stated preparation, because it is already included in that bundle.
4. The timestamp `Prepared: 4 October 2026, 11:40 UTC` in `START_HERE.md`, the two event-log times, and the common mail Date offset are trustworthy for this *hypothesis*. This is a test assumption, not an independently established custody guarantee.

## Original-source observations and arithmetic

| Event | Recorded timestamp (UTC) | Constraint on Δ |
| --- | --- | --- |
| mail/13 header | 2026-10-02 09:56:00 | Δ at least 34h 59m 10s to follow AX-7782 COMMIT |
| AX-7782 actual non-dry-run COMMIT | 2026-10-03 20:55:10 | `transfer-audit.jsonl` |
| mail/16 header | 2026-10-03 07:49:00 | Δ at least 10h 14m to follow request |
| PS-261003-0417 RECOVER attempt 3, REQUESTED | 2026-10-03 18:03:00 | `spool-reconstruction.log` |
| mail/20 header | 2026-10-04 11:06:00 | Δ no more than 34m to precede preparation |
| Original bundle preparation | 2026-10-04 11:40:00 | `START_HERE.md` |

Under the stated model, the lower bound is **34 hours 59 minutes 10 seconds** and upper bound **34 minutes**. Their intersection is empty; one shared Date-header clock correction cannot make the three email claims simultaneously retrospective and preserve their inclusion in the prepared export.

[Read-only standard-library reproduction](check_h17_uniform_mail_offset.py) parses the original repository `resources/` messages, COMMIT receipt, printer attempt and bundle header; it asserts the bound contradiction and passes a synthetic in-memory *reconcilable chronology* positive control. It does not change evidence.

## Interpretation and limits

This rejects **only the common constant mail-Date offset model subject to the enumerated historical assumptions**. It does not establish that all mail is forged or backdated. For example, the claims may have been anticipatory, individual messages may have been corrected, or original records may be inaccurate. The original material does not select among those alternatives. Neither does a clock correction by itself authorize changing the explicit incident-date ESC-N route or the selected ACK bytes.

Prior reports already document the separate timing discrepancies: [K04 source-rule certificate](h17-source-rule-consistency.md) and [cross-slot chronology control](h17-chronology-cross-slot-control.md). This focused result adds a falsification of one proposed **shared** correction mechanism. No accepted K04 payload or verbatim K08 caption emerges, and the central six-slot candidate remains unchanged.
