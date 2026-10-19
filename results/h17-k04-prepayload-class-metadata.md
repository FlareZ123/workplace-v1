# K04: source-reconstructed pre-payload states predict printer CLASS labels

**Agent 7, 19 October 2026, ~19:08 UTC.** New source-derived producer discriminator and conditional pruning rule for the missing coupon. **No selected coupon bytes, selected MT output bits, or K08 words have been recovered.** Original REC8 acceptance/checker, source records, mask are unchanged.

## New intact-source prediction

Untemper the original printer spool's four 32-bit payload words per row, automatically discover **25 exact MT19937 three-row recurrence witnesses** within the surviving regular chronology, and solve their consistent relative-index graph (14 distinct components). Middle and future intact source rows that are separated by precisely 227 state indices furnish adjacent reverse-twist fragments. Combined fragments directly reconstruct **X[s(row)-1]**, the whole untempered state word immediately preceding a specific row's four payload words. Selected row129's payload is excluded at parse time.

| Regular row | Source donor rows | Full original-source X[s-1] | Tempered upper3 | Recorded CLASS |
|---:|---|---|---:|---|
| 3 | 56, 86 | 482F6361 | **2** | RECOVER |
| 13 | 67, 97 | 8F878FB0 | **1** | STORES |
| 38 | 91, 121 | 820D840E | **2** | RECOVER |
| 45 | 98, 132 | B37E7885 | **1** | STORES |

Calibrate RECOVER→2 and STORES→1 on rows 3, 13 and 38, then predict withheld row45 CLASS **STORES**; it agrees. The exact row38 predecessor 820D840E and its RECOVER code2 were previously reported in the Agent11/38 node50 model-falsification. **The new observation is the cross-group calibration and row45 source prediction, plus the separate row44 test below.**

A fifth observation follows under the separately published 42-witness relative placement s97=s44+394, s130=s44+620. Then row97 words0..2 paired with row130 words1..3 independently reconstruct X[s44-1]=0ACF4761, tempered upper3 **1**, predicting row44 CLASS **STORES**, as observed. This conditional computation cannot independently prove the assumed group placement.

This suggests a candidate producer relation between CLASS and the preceding MT state. The export does not specify the classification implementation. The same five samples also fit a **top2** mapping RECOVER→1, STORES→0; no full predecessor for a LABEL row is yet recovered. A new independent LABEL predecessor or a STORES/RECOVER with divergent upper3 would discriminate competing coding rules. Do not assert a complete historical producer from five selected observations.

## New target-directed conditional discriminator

Earlier independent source placement has row128 at state position 623 and selected row129 at p=627..d+616, with d=11..65. At **p=627**, X[p-1] coincides with **original retained row128's final payload word** X[626]. The tempered high3 of that retained word is **5**, whereas the selected row129's recorded CLASS is RECOVER, provisionally encoded as **2** from the regular-row reconstruction. If the same direct preceding-state CLASS encoding and source-payload integrity apply to the recovery attempts, **p=627 contradicts the observed source metadata**.

This would exclude 55 out of the 1,540 (d,p) placements, including the much-studied d=11,p=627 donor-completion branch. The exclusion is expressly conditional, since special recovery attempts may be externally assigned RECOVER status rather than drawn using the regular metadata producer, and spool bytes have no independent checksum. The original 42-witness geometry itself is not falsified.

A separate stronger hypothesis that each recovery-tail row consumes **one distinct class draw before its payload** requires at least one skipped output on each side of row129, implying d>=13 and **1,431** admissible placements. This is also conditional and should never replace the verified original source constraints.

## Reproduction and next work

The new SHA-pinned, original-source-only standard-library [SFT](../agents/agent7/k04_class_boundary_sft.py) finds all 25 direct witnesses; checks index closure, obtains the four direct full predecessor states, computes the separate fifth conditional word, and evaluates the tail p=627 model discriminator without reading selected payload, K04/K08 commitments or mask. A locally equivalent implementation was executed against the supplied original 43-file case ZIP and passed its assertions.

**Highest-value next crack:** recover a source-indexed LABEL predecessor to resolve the top2/top3 ambiguity and identify whether the explicit tail RECOVER attempts reuse the ordinary classification producer. A separately corroborated rule could turn preserved metadata into target-relevant state constraints.

**Acceptance unchanged:** six slots PASS, K04/K08 MISSING; combined INCOMPLETE; accepted=false.
