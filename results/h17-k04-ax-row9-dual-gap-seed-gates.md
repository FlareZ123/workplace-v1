# K04: AX-7778 + printer row9 yields a previously unused initialized-state witness and two new seed-length gates

**Agent 28, 19 October 2026 ~14:39 UTC.** Original-source conditional **K04 cracking discrimination**, with 36 actual CPython seeded positive controls. **No K04 coupon bytes recovered; K08 remains missing.** Original commitments, mask, selected printer row129, verifier and K08 data are neither consulted nor modified. One-file stdlib reproducer: [`agents/agent28/k04_row9_ax_seed_gates.py`](../agents/agent28/k04_row9_ax_seed_gates.py).

## Mechanism, independent carrier and exact phase assumptions

Define `p` as the unknown absolute first MT19937 output index of ordinary printer row34, with `402 <= p <= 621` for the conditioned first-output-cycle interpretation. Agent36's original-source cross-carrier assignment fixes printer row33 at `p-6`, row63 at `p+220`, and AX-7778 checkpoints ordered by `(seq,attempt)` at stream positions `p-407 .. p-392`. **These are producer/order hypotheses; only the bytes and the internally matched three-word cross-carrier fingerprint are original observations.**

Original, SHA-pinned row33/63 inversions combined with AX checkpoint indices 5,6,7 reconstruct exact untempered `X[p-402..p-400]`:

`51DA82D0 174C046A 6447255B`

These three words are separately corroborated by the original checkpoint high16s `1CB5 AEDE C98C`, interpreted as little-endian 16-bit words. Earlier seed-window work used row10 together with the *different* AX-derived ancestor block at `p-396..p-393`; the block above had **not** been inverted against row9 to recover a new CPython initialized-state fragment.

For the first twist's in-place second region, when `p-175..p-173` represents three consecutive first-cycle outputs, its pairwise XOR with `X[p-402..p-400]` and inversion of MT's twist gives initialized-state words:

`S[p-174]`, `S[p-173]` and `S[p-172].low31`.

Original row9 provides that exact later three-word run under either of two **explicit and distinct draw-count hypotheses**:

- `g=6`: row9 starts at `p-176`, so use its words 1–3.
- `g=5`: row9 starts at `p-175`, so use words 0–2, leaving word3 at `X[p-172]` available for a held-out AX check. **The five-draw branch is inconsistent with the leading two-metadata-draw-per-transition model**, but is separately useful for discriminating less restrictive producers.

The independently known late initialized-state quartet from Agent9's intact source bridge is `S[p-1..p+2] = 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`.

## Original-source result: six-draw hypothesis, 173/174-key-period collisions

New reconstructed initialized-state fragment:

`S[p-174]=418BDA1E`, `S[p-173]=2E02BC3D`, `S[p-172]&7FFFFFFF=38EBB043`.

Within CPython `init_by_array`, each three-word initialized-state window algebraically yields its key-array word plus modular key index, without needing the seed. This early window's key index is `p-173`. The late quartet independently supplies the key terms at indices `p` and `p+1`. When the key-array word length `n` divides 173 or 174, the corresponding two extracted key terms must be identical.

**Zero equality matches** among 220 phases `p=402..621` × two possible high-bit completions of the early third word, for each of these five lengths:

| `n`, 32-bit seed-array words | Repeated key-index separation | Original matches / 440 |
|---|---:|---:|
| 29, 58, 87, 174 | 174 | 0 each |
| 173 | 173 | 0 |

The values 29,58,87,173,174 were outside the prior 167/168-period sieve. This branch needs **no AX position8 contiguity assumption** and no seed enumeration, but it *does* depend on the unconfirmed row9→10 six-output placement.

## Original-source result: five-draw hypothesis, independent held-out AX position8

Under `g=5`, the new initialized-state fragment becomes:

`S[p-174]=FBB38820`, `S[p-173]=CCA6D76A`, `S[p-172]&7FFFFFFF=4814FE5F`.

The same late quartet supplies the CPython seed-key term at early update index `i=p-171` whenever `n|172` or `n|173`. With each of the two completions of `S[p-172]`, ordinary `init_by_array` predicts full `S[p-171]`. Invert the first-cycle MT transition using original row9 word3 `X[p-172]` to predict full `X[p-399]`, then temper its high16.

This is compared against **independently withheld original AX-7778 checkpoint position8**, literal `(seq4,attempt1)=7CA7` and interpreted upper-16 value `A77C`. The checkpoint is not used to construct the initial three ancestor words or derive the candidate seed keys.

| `n`, 32-bit seed-array words | Key-index separation | AX position8 matches / 440 |
|---|---:|---:|
| 43, 86, 172 | 172 | 0 each |
| 173 | 173 | 0 |

This branch requires the **stronger** contiguous ordering premise for AX checkpoint positions5–8 as well as the less-preferred five-output row9→10 transition. The result is a bounded, independent 16-bit prediction failure, not a general prohibition of those seeds or that printer producer.

## Calibration and consequence

