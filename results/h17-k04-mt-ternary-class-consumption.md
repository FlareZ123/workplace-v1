# K04: three-bit printer-class sampler recovered from hidden MT outputs

**Agent 6, 19 October 2026 ~05:25 UTC. New source-only cracking lead; original K04/K08 commitments remain unresolved.** Reproducer: [agent6/k04_mt_ternary_class_gate.py](../agents/agent6/k04_mt_ternary_class_gate.py). Input is the original 43-member local ZIP, printer spool SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The test reuses Agent 23's original-source 42 MT recurrence witnesses, *withholds selected row 129*, and never opens acceptance commitments, K04 mask or K08 nonce. The algorithm iterates inverse **and forward** MT recurrence inference to a fixed point, extending Agent 23's one-pass recovery of 30 full group-relative words to **65** full unobserved group-relative output words (35 additional). Do not count them as independently preserved historical printer records or deduplicate them across disconnected relative-coordinate groups without an alignment.

## New three-way class relation

For an intact ordinary printer row with independently reconstructed untempered MT output immediately before its four-word PAYLOAD, temper that predecessor back into its observable 32-bit RNG output. Its **highest three bits** give the entire recorded CLASS index, in this order:

- **0 → LABEL**
- **1 → STORES**
- **2 → RECOVER**

Exactly **12 ordinary rows** have a fully reconstructed immediate predecessor. Their zero-based row IDs and recovered three-bit indices are:

| Row | CLASS | Highest three bits |
|---|---|---|
| 3 | RECOVER | 2 |
| 4 | LABEL | 0 |
| 13 | STORES | 1 |
| 14 | STORES | 1 |
| 28 | STORES | 1 |
| 30 | STORES | 1 |
| 34 | LABEL | 0 |
| 38 | RECOVER | 2 |
| 44 | STORES | 1 |
| 45 | STORES | 1 |
| 74 | LABEL | 0 |
| 93 | RECOVER | 2 |

Choosing index mapping from the six chronological earliest observed rows (3,4,13,14,28,30) predicts **all six** later independently reconstructed predecessors (34,38,44,45,74,93). The last two rows 74/93 are newly accessible from iterative closure and were *not* in Agent 23's earlier ten-row first-pass probe.

In seven other fully reconstructed **consecutive predecessor positions** belonging to these same twelve ordinary rows, the highest three bits are each **3–7**, consistent with failed random-rejection samples just before the final accepted 0/1/2 class sample. Exact observed prior rejected sequences, latest-first, are row4 [5,7], row34 [4], row38 [5], row44 [7], row45 [7], row93 [6]. Thus the falsifiable producer hypothesis is a **three-bit rejection loop** with accepted values 0/1/2 mapping to CLASS, followed immediately by four 32-bit printer payload outputs. This explains variable hidden draw consumption in the *ordinary* cohort and is substantially more specific than the earlier binary predicate `CLASS==RECOVER`, which only used the upper two bits.

The original spool does **not** document the producer code or guarantee this hypothesis. The 12 observed rows are a recurrence-selected subset, not a random sample of all 128; the chronological last-six check is a diagnostic holdout over this subset, not an independent preregistered test. Some skipped MT outputs may come from destination or other fields. Do not promote the inferred draw loop to an authenticated spool-generation specification solely from arithmetic coincidences.

## Why this changes the K04 attack

The ordinary-class candidate rule is **consistent with** the exact missing-output gaps after row43 and row96: the rejected three-bit values generate variable numbers of invisible draws, including long streaks. It gives a testable bit-level side channel to infer unknown MT outputs and chronological row-start placements without consulting the selected K04 hash. For every *newly* inferred ordinary row-start predecessor, require the correct 0/1/2 class index; for a hypothesized preceding rejection streak, require values 3..7. Apply these tests on an intact row held back from fitting, then attempt the hidden row43→44 / row96→97 interval reconstruction.

**Tail distinction:** in the five `Z`-timestamp RECOVER-tail records, selected row129 remains withheld. The known exact `s131-s130=4` means row131's immediate preceding output is simply row130's final payload word, whose top three bits are **3**, and therefore **not an ordinary cohort CLASS sampler**. A separate retry/no-metadata-draw path may account for this verified zero-gap transition. The test must not force the ordinary CLASS gate onto row131 or other tail records without an independent source argument.

**Conditional new tail hypothesis, unproved:** if both tail transitions row128→129 and row129→130 also consume *exactly four outputs each*, the established source equations `s128=s43+623` and `s130=s44+620` imply `s44-s43=11` and the selected row start is `s129=s43+627` (a **single output index**, compared with the 55 model-permitted indices). This is only a testable new model assumption. Neither the selected 16 printer bytes nor their K04 XOR output can yet be predicted from the source-observed words, and the unchanged K04 commitment has not passed.

## Verification limitations and next step

