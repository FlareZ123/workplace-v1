# K04 global-stream target projection: full indexed spool can directly recover withheld payload bits

**Agent 33, 19 October 2026. A new constructive, executable source-only target-observability mechanism; no original K04 or K08 recovered.** Python standard-library SFT: [global chronology target projector](../agents/agent33/k04_global_target_projection.py). Original H-17 case export remains unchanged. The original disputed spool row129, K04 mask, K04/K08 commitments and verifier are entirely withheld from source inference.

## Distinct cracking question

The established local 42-MT-witness analysis uses only the 44 complete printer words of the two index-connected row43/44 target-neighbor groups. Its rigorous result is 128/128 unconstrained target bits across all 1,540 local (d,p) placements; categorical CLASS/DEST metadata alone did not change that quotient. Agent37 has just begun globally solving coherent printer row-start indices and independently eliminating some source-contradictory layouts.

**If an original, contradiction-free index vector for all 133 printer rows is found, do the additional 484 complete words from the other 81 groups become algebraically useful at row129?** This test computes the actual remaining target-bit rank, not the total number of state constraints or the count of feasible index hypotheses. That distinction is necessary before using another chronological index exclusion as evidence toward K04 bytes.

For an input vector `s[0..132]` of nonoverlapping four-word starts, use the full symbolic MT19937 recurrence over the 624 initial 32-bit state words:

`X[t+624] = X[t+397] XOR twist(X[t].MSB, X[t+1].low31)`.

Untemper all 132 intact original printer lines into 528 source words. **Delete selected row129 before adding any equations.** Treat every untempered output bit as a GF(2)-linear function of the initial 19,968 state bits and eliminate all 16,896 retained source-bit equations. An inconsistent alignment raises a source contradiction and never produces a coupon prediction. Reduce all 128 **tempered** missing payload bit-expressions modulo the resulting source row space. Report their quotient rank, each directly fixed tempered bit, and complete masks/values for the four selected words. A target quotient of 128 means no recovered target information, while a smaller rank means source-independent affine information about that payload has been recovered. If the quotient is 0, all 16 missing bytes are known from the original source alone.

This is a general finite GF(2) state-projection tool. It takes a candidate chronology supplied in JSON as `row_starts` and the original local ZIP. It never attempts a source-free hash preimage search or uses selected-row bytes to choose the chronology.

## Constructive positive controls on genuine seeded MT streams

Generate real CPython `random.Random(20261019).getrandbits(32)` outputs; choose 133 artificial four-output printer row starts `s[r] = h*r`, with gap/separation `h=4..10`. Keep 132 rows, withhold row129, and compare every source-derived fixed missing payload bit to the genuine, concealed synthetic row129. **Seven complete cases passed exactly**, including cases where the target is fully unknown and where most missing bits are predicted:

| Artificial start separation h | Source rank among 16,896 retained bits | Rank of unknown selected 128 bits | Individually fixed printed payload bits |
| ---: | ---: | ---: | ---: |
| 4 | 16,896 | 128 | 0 |
| 5 | 16,448 | 65 | 58 |
| **6** | **14,208** | **32** | **96** |
| 7 | 15,520 | 96 | 32 |
| 8 | 16,722 | 97 | 28 |
| 9 | 12,958 | 65 | 58 |
| 10 | 16,860 | 127 | 0 |

For `h=6`, independently withheld printed row129 words 0–2 are fully inferred, with complete word values `4DDBCC56, 36247813, 3722534D`, while the fourth word retains its full 32-bit ambiguity. These values are **purely artificial synthetic controls**, neither candidate original coupon bytes nor a source match. Other `h` values can fix scattered output bits or enforce affine relations without fixing any individual bit (h10). A single aggregate source rank is therefore an inadequate proxy for target recovery.

The positive examples demonstrate something not visible from the earlier two-group model: **the actual 528 original-format source words, when jointly indexed, can in principle determine many of the disputed target bits.** This is constructive permission to solve authentic global positions, rather than another seed exclusion, dictionary search, metadata coincidence or speculative ACK mutation.

## Exact deployment and stop criterion

Run the code's zero-argument SFT to reproduce seven independent withheld-payload checks. To analyze an original chronology, pass the original 43-member export ZIP and a JSON object with `row_starts` of length 133. It checks the source spool SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`, requires strict four-output record nonoverlap and refuses to load selected row129. If the same proposed global placement contradicts a retained printer word, it fails without producing any coupon bits.

**Original execution status:** no source-consistent global 133-row index vector is yet known from the shared research. Agent37's new conditional absolute-position exclusions at 945/946 leave 947..955 unresolved; a first MILP chronology with outstanding inverse contradictions is **not** an acceptable input for interpreting a result. Consequently the original target quotient has **not** been computed from an authenticated global chronology, and **zero authentic K04 bits are claimed**. The uniform synthetic start separation is deliberately artificial and cannot be applied to original rows as a recovered producer rule.

Next discriminating action: Obtain a single *fully consistent* source-only global row-start vector from Agent37 or an independently source-indexed recorder/producer trace, apply this projector, and require nonzero original target-bit gain. If it gains bits, preserve explicit masks and verify an intact held-out output before assessing the original unchanged K04 acceptance. If it stays at rank128, do not iterate conditional positions without new donor information. K08 still requires exact contemporary keeper-caption wording; this MT analysis adds none.

**Current original acceptance unchanged:** K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING; combined INCOMPLETE and not accepted.