The source-pinned standalone Python SFT checks the unchanged original spool SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083` and unchanged transfer-audit SHA256 `32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf`. Synthetic `random.Random(large_integer_seed)` controls reconstruct state and compare against **actual** seeded Python `getstate()` at phases 402,430,555,621, for all nine branch/length combinations: **36/36 PASS**. No original selected row129, XOR mask, REC8 hash or K08 materials are read.

The branches conditionally exclude eight **distinct** seed-array lengths across their respective models: the g6 family `29,58,87,173,174` and the g5 family `43,86,172,173`; **they must not be pooled as one unconditional eight-length rejection**. Neither branch recovers K04 target bits. The important new reusable attack surface is the **row9-to-AX original-source seed window** at `p-174..p-172`, which creates modular period lengths 172–174 beyond previous 167/168 offsets. A producer-order witness confirming `s10-s9` or an independently placed full-word gap donor could make this window more decisive. Avoid generic target hashing or six-slot replay.

**Acceptance status unchanged:** K01/K02/K03/K05/K06/K07 PASS, K04 and K08 MISSING, combined INCOMPLETE and `accepted: false`.

## Additional constructive K04 phase discriminator: two AX checkpoint high16s predict metadata (14:44 UTC)

The six-output row9→10 branch places two unobserved generator outputs at `X[p-172]` and `X[p-171]`, after row9's four-word payload and before row10. Under the hypothesized ordinary producer's **post-payload DEST** then **terminal pre-payload CLASS** order, exactly two metadata outputs means both sampled without rejection. The original row9 `DEST=store` corresponds to 2-bit return **0**; row10 `CLASS=STORES` corresponds to 3-bit return **1**.

For any CPython key-array length dividing **172**, the two known late key-array terms at residues `p,p+1` determine the two consecutive early state updates `S[p-171],S[p-170]` from this report's gap6 `S[p-173],S[p-172]` (two MSB completions). The original, *previously unspent* AX checkpoint positions **8 and 9** record `7CA7` and `A234` as little-endian 16-bit words, i.e. high16 tempered `A77C` and `34A2` for `X[p-399]` and `X[p-398]`. Because tempering is GF(2)-linear, the two predicted sampler high16s are:

`temper(X[p-172]).high16 = A77C XOR temper(twist(S[p-172],S[p-171])).high16`

`temper(X[p-171]).high16 = 34A2 XOR temper(twist(S[p-171],S[p-170])).high16`.

Testing both native upper-bit completions over every first-cycle phase `p=402..621` gives the **same conditional shortlist for n=43,86,172**, because each length divides 172:

| Source-only terminal requirement | Surviving `(p,bit)` assignments / 440 |
|---|---:|
| row9 DEST=store (top2=0) | 105 |
| row10 CLASS=STORES (top3=1) | 50 |
| **both simultaneously** | **10** |

Surviving absolute phases: **460,470,472,485,497,536,567,568,571,592**, each with one recovered `S[p-172]` MSB. Under the *additional* disputed recorder-prefix chronological bound `p>=535`, only **536,567,568,571,592** survive. The stronger prefix premise is kept separate from the first-cycle inference. **12/12 independent CPython seeded positive controls** reproduce full predicted high16s from actual `random.Random(seed).getstate()` and generated 32-bit outputs. Standalone read-only companion [`agents/agent28/k04_gap6_ax89_metadata.py`](../agents/agent28/k04_gap6_ax89_metadata.py) imports the first reproducer and reads no selected K04 payload or REC8 acceptance.

This is a first constructive combination of this source-derived row9 initialized-state window, *both additional AX checkpoint* high16 values and **two original recorded metadata labels**. It reduces a conditional seeded phase space; it does not determine selected row129 bits or prove the physical historical producer used the two selector calls. In particular it assumes AX checkpoint position8/9 contiguity, the common MT stream, standard CPython initialization, and exactly two consumed sampler outputs between row9 and row10. **No K04/K08 acceptance has changed.**

## New backwards seed-state gate: AX position4 excludes five more period-175 hypotheses (14:52 UTC)

The six-draw row9 window `S[p-174],S[p-173]` and the late window's two complete key-plus-index terms support a different attack: **reverse** two steps of CPython `init_by_array` into `S[p-175]` and `S[p-176]`. Both mixing multipliers, 1664525 and 1566083941, are odd modulo `2^32`, so these state steps invert exactly. For every key-array length `n` dividing **175**, the key at early update index `p−173` matches the late key term at `p+2`, and the key at early index `p−174` matches the late key term at `p+1`. This determines two prior initialized-state words **without guessing even one 32-bit seed word or the unknown high bit of `S[p−172]`**.

Original row9 word0 supplies the output `X[p−176]` under the gap6 premise. Inverting the MT first-cycle twist,
`X[p−176] = X[p−403] XOR twist(S[p−176],S[p−175])`,
predicts the **high16 of earlier `X[p−403]`**, which can be independently checked against source AX-7778 checkpoint **position4**, literal `(seq2,attempt1)=368D`, little-endian high16 **`8D36`**. This checkpoint, unused by the prior AX5–7 fragment reconstruction and unused by key-word inversion, is withheld from candidate generation.

For phases `p=403..621`, all five divisors `n=5,7,25,35,175` have **0/219** original checkpoint matches each. The minimum predicted-vs-original 16-bit Hamming distance across phases is **three bits** for each family. **20/20 seeded CPython positive controls** (five lengths, four phases including p407 and p621) exactly reconstruct the two prior initialized-state words and withheld checkpoint. [Source-only standalone companion](../agents/agent28/k04_gap6_ax4_reverse.py), same pinned original sources, no selected coupon, original acceptance, mask or K08 material read.

The new **25,35,175-word seed-length exclusions** are distinct from the previous 167/168/173/174 collision families. The `n=5` rejection is particularly interesting in light of Agent50's alternative first-cycle `n=5` boundary survivors `p=564,566,621`: under the **additional six-output row9→10 plus ordered AX checkpoint4 physical producer premise**, even those three phases fail the independent 16-bit checkpoint. This does **not** contradict Agent50's less restricted phase analysis, which does not assume the new row9/AX4 alignment. The compatible `n=7` class had already failed a separate 168-period test under another source alignment.

**Research next:** independently substantiate or falsify `s10−s9=6` using normal spool metadata and unaffected intact rows; attempt a nearby group/AX checkpoint hit that confirms the alignment without consulting target row129. This mechanism is a source-conditioned nonlinear **seed-family gate**, not an authenticated K04 coupon or K08 caption.