- A deterministic source-only reproduction of 65 additional/group-relative full words and 12 class-index matches exists. These are **conditional on the 42 witnessed matches representing one chronological MT19937 stream**, and on the recurrence closure being interpreted as source-generator outputs.
- Existing inverse-closure data do **not** determine any of the four selected row129 words, even after combining the two connected source groups around row43/44 for all 55 feasible inter-row gaps. Do not advertise the selected coupon as recovered.
- Highest-value follow-up: integrate these 3-bit acceptance/rejection constraints into a simultaneous stream-position + MT-state model; infer **previously hidden** class-candidate bits or a held-out intact tail prediction. Focus on the 43→44 and 96→97 gap words, then submit any complete K04 candidate to the original unchanged verifier.

Original source files and acceptance commitments untouched; verified key remains **K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false**.


## Quantified consequence: regular metadata-draw floors collapse the target index window

The new [source-pinned constraint solver](../agents/agent6/k04_mt_metadata_draw_bounds.py) retains all **42** selected-row-withheld witnessed MT equations and applies two distinct *additional hypotheses* to 127 ordinary-to-ordinary transitions. It imposes only the original four-payload-word floor on the RECOVER tail, avoiding an unsupported assumption that tail rows use the ordinary sampler. Each interval is the exact feasible extremum of the corresponding difference-constraints system.

| Ordinary per-row minimum generator draws | Assumption | `s44-s43` | `s129-s0` possible | Positions |
|---|---|---|---|---|
| 4 | Original source-only monotonicity | 11..65 | 917..971 | 55 |
| 5 | Every ordinary row consumes at least **one** preceding CLASS sampler draw | 11..43 | 931..963 | 33 |
| 6 | Every ordinary row additionally consumes at least **one** DEST/other metadata draw | 11..21 | 945..955 | **11** |
| 7 | Every ordinary row consumes at least **three** nonpayload draws | **INFEASIBLE** | **INFEASIBLE** | 0 |

The 6-draw floor remains jointly compatible with all 42 source witnesses; the stronger universal 7-draw floor contradicts them. Source evidence contains three DEST values (`desk`, `bench`, `store`) and the recovered CLASS sampler consumes at least one draw. Whether DEST is separately sampled from this same MT stream for **every** ordinary row is still a testable producer hypothesis. The 11-index K04 bound is conditional, not an unconditional recovery or an independently observed tail spacing.

A simple iid model with explicit 3-bit rejection for CLASS (success probability 3/8) and 2-bit rejection for DEST (success probability 3/4), one each per ordinary record, consumes a mean **332** metadata draws over 83 regular row transitions, compared with **292** inferred from the source equation `s83-s0=624` minus 83 × 4 payload draws. An exact convolution of two negative-binomial distributions gives `P(total draws <= 292)=0.01902677154` under this fully specified *hypothetical* model. A single 3-bit CLASS sampler by itself instead gives `P(total draws >= 292)=0.00051295800`. This is only a model-comparison diagnostic; the two samplers, their independence, and all-row uniform application are not authenticated producer facts. Conditional model fitting after inspecting the case must not be presented as a preregistered probability claim.

**Next cracking discriminator:** reconstruct a previously unseen destination-selector predecessor word from original MT recurrence, use the recorded DEST to test a fixed 2-bit mapping before inspecting the actual bits, and then apply a source-checked draw-consumption automaton to row43→44 and row96→97. A correct 11-index branch alone still cannot supply the four missing K04 words without state or seed reconstruction.


## A strictly source-only index improvement from recovered-word nonoverlap

The [separate reproducer](../agents/agent6/k04_mt_word_nonoverlap.py) **does not assume** either CLASS or DEST is RNG-generated. It takes each independently recovered complete word immediately before an intact row, temporarily considers the ordinary four-output floor `s[r]-s[r-1]>=4`, and rules out any candidate adjacent-row distance that would assign **two different source-determined 32-bit words to the same MT output position**. This inference depends on the same 42-witness common-stream interpretation as the prior MT reports, but no additional producer algorithm.

Exactly **12** previous→current transition lower bounds improve, by a total of 19 required positions over the original four-word floors: 2→3 ≥5; 3→4 ≥7; 12→13 ≥5; 13→14 ≥5; 27→28 ≥5; 29→30 ≥5; 33→34 ≥6; 37→38 ≥6; 43→44 ≥6; 44→45 ≥6; 73→74 ≥5; 92→93 ≥6. The previously known cross-tail witness already forces 43→44 ≥11. These bounds use **actual full-word inequality**, so they do not require assuming the newly identified CLASS selector mechanism applies uniformly.

Adding only these twelve constraints to all 42 intact-source MT equations tightens the original row129 stream-start interval **917..971 (55 indices) → 919..971 (53 indices)**; the regular row43→44 difference narrows **11..65 → 11..63**. This modest but unconditional-*within-the-existing-MT-stream-hypothesis* improvement belongs on a different evidence tier from the much tighter 11-index bound under speculative universal two-metadata-draw consumption. The selected ACK row129, its recorded bytes, and all REC8 commitments were withheld throughout.
