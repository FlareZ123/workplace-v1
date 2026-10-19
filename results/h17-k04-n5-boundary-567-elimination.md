# K04: closing the 160-bit p=567 CPython boundary and recovering one conditional seed-key bit at p=564

**Agent 50, 19 October 2026, ~14:16 UTC.** Source-conditioned new cracking constraints from the *five residual 160-bit initialized-seed phases* identified by Agent14. **K04/K08 remain MISSING**, all original acceptance inputs, selected printer row129 and original verifier withheld.

## Why these phases were genuinely untested

Agent14's 160-bit three-window solver eliminated p396..563; its cross-cycle extension eliminated p568..620 (for the source-aligned row34 absolute first-output index p). It explicitly left **p=564,565,566,567,621** unresolved because first-cycle MT wrap changes what the row10/41 pair inversions represent and the CPython initialization second-pass step at i=3 is exceptional.

This result treats the exact boundary instead of extrapolating either adjacent formula. It reuses source-pinned immutable initialized-state constraints: S[p−168..p−167] = `0A9DE247 FBBBB07E`, S[p−166].low31 = `2A07F662`, and S[p−1..p+2] = `6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`. These follow from original intact printer rows10/34/64, the separate row3/34 prefirst-twist construction and the conditional AX-7778 stream alignment. Original source hashes and reproducible derivations are pinned by the imported Agent14 scripts.

## Phase p=567: new exact rejection

Here intact row10 outputs lie at X397..400; row41 lies at X624..627, entirely in the second cycle. Inverting the four MT 227-step relations gives first-cycle X1..3, whose first-cycle twist against the known initialized words S399,S400 yields **S3 full = `F1A6234C`**, **S4.low31 = `2F1F9ABB`**, and **S2.high = 0**.

From the completely separate late initialized quartet at phase p567, CPython `init_by_array` reversibly determines the 32-bit five-word seed-array member **KEY[3] = `C021701B`**. The ordinary second-pass initialization update at **i=4** is invertible and valid even though the previous i=3 update crosses the exceptional first-loop boundary. For both possible unknown top bits of S4, invert that update to predict S2:

| S4 upper bit | Predicted full S2 | Independently observed S2 upper bit |
| --- | --- | --- |
| 0 | `9AA55A97` (upper bit 1) | **0** |
| 1 | `EF92B76C` (upper bit 1) | **0** |

**Neither branch agrees. Thus the original observations exclude the p=567 five-word CPython seeded-state hypothesis under the joined-source phase premise.** No seed enumeration or K04 hash test is used. This safely avoids applying the invalid exceptional i=3 inverse step.

## Phase p=564: a new *conditional* complete seed word

Here row41 outputs X621..624 straddle the first/second MT twist boundary. The first three 227-step inverse pairs from row10/41 yield fully observed **initialized S622 = `348ADB23`**, **S623 = `324EF3E1`**, and **S621.high=0**. The independently observed early initialized pair and S398.low31 constrain seed-array member **KEY[2].low31 = `1E2EBD55`**.

Reverse the ordinary state update at initialized index 623, once for each possible KEY[2] upper bit. The predictions for S621 are:

| KEY[2] upper bit | Predicted S621 | Consistent with original S621.high=0? |
| --- | --- | --- |
| 0 | `C8113B43` | No |
| 1 | `1CFE981A` | **Yes** |

Therefore phase p564, **if ultimately viable**, requires **KEY[2] = `9E2EBD55`**. This is one independently conditioned recovered initialized-seed bit, not a coupon bit. Phase564 is **not** eliminated; no claim is made about the remaining unknown key-array members.

## Reproducibility

[Read-only standalone test driver](../agents/agent50/k04_n5_boundary_564_567.py) imports Agent14's source-pinned seed/MT routines, reads only intact spool rows and AX transfer checkpoint context (not selected row129), and executes **32 actual `random.Random(160-bit seed)` positive controls per phase**, all passing. It independently confirms that the true initialized states and seed words survive the p564/p567 inversions, then performs the untouched original-source comparisons above. An independent locally implemented equivalent passed an additional 12 real-seeded p567 controls. The driver reads no K04 mask, REC8 commitment, nonce or original checker.

Other CPython seed-array lengths, differing stream-phase alignments, non-CPython generators and cache/offline stream production remain possible. Even the excluded five-word p567 case does **not** directly determine any K04 target bit. The original six slots continue to pass independently; K04/K08 unknown, combined recovery incomplete.

**Follow-up:** treat remaining conditional n5 first-cycle phases **564,565,566,621** as distinct twist-edge cases; at p564 propagate fixed KEY2 and independently source-derived S622/S623 into a high-confidence new initialized-state/known-key discriminator before attempting coupon bytes. At p565/566 the row10/41 inverse pairs straddle a different number of first-twist outputs. At p621 the former low31 observation after S623 represents first-cycle output X0 rather than a nonexistent initialized S624. Do not repeat p567 or its already established 32 synthetic controls.
