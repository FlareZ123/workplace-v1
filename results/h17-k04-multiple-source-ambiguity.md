# K04: independent source-authentication layers and non-identifiability

**Agent 35, 18 October 2026. Result:** no additional K04 value or accepted key. This note narrows what can legitimately be concluded from the existing K04 rejection. It is a source-model clarification, not a new candidate search.

## Three source assertions are independently needed

The literal K04 reduction uses three distinct reported inputs:

1. **Rule and mask.** `resources/evidence/recovery-routing.json` is the custodian's *transcription* of commissioning rules; its sole `masked_component` field is `8556C8CB6140A7F9A5123AC7571BEE1C`. In the 43-member original export, this entire hex value occurs only in this routing file. There is no second retained copy that independently authenticates its digits.
2. **Logical route mapping.** `resources/evidence/archive-labels.ini` calls itself a label *transcription* and maps incident-date ESC-N to `PS-261003-0417`. `mail/16.eml` independently describes ESC-N as the north coupon and describes the selection rule, but it does not reproduce the job ID as an independent contemporaneous receipt.
3. **Selected payload.** `resources/evidence/print/spool-reconstruction.log` contains the selected 18:02Z, RECOVER-class, attempt-2 ACK payload `A9A9DC5731A5E2AE879C47215C2559D5`. `mail/16.eml` and `records-custodian.txt` explicitly warn that dispatch ACK authenticates neither every retained payload byte nor the reconstructed media. `mail/16.eml` itself is timestamped 07:49Z yet refers to a later request recorded at 18:03Z. This is a chronology limitation, not a basis to amend data.

The last reported ACK XOR the *reported* mask yields
`2CFF149C50E54557228E7DE60B3EB7C9`. SHA-256 of those 16 bytes is
`11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`,
while the unchanged K04 commitment is
`930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.
The literal retained reduction therefore **fails**, exactly as reported in [the source-rule certificate](h17-source-rule-consistency.md). This does not isolate the error to the spool.

## Why the commitment cannot diagnose the faulty layer

Let `P` be the genuine historical RECOVER payload, `M` the genuine historical mask, and `K = P XOR M`. The acceptance file contains only `SHA256(K)`. With `P_observed` and `M_observed` inconsistent with that commitment, several distinct mechanisms remain observationally indistinguishable:

- historical `M_observed` correct, printer reconstruction `P_observed` damaged;
- historical `P_observed` correct, mask transcribed incorrectly;
- mapping or selection evidence incorrect, yielding a different original payload;
- some combination of source errors.

For any unknown acceptance-consistent 16-byte value `K`, both `P = K XOR M_observed` and `M = K XOR P_observed` satisfy the XOR equation. The supplied hash permits verification of a proposed `K` but supplies neither its preimage nor a diagnosis of which observed source is faulty. Exhaustively rejecting every alternate complete spool payload with the same reported mask does not falsify a wrong-mask model, and does not authenticate the route mapping.

This is **structural non-identifiability of error location conditional on the stated evidence**. It does not establish actual corruption, an alternate mask, or a recoverable hidden carrier.

## Source-model gate for new work

| Model to test | Original observed anchor | Required discriminating evidence |
| --- | --- | --- |
| Reconstructed payload damaged | Printer's explicit retained-fragment/integrity warnings | Independently source-supported payload integrity invariant, or an authenticated local copy of the selected coupon |
| Mask transcription damaged | Custodian calls the route sheet a transcription; mask appears in that one file | An independent original rule/mask witness or a documented correction mechanism, not target-conditioned guessing |
| Job mapping/selection damaged | Dated labels transcription; same-job reused `LABEL`/ `RECOVER` ID; mail/16 chronology | Original mapping/dispatch evidence discriminating among different job and class identities |

The original assignment limits this investigation to the retained local export, so the witness conditions above are **tests of evidence sufficiency**, not instructions to reach external devices, people or mailboxes. The current file set supplies no independently authenticated correction in these categories. All six other canonical slots remain accepted, and K04/K08 remain null. See [source sufficiency matrix](h17-source-sufficiency-matrix.md) for the broader case assessment.

**Research implication:** Do not interpret a K04 NO_MATCH as proof that the correct XOR mask was already authenticated and only the printer bytes can be wrong. A new K04 candidate must state *which source assertion it revises and why*, then pass the original unmodified K04 commitment.
