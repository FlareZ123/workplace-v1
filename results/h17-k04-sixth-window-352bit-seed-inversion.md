# K04: sixth source-bridged MT initialized-state window cracks a synthetic 352-bit seed

**Agent 46, 19 October 2026, 07:11 UTC.** New, source-conditioned *method*, bounded negative result on original spool, **no accepted K04/K08 value**.

## What changed

Agent 8's two-stage numeric CPython `init_by_array` inversion had successfully recovered seeded synthetic 288/320-bit cases and rejected 22,445 completed original-source 320-bit assignments. I first tested larger 352/384-bit two-stage cases using the exact same four original seed-fragment windows and row11 three-pair boundary. Original source had, respectively, 67,274 and 62,486 four-window phase-compatible tuples, and 61,123 and 50,091 successful first bridges. Neither yielded any **complete** source key. Crucially, the identical limited-window synthetic controls also could **not** recover a full key in either class; therefore this says **nothing** about excluding 352/384-bit seeds.

A new source-only window inventory uses the 42 printer recurrence anchors plus Agent 4's three independent, source-carried low31-bit TRP2/RC17 index relationships:

- row9→40 start +229 (node49/event82 archive controls);
- row7→38 start +230 (CRC-valid node50/event8 TRP2 record26);
- row28→59 start +226 (two withdrawn RevB RC17 PURGE/VERIFY control strips).

The 42-witness fixed-point output reconstructor has **30** maximal 227-separated full-word pair runs of length≥2 in the printer-only groups, rising to **35** after the source-conditional cross bridges. In the merged group `rows28,59,80,111`, the newly created run starts at group-relative **-1** and consists of **four** consecutive complete 227-separated output pairs. That gives **one additional independently reconstructible CPython seed-array word**, via the exact same inverse-initialization algebra as Agents 1/8. Other new runs are row7/38/91/121 relative index 1 length3, 397 length3 and 624 length4; row9/40 relative2 length2; row28 merged relative623 length3. The last few do not directly supply additional first-cycle key words under the current inversion range. See [window enumerator](../agents/agent46/k04_cross_carrier_seed_windows.py).

## New six-window seed inversion

The [reproducer](../agents/agent46/k04_seed_six_window.py) uses:

- four original initialized-state pair windows rooted at printer rows3,10,13,14;
- original row11's three-pair boundary for the first unknown-key algebraic bridge;
- row13→14 as the second unknown-key bridge;
- the **new 4-pair row28/59/80/111 group** at first pair `s28-1` as an extra seed-fragment source.

Each source-phase tuple is checked for exact key-word consistency before completing the missing key at the sixth window. Row28's tentative first-cycle phase is searched only from `max(p14+84,180)` through `393`, enforcing at least 14 ordinary six-output row transitions from row14 to row28 under the conditional CLASS+DEST sampler. The four original phase search windows are the ones inherited from Agent8, and short row10→11 and row13→14 bridge limits remain **18** outputs. This is a **bounded model**, not an exhaustive test of 352-bit Python initialization. All original input files and REC8 commitments remain unchanged. Printer **selected ACK row129 is completely withheld** from candidate construction and tests.

### Computational controls and original-source outcome

| Tested seed class | End-to-end synthetic recovery | Four-group phase assignments | After first bridge | After second bridge (10 key words) | Complete six-window seed assignments | Held-out intact printer word34/3 |
|---|---|---:|---:|---:|---:|---:|
| 352-bit / 11 words | **PASS**, actual synthetic seed recovered (phases `14,57,62,86,95,184`) | 67,274 | 61,123 | 3,735 | **63,916** | **0 matches** |
| 384-bit / 12 words | **NOT COVERED** in searched synthetic phase family | 62,486 | 50,091 | 2,388 | **0** | 0 tests |

The 352-bit synthetic case uses Python's actual `random.Random(seed)`, complete MT19937 output generation and inverse twist, and verifies exact recovered key equality, including all eleven 32-bit words. The original-source heldout is row34's **fourth** printer word, which was omitted from the seed-fragment inputs. Original source's 63,916 *phase assignments* may include repeated complete seed values. Every assembled assignment failed this genuinely separate intact-source output prediction; no original acceptance commitment is invoked.

The 384-bit experiment must **not** be described as an excluded seed class: the two short algebraic bridges plus one extra fragment recover at most 11 of 12 key words within the tested phase grammar, leaving a genuine missing key word. One more independently identified initialized-state word or a generalized long-gap inversion would be needed to make that class test constructive.

## Consequence for subsequent K04 cracking

The new cross-source RC17/recorder links do more than raise restored MT state-word counts: they generate a **usable sixth independent CPython initialization window** and allow exact 352-bit seed algebra instead of infeasible raw 2^352 enumeration. Within the strict first-cycle/common-stream, bounded, two-selector phase model, every fully reconstructed original 352-bit seed assignment is falsified by an intact printer word. The remaining source phase configurations, other seeding types, advanced MT epochs and non-CPython models are open. No K04 bytes, K08 phrase or combined REC8 acceptance were recovered.

### Reproduction

Both runs executed with the repository's manually dispatched `workflow_dispatch` workflow `.github/workflows/h17-k04-extended-seed.yml`; there is **no per-commit workflow**. Logs:

- [First 352/384 two-stage probe](https://github.com/FlareZ123/workplace-v1/actions/runs/39213550554)
- [30→35 source-window inventory](https://github.com/FlareZ123/workplace-v1/actions/runs/39213740700)
- [Calibrated 352-bit six-window result](https://github.com/FlareZ123/workplace-v1/actions/runs/39214281409)

The workflow constructs a temporary 42-member ZIP from the current `resources/` tree; the removed historical AGENT_PROMPT file is unnecessary because the scripts read unchanged original spool, recorder and procedure sources from that tree. The selected row is excluded by the source-pinned imports. See [source code](../agents/agent46/k04_seed_six_window.py) for exact loop ranges and synthetic construction.

## Important cross-source origin qualifier (19 October ~07:29 UTC)

The independent [Agent48 recorder-origin bound](h17-k04-shifted-seed-prefix-constraint.md) derives `s0>=292`, `s10>=396` and `s13>=420` if an original recorder control and the printer were emitted by the same chronological MT stream. A row13 five-pair group then **cannot** occupy the first 624-output seeded state cycle (`p13<=392` would be required). Our present 352/384-bit experiments deliberately assume *all original row3/10/13/14 reconstructed seed windows occupy that first cycle*, as inherited from Agent8's original model. **Those phase models are therefore incompatible with the additional shared-recorder-origin premise.** These reports establish reusable multi-window algebraic methods and bounded negative results only for their stated, narrower printer-first-cycle model. They should not be interpreted as disproof of 352/384-bit seeds in the richer cross-source historical hypothesis. This is why subsequent Agent46 work shifted to early-cycle row3 + TRP2-bridged row7 instead of extending first-cycle long-seed sweeps further.
