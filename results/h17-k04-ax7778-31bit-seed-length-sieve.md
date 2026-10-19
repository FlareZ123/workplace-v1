# K04 AX-7778: unused 31-bit initialized-state holdout eliminates 17 CPython seed-array lengths

**Agent 18, 19 October 2026, ~12:03 UTC. Genuine new source-conditioned K04 seed-family exclusion.** This report does not claim selected K04 coupon bytes or K08 caption. Original evidence, printer row129, route/mask, nonce, acceptance commitments and verifier are untouched and excluded from the reproducer.

## New source observation, previously dropped by two-cycle inversion

Agent 9's [AX-7778 crossing-cycle bridge](h17-k04-AX7778-cross-cycle-seed-window.md) established source-derived initialized CPython pre-first-output MT19937 words `S[p-168]=0A9DE247`, `S[p-167]=FBBBB07E`, where `p` is the absolute first output index of intact printer row34. It retained only the **two fully reconstructed words** from three inverse-twist pairs.

There is an additional **unspent 31-bit witness** in the **third** inverse pair. With the source-anchored `s64-s34=227` geometry, invert intact printer row34/64 outputs to reconstruct ancestors `X[-396..-394]=BFD3ACA1 EF2DD8BC 611914B2` in row34-relative output coordinates. Intact printer row10 output 3 at position `-167` equals `341AEF83` (untempered). The exact MT mixed input

`M = untwist(611914B2 XOR 341AEF83)`

supplies the top bit of `S[p-167]` **and separately the low 31 bits of the next initialized state word**:

**`S[p-166] & 7FFFFFFF = 2A07F662`.**

Agent9's two-word reconstruction used only the top bit of that same mixed input. The low31 remained available as a **new held-out source constraint**, not an extra word guessed from the seed model. This is conditionally source-pinned by the AX-7778 joined printer spacing and by the same CPython first-cycle interpretation. It is mathematically distinct from the two full early words.

## Algebraic seed-length sieve

For CPython's numeric `Random(int)` `init_by_array` initial state and a key array of `n` 32-bit words (`1 ≤ n ≤ 169` here), the four independently reconstructed late initialized state words

`S[p-1..p+2] = 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`

determine **two complete key-array words** directly by reversing the two mixing recurrences, at modular indices `p % n` and `(p+1) % n`. The two reconstructed early initialized words `S[p-168]`, `S[p-167]` can predict `S[p-166]` from the same recurrence using key index `(p-167) % n`.

Thus the early forward word is **fully source-predictable without guessing any seed word** whenever either `n | 167` or `n | 168`. There are 17 such word lengths at most 169. For each one, enumerate the explicitly conditioned absolute row34 positions `p=535..621` and compare the predicted low31 word with **held-out original source** `2A07F662`. This is a maximum of `17 × 87 = 1,479` seed-model comparisons, rather than enumerating even one 32-bit unknown seed word. It does not use the selected printer row129 or an acceptance digest to fit a prediction.

## Completed source scan and actual positive controls

[Independent source-only stdlib SFT](../agents/agent18/k04_ax_31bit_seed_sieve.py) reads and SHA-256 pins the original spool; derives the early words and heldout low31 directly from intact original rows 10/34/64; imports no other researcher code; uses Agent9's published intact-source late quartet; and enumerates the 87 phases under the original common-generator/recorder-prefix model.

| Tested CPython seed-array word lengths `n` | Phases per length | Original low31 matches |
|---|---:|---:|
| `1, 2, 3, 4, 6, 7, 8` | 87 each | **0** |
| `12, 14, 21, 24, 28` | 87 each | **0** |
| `42, 56, 84, 167, 168` | 87 each | **0** |
| **Total: 17 lengths** | **1,479** | **0** |

Synthetic tests construct **actual CPython `random.Random(seed)` initialized states** for independently chosen numeric seeds at 5 phases `p=535,555,584,605,621` for *each of the 17 sizes*. **All 85/85 positive controls pass**, including 96-bit, 128-bit, 672-bit and multi-kilobit seed arrays. The same seed-byte-to-array interpretation as CPython is used; the test validates actual initialized state values rather than internal reconstruction circularity.

This is more than another seeded text dictionary: the 31-bit condition eliminates **all possible values** of the tested numeric seed-array sizes under the conditional window, including potentially long SHA-512-expanded string/bytes seed arrays **if** their resulting `init_by_array` key length is one of the enumerated sizes. For example, a 21-word or 24-word key array cannot match this source alignment regardless of its contents. It also directly extends the newly completed separate later-cycle 32/64-bit test ([Agent18 report](h17-k04-ax7778-latercycle-shortseed-exclusion.md)) to 96-bit, 128-bit and many longer seeds, without search over any missing key word.

## Limits and future cracking leverage

The inference assumes all source-pinned row10/34/64 word placements belong to **one CPython MT19937 stream** and that both reconstructed initialized-state windows fall in the specified **first initialized-state / first output-cycle alignment**, with the conditional recorder-prefix absolute range `535..621`. It does **not** exclude other phases, another generator, a restarted/advanced epoch, incorrect historical cross-source ordering, or key lengths outside `n | 167` or `n | 168`. Direct text-seed constructions with other lengths survive. The inferred mixed input and low31 must not be mistaken for four accepted coupon bytes: **K04 target information recovered remains zero**.

A powerful new general technique follows: before searching source controls or candidate seeds, compare **seed-word index residues** between disjoint initialized-state windows. If their update indices coincide modulo a hypothetical key length, source reconstruction yields a *pre-candidate* 31-bit or full32 discriminator even when most key words remain unknown. For surviving lengths, locate another initialized-state pair or a different cross-cycle partial observation with complementary residue geometry, rather than repeating mass seed/phrase/hash scans.

**Original REC8 state remains K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING; combined INCOMPLETE and `accepted: false`.**
