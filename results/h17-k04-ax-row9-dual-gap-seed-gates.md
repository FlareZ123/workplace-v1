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
