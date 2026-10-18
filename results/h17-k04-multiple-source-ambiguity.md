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

## Bounded local test: verbatim alternate mask carriers

**Hypothesis and provenance gate.** Because the retained mask is a transcription, one conceivable local recovery mechanism is that an independent original 16-byte mask is still present verbatim in a different exported member, while the selected printer payload is correct. Such a hit would require *separate contextual authentication* as a genuine historical mask; the hash alone would not grant provenance. A literal byte or hex representation predicts a specific testable accepted component.

**Deterministic test.** Hold the source-selected RECOVER attempt-2 payload fixed at `A9A9DC5731A5E2AE879C47215C2559D5`. Treat every 16-byte sliding window of the original 43 files as a possible replacement mask; separately decode every 32-hex-character sliding window within runs of ASCII hexadecimal characters. For each mask `M_candidate`, compare `SHA256(P_observed XOR M_candidate)` with the **untouched original** K04 commitment. The [read-only reproducer](check_h17_k04_alternate_mask_carriers.py) obtains the selected payload, route and target from original resources.

**Result:** 108,021 raw byte-window assignments and 432 hex-text-window assignments, **zero original K04 commitment matches**. A synthetic raw control using the first 16 bytes of `START_HERE.md` and a synthetic hex control using the literal route-sheet mask each produced the expected hit through the same scanner (one each). These are assignment counts and can include equivalent byte strings.

**Interpretation:** under the explicit assumption that the ACK-selected payload is intact and that an alternative mask exists verbatim as a contiguous 16-byte raw or 32-nibble ASCII-hex sequence in the preserved 43 files, that hypothesis is excluded. This is not evidence that the transcribed mask is correct, does not test structured or noncontiguous original masks, and does not turn some other file into an authorized mask source. It leaves the source-layer non-identifiability and incomplete six-of-eight status unchanged. This scope is the *mask-side dual* of the fixed-mask all-file payload scan in [the original carrier audit](h17-all-file-carrier-bound.md), and is not a general preimage search.

## XOR symmetry: correction bounds also apply to an alternate mask

The independent [minimum-correction-footprint synthesis](h17-k04-minimum-correction-footprint.md) established necessary conditions for any 16-byte K04 value matching the original SHA256 commitment relative to the currently derived baseline `K0 = P0 XOR M0`: at least **three different bytes, four different hexadecimal nibbles, seven different bits, and a changed-byte span of five or more positions**. These are bounds on mathematical candidate differences; they do not diagnose the source.

The symmetry extends those bounds to a **single-layer correction** on either side of XOR:

- If mask `M0` is correct and the authentic payload is `P1`, then `K1 XOR K0 = P1 XOR P0`.
- If selected payload `P0` is correct and the authentic mask is `M1`, then `K1 XOR K0 = M1 XOR M0`.

In each scenario, XOR with the held-fixed 16-byte value preserves every changed bit, nibble and byte position. Therefore an accepted **payload-only** correction and an accepted **mask-only** correction would each need to exceed all the same lower bounds. In particular, a one-character typo in the 32-nibble printed mask is excluded, as is any mask amendment confined entirely within four consecutive bytes. This is an algebraic transfer of previously validated negative-search scopes, **not** a new 16-byte preimage search or evidence that either proposed correction occurred.

If *both* payload and mask are wrong, their differences may cancel or combine, and no individual source-layer minimum follows from these bounds. If the actual job/attempt differs, the geometric comparison has no necessary provenance interpretation.

### Joint-mask-and-payload correction bound

The same algebra constrains **combined** source edits. If `ΔP = P1 XOR P0` and `ΔM = M1 XOR M0`, then `K1 XOR K0 = ΔP XOR ΔM`. Because bitwise XOR can cancel changed positions, the combined output change has **at most** the sum of the source-layer changes, and every changed output position must belong to the union of positions changed in one or both inputs.

Consequently, assuming the original 16-byte XOR reduction and the observed `P0/M0` baseline:

- At least **seven bit changes total across both sources** are necessary. Two possible source errors of at most three bit changes each cannot suffice.
- At least **four changed nibble occurrences total** and **three changed byte occurrences total** across both sources are necessary. These are counts of changed positions *per source layer*; positions changed in both may cancel in the output.
- The **union** of byte indices changed in one or both sources must span at least **five consecutive positions**. Any corrections to both sources restricted to the same contiguous four-byte region are excluded.

These conditions follow from the component footprint bounds and containment properties of XOR, without new hashing work. They leave open large, dispersed, source-supported corrections and changes to the selected job/attempt. The true source differences, if any, have not been established.
