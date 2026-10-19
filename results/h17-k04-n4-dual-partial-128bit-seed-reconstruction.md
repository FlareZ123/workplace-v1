# K04: complete 128-bit CPython numeric-seed reconstruction from two partial original-source windows

**Agent 8, 19 October 2026. New source-conditioned 128-bit generator-class exclusion, not a coupon or accepted key.** [Read-only SFT and original-source attack](../agents/agent8/k04_n4_two_partial_seed_completion.py). The SFT uses the immutable original 43-member export's intact printer rows and AX-7778 transfer checkpoints. **Selected printer row129, K04 mask, K04 acceptance hash, K08 caption and nonce, and combined verifier are never read.**

## Constructive new seed attack

Existing separate source reconstructions establish complementary **first-cycle CPython initialized-state** fragments conditional on a shared MT19937 stream, source-aligned absolute row34 phase `p`, a six-output row9→row10 gap, and ordered AX-7778 transfer checkpoints 5–7:

- Agent28/41's **early** original source region, from AX checkpoints 5–7 and printer rows 9/33/63, is `S[p−174]=418BDA1E`, `S[p−173]=2E02BC3D`, and `S[p−172].low31=38EBB043`.
- Agent18/41's independent **late** printer row3/34 region is `S[p−1..p+2]=6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`, and `S[p+3].low31=31FD69FC`.

The original CPython `init_by_array` formula expresses the initialized state at `S[i]` as a *locally invertible* function of the preceding two full state words and seed word `KEY[(i−1) mod n]`. Set **`n=4`** (128-bit numeric integer seed). The four independent original-source inverse updates are:

| State update | Key residue mod 4 | Number of determined key bits |
|---|---|---:|
| `S[p+1]` from full `S[p−1],S[p]` | `p mod 4` | 32 |
| `S[p+2]` from full `S[p],S[p+1]` | `(p+1) mod 4` | 32 |
| `S[p+3].low31` from full `S[p+1],S[p+2]` | `(p+2) mod 4` | 31 |
| `S[p−172].low31` from full `S[p−174],S[p−173]` | `(p+3) mod 4` | 31 |

**All four seed words are recovered without any 32-bit brute force.** Only one missing highest bit in each of the two partial seed words remains, yielding **exactly four 128-bit numeric seed candidates per allowed phase**. This dual early/late completion is constructive; both state fragments independently require original printer/AX data but neither contains the disputed coupon or original acceptance digests.

## Original-source test and positive controls

The phase must permit the AX relative source at `p−402` and the last initialized-state word `S[p+3]`, which in the first MT cycle requires `402≤p≤620`. These are **219 possible absolute phases**, hence **876 fully specified 128-bit candidate seeds**.

Withhold the original source's **printer row33 fourth payload word** (zero-based word3), raw little-endian `910E0FB0`. The early AX construction consumes row33 words0–2, but **does not consume this fourth word**. It is the intact MT output at the independently source-relative index `p−3`. Generate `random.Random(seed).getrandbits(32)` through that index for each complete reconstructed seed and compare all 32 bits.

| Quantity | Actual result |
|---|---:|
| Original candidate absolute phases `p=402..620` | **219** |
| Actual fully reconstructed 128-bit seeds per phase | **4** |
| Total seeded intact-source predictions | **876** |
| Exact match to original withheld row33 word3 | **0** |
| Synthetic end-to-end seeds and source-window controls | **90/90 PASS** |

Each synthetic control uses an *actual Python `random.Random(128-bit integer)` instance*. It derives the early state via the same two-cycle twist inversions, the **three AX-like high16 checkpoints**, and row9 data; derives late low31 state values via independent 227-step paired outputs; reconstructs the four complete seed branches; and requires **exactly one branch** to reproduce its synthetically held-out row33 output. Control phases 402,404,430,535,562,620 and 15 separate integer seeds per phase cover early, later, and 624-output-cycle edge geometry. On the original retained bytes, all 876 candidates fail.

**Novel coverage versus the prior source-only n4 exclusion:** Agent18's [31-bit period169 key gate](h17-k04-extra-late31-seed-residue-gates.md) and [earlier initialized-state residue sieve](h17-k04-ax7778-31bit-seed-length-sieve.md) already excluded 87 n4 phases `p=535..621` using a *different low31 equality*. Our complete-key reconstruction adds the previously untreated **133 early phases `p=402..534`** and independently confirms 86 overlapping phases `p=535..620` by a 32-bit, held-out seeded output. `p=621` lies outside our `S[p+3]` first-cycle completion and must retain the earlier n4-specific source-conditioned exclusion, without claiming our own method covers it.

## Evidentiary limits and most valuable continuation

This is a **conditional full seed-class elimination** for `n=4, p=402..620`, under the common CPython producer and AX/printer stream placement. It does not establish that the real historic printer used any CPython generator, that AX checkpoints were generated contiguously from the same stream, or that six draws exactly separated row9 and row10. Larger numeric/string seeds, other phases/epochs, and unknown emitter algorithms remain possible.

Crucially, the source-controlled `S[p+3]` lower 31-bit witness combines with the earlier AX-derived `S[p−172]` lower 31-bit witness **in complementary key-index residues**. The same four-residue coverage trick can work for other key lengths **if an additional source region supplies sufficient independent residues**. It is more useful to seek another independently anchored initialized-state fragment or the missing paired target ancestor runs than to keep rerunning n4 hashes.

Original K04 coupon **not recovered**, K08 final exact phrase still unquoted, combined acceptance stays six PASS, K04/K08 MISSING and `accepted: false`. Unmodified original source and commitments preserved.
