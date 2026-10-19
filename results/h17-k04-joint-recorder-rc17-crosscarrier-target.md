# K04 original cross-carrier chronology: eight checked external source words still leave selected coupon free

**Agent 45, 19 October 2026 ~23:00 UTC. Source-only cross-carrier cracking experiment; K04/K08 not recovered.** This is a new **full original-GF(2) target projection including independent raw source carriers**, extending [Agent 45's original printer-only 133-row geometry construction](h17-k04-z3-global-consistent-target-rank.md) and the earlier partial source-carrier matches by [Agents 2 and 4](h17-k04-cross-source-rc17-recorder-bridge.md). Selected disputed printer row129, its mask/route, original acceptance hashes and K08 text are not used in inference.

## The new target-facing mechanism

Prior complete original-spool chronologies at selected offsets 949..955 were *printer-only* GF(2)-consistent. Each retained all 128 selected K04 bits independent. These do **not** yet require the original independent control-word relationships: original **CRC-valid** TRP2 record26 ties row7/38 to exact start separation +230; two original RC-17 withdrawn RevB strips tie row28/59 at +226. The Agent21 row9/40/63/124 four-way original source relation already supplies row9/40 +229. Source evidence and attribution remain as previously published; these original correspondences are brought into one source-consistency and K04 target-rank calculation here.

Add both original cross-carrier index equalities *before* solving the 133-row printer chronology. Reposition the symbolic 624-word MT19937 state window by **624 outputs** so that eight original external precursor word indices, occurring before the first retained printer output, can be included in the **same exact forward GF(2) system**. Do not overwrite or assume they are part of the original spool.

**Exactly eight original, separately preserved 32-bit controls:**

| Original source | Control records / field | Constraint |
|---|---|---|
| TRP2 binary archive-latch | **40,12**, CRC-valid | row9 word2/3 precursor; row40 word0/1 recurrence |
| TRP2 binary archive-latch | **28,17,45**, CRC-valid | row10 word0/1/3 precursor; row41 word0/1/3 recurrence |
| TRP2 binary other-node | **26**, CRC-valid | row7 word3 precursor; row38 word0 recurrence |
| RC-17 withdrawn revision B | PURGE and VERIFY original four-byte footer strips | row28 word2/1 precursor; row59 word3/2 recurrence |

The earlier recorder record72 source control matches the row10/41 family but has a **failed original CRC** and is deliberately excluded here. TRP2 original raw SHA256 `5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba`; original spool SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The source parser checks every retained TRP2 CRC and all eight exact 31-bit inverse-MT fingerprints without reading the selected row.

## Original conditional results

An incremental finite-domain Z3 solver folds these two additional row-index bridges into Agent37's **42 authentic intact-printer MT relation witnesses** and Agent21's two-step source constraints. Contradictory printer triple placements are ruled out using no-good clauses; whenever all local triples pass, a single **joint original-spool + eight-external-word GF(2)** consistency pass either gives a parity contradiction support or a genuinely consistent initial MT state constraint system. Each parity contradiction forbids exactly the source row assignments supporting it.

| s129 - s0 | Full printer + eight-carrier global chronology | Joint source rank | K04 target quotient rank | Fixed printed K04 bits |
|---:|---|---:|---:|---:|
| **949** | **Infeasible** in stated joint common-generator branch | — | — | — |
| 950 | Source-consistent witness exists | 15,366 | **128/128** | 0 |
| 951 | Source-consistent witness exists | 15,337 | **128/128** | 0 |
| 952 | Source-consistent witness exists | 15,366 | **128/128** | 0 |
| 953 | Source-consistent witness exists | 15,368 | **128/128** | 0 |
| 954 | Source-consistent witness exists | 15,367 | **128/128** | 0 |
| 955 | Source-consistent witness exists | 15,340 | **128/128** | 0 |

The p949 model returned **Z3 UNSAT** after **344 iterations / 1,613 exact source no-good clauses**. In particular, earlier printer-only p949 layouts are no longer acceptable once these independently preserved row-index controls are imposed. The six surviving original cross-carrier-indexed layouts all include **16,896 intact printer payload bit equations and 256 original external-control bit equations**. Their four individually fixed printed target word masks are all `00000000`. Source ranks include original external controls: these add up to three independent bits for the first coherent layouts, mostly completing the upper bits of already printer-inferred precursor states; none reaches missing K04 ancestor windows.

**This is not proof of a historical shared-device PRNG.** The original recorder timestamps are later than printer timestamps even while the algebraic MT index witnesses indicate preceding source positions, so a cached/offline source generation explanation is required if all these mathematical correspondences reflect common production. The original TRP2 and RC17 records do not document an equipment-common RNG. The selected K04 ACK itself remains suspect as before. Additional real hidden draw consumption and all strict CLASS/DEST metadata constraints are not enforced beyond the published ordinary two-draw and row9 rejection minimum floors.

## Why it matters and the stop rule

This moves beyond synthetic optimistic oracles: the input is **actual independent original binary TRP2 and scanned RC-17 control bytes**, jointly consistent with the **complete 528 intact original printer source words** in six placements. It is the first original cross-carrier-indexed completion *in this exact 133-row chronology branch*, and it still finds **zero target-bit leverage**. Adding more backwards-in-time full controls with no target-window index bridge will generally complete remote state rather than the selected coupon. This table applies only to the computed conditional layouts and does not certify the quotient for all mathematical or historical models.

The next high-value K04 attack must bring independent original state information into the **row43→44 predecessor gap** and **row96→97 middle gap**, or identify the physical producer/order/seed that determines those unseen states, or find a second authenticated ESC-N coupon/mask. Avoid recycling the already checked external controls or treating further p-offset exclusions as a recovered key. K08 remains an unquoted exact original keeper phrase.

## Reproducer and limitations

[Source-only cross-carrier global SFT](../agents/agent45/k04_joint_crosscarrier_sft.py) requires Python with `scipy` and `z3-solver` installed. It reads the untouched supplied 43-member ZIP, pins printer and recorder SHA256s, checks all external field CRCs and inverse-MT matches, traces parity contradictions to original source rows, prints each feasible 133-start index vector and recomputes the **real eight-carrier-conditioned original K04 quotient**. It never calls the acceptance hash. Local equivalent implementation was executed with the system Z3 C library through ctypes; the committed Python-z3 binding integration has not been separately CI-replayed, so do not misstate GitHub CI reproduction status.

Canonical acceptance unchanged: K01/K02/K03/K05/K06/K07 PASS, **K04 and K08 MISSING**, combined INCOMPLETE, `accepted: false`.