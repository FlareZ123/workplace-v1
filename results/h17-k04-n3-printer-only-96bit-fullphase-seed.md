# K04: all first-cycle 96-bit CPython integer seeds excluded by a two-candidate printer-only inversion

**Agent 8, 19 October 2026.** [Standalone read-only SFT](../agents/agent8/k04_n3_complete_firstcycle_seed.py), plus original-source calibration. **Zero original K04 seed-class survivors; K04/K08 remain unresolved.** The analysis does not access original selected coupon row129, K04 mask, original REC8 acceptance file, K08 nonce/phrase, or the verifier.

## Source-derived algebraic completion

The original printer's existing five 227-separated MT pairs in the **intact row3/34 group** yield four full consecutive pre-first-twist initialized-state words and one further known low31 word. These are already derived in Agent1/18's source-pinned printer inversion and are reloaded from the intact original spool:

`S[p−1],S[p],S[p+1],S[p+2] = 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35` and `S[p+3].low31=31FD69FC`.

For **CPython `random.Random(integer)` with exactly three 32-bit numeric seed-array words**, the reversible `init_by_array` equation takes consecutive triples `S[i−2..i]` to a source-constrained seed word `KEY[(i−1) mod 3]`. Unlike the five-word case, the three latest reconstructed updates cover **every numeric seed residue**:

| Source inverse update | Key-index residue | Seed bits resolved |
|---|---|---:|
| `S[p+1]` | `p mod 3` | 32 |
| `S[p+2]` | `(p+1) mod 3` | 32 |
| `S[p+3].low31` | `(p+2) mod 3` | 31 |

Thus **95 out of 96 original-seed bits can be inferred**, with only the final key word's highest bit ambiguous. Exactly **two complete 96-bit seed candidates per phase** remain, irrespective of the 2^96 nominal seed space. No AX-7778 checkpoint, recorder bridge or CLASS/DEST sampler assumption is used; this new class uses only one intact printer MT group.

An absolute index `p` must let the first reconstructed output at `p−229` exist and keep `S[p+3]` in the initial 624-word state. This yields **every possible first-cycle phase `p=229..620`**, 392 phases. The earlier source-only short-seed sweeps examined narrower phase windows; this result provides a complete source-only full-phase n3 test for this group geometry.

## Independent intact-source holdout

The fourth 32-bit word (zero-based word3) of original **printer row34** is `2AC160B4`. The reconstruction used intact row34 words0–2; **word3 was excluded from every state and seed inversion equation**. Conditional on a given phase, it is the actual tempered MT output at absolute index `p+3`.

Using the real Python 3 `random.Random(seed).getrandbits(32)` generator, initialize each of the two reconstructed 96-bit integer seeds and predict this entire withheld original output. **Neither branch matches at any phase**:

| Quantity | Original-source result |
|---|---:|
| Tested first-cycle phases `p=229..620` | **392** |
| Reconstructed 96-bit seeds per phase | **2** |
| Fully specified candidate seeds tested | **784** |
| Exact 32-bit heldout word matches | **0** |
| Actual CPython-seeded full-window positive controls | **90/90 PASS** |

The positive controls use 15 distinct, actual Python 96-bit numeric seeds at each of six phase placements 229,230,300,396,535,620. Invert five synthetic source MT pairs into four complete and one low31 initialized-state words, reconstruct the two candidate keys, and require the **true numeric seed be the unique branch** predicting a separately withheld generated word. This verifies the inverse key residue indexing, seed construction, tempering and boundary geometry.

The original source was held fixed and authenticated by its spool SHA-256. The new execution independently returned **784 tested, 0 heldout matches**, consistent with a source-conditioned exclusion of this entire n3 first-cycle model.

## Relevance, limitations and next cracking priority

This is a meaningful elimination of a **96-bit historical seeded producer class**, using a new 95-bit inversion and 32-bit prediction, rather than testing the archive hash or scanning arbitrary seed dictionaries. It strengthens earlier bounded 32/64-bit and 96-bit tests and does **not** rely on the disputed transfer-checkpoint ordering.

The actual printer's shared MT19937 interpretation, pre-first-twist initial epoch and CPython numeric seeding remain producer hypotheses, not authenticated original software. A later-cycle source, independent seed epoch, different MT implementation, arbitrary seed length or inaccurate spool reconstruction would escape this particular exclusion. The computation yields **zero recovered bits of the historical K04 coupon**, because the n3 model fails its untouched source holdout. The original K08 caption is still unquoted and unresolved.

**Cracking implication:** small numeric seed classes can be attacked completely and algebraically from intact source words, but all first-cycle 96-bit candidates are incompatible with retained printer evidence. Focus next on an independently sourced producer/seed contract or the *two paired ancestral intervals* required for direct K04 coupon reconstruction. K04 and K08 remain MISSING; combined acceptance remains INCOMPLETE and `accepted: false`.
