# K04: complete source-only 160-bit CPython `init_by_array` first-cycle phase exclusion

**Agent 18, 19 October 2026 ~15:00 UTC. New exact 160-bit seeded reconstruction and independent original-source rejection at the final open boundary phase p564.** Prior Agents14/50 and our own p566/p621 results had closed every other phase. This report excludes the last case **without assuming AX-7778 transfer position10 immediately precedes position11** in the generator output stream. The source-pinned joined printer/AX geometry and single CPython first-cycle MT19937 producer remain conditional historical premises. Original printer selected ACK row129, original K04/K08 acceptance material, mask, nonce and verifier are unread, unchanged.

## New p564 crossing-cycle witnesses

Let `p=564` be the absolute initial `getrandbits(32)` output index of original intact printer row34 in the joined stream. Printer row10 lies at p−170 and row41 at p+57; their four intact 227-separated 32-bit MT untempered outputs invert to:

```text
S[621].high = 0
S[622] = 348ADB23
S[623] = 324EF3E1
X[0]  = 353CCDFC       (first generated untampered output)
X[1].low31 = 16DF5138 (new unspent cross-boundary partial)
```

The independent source initialized-state windows are `S[396]=0A9DE247`, `S[397]=FBBBB07E`, `S[398].low31=2A07F662` and `S[563..566]=6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`, `S[567].low31=31FD69FC`.

From `X0=S397 xor twist(S0,S1)`, with CPython `S0.high=1`, derive `S1.low31=2F1F9ABB`. The new `X1.low31` combined with independent `S398.low31` determines `twist(S1,S2).low31=3CD8A75A`. Both possible top-bit completions invert to **`S1.high=0`**, giving the *complete* source-only initialized state

**`S1=2F1F9ABB`.**

This low-index word, which Agent50's p564 boundary analysis had not reconstructed in full, enables inversion across CPython's exceptional **first-pass and second-pass initialization wrap**.

## Four complete key words by the previously unused wrap identity

Let `B` be CPython's ordinary 624-word seeded initialization base `init_genrand(19650218)`. The original late initialized quartet directly solves **KEY4** from update i565 and **KEY0** from i566. Its 31-bit trailing witness fixes **KEY1.low31**; the independent early pair and S398.low31 fix **KEY2.low31**. Agent50's p564 `S621.high` test fixes KEY2's top bit to 1, giving KEY2 completely.

The missing **KEY3** is exactly reconstructable because a **five-word** `init_by_array` key executes **624 first-pass iterations**:

1. The first first-pass iteration updates index1 with **KEY0**, producing `T1=(B1 XOR mix1664(B0)) + KEY0`.
2. The final 624th first-pass iteration wraps back to index1 and uses **KEY[623 mod 5]=KEY3** after setting its active index0 to the then-current first-pass P623: `P1=(T1 XOR mix1664(P623)) + KEY3 + 3`.
3. The second-pass last update also wraps index1. Reversing final S1 with final S623 recovers the prior first-pass `P1=(S1+1) XOR mix1566(S623)`. Separately, reversing the final second-pass update i623 with final S622 recovers the prior first-pass `P623=(S623+623) XOR mix1566(S622)`.

The equations have one solution for KEY3 (all arithmetic modulo 2^32):

```text
P1   = 66F6F879
P623 = 1882839F
T1   = 874C9E07
KEY3 = P1 − (T1 XOR mix1664(P623)) − 3
     = C8216162
```

Thus source-only observations now fix **four complete 32-bit seed words** and the low31 bits of KEY1. Exactly the two possible KEY1 high bits remain:

| Numeric seed word, low-order first | Candidate A | Candidate B |
|---|---|---|
| KEY0 | `87C39456` | `87C39456` |
| KEY1 | `14F6FDDB` | `94F6FDDB` |
| KEY2 | `9E2EBD55` | `9E2EBD55` |
| KEY3 | `C8216162` | `C8216162` |
| KEY4 | `4F2A90C0` | `4F2A90C0` |

There is **no** free 32-bit seed word and no key-space brute force. The two remaining seeds are obtained by algebraic inversion of the actual `init_by_array` algorithm.

## Independent original printer holdout rejects both

Reserve the untouched original **printer row33 first 32-bit word** as held-out evidence. Under the source-aligned printer geometry, row33 begins at first-cycle absolute output `p−6=558`. Its original tempered little-endian 32-bit output is `8F4C954C`. Neither row33 nor its payload was used to derive the seed candidates above.

Running actual CPython `random.Random(seed).getrandbits(32)` at index558 gives:

| Full n5 candidate | Predicted row33 word0 | Original intact row33 word0 | Source match |
|---|---|---|---|
| KEY1 high0 | `14068D57` | `8F4C954C` | **FAIL** |
| KEY1 high1 | `73DB8979` | `8F4C954C` | **FAIL** |

**Zero original candidates survive.** An independent earlier source check at printer row34 word0 also fails for both seeds, but the withheld row33 observation is a cleaner prospective discriminator outside the seed-inference record set.

The [read-only standalone p564 SFT](../agents/agent18/k04_n5_p564_wrapseed_completion.py) derives the initial-state windows by inverting **actual generator outputs** for **100 independently seeded 160-bit CPython numerical positives**. Every one is guaranteed to retain its *actual full seed* among the two algebraically reconstructed candidates: **100/100 PASS**. The source-only p564 two-key enumeration and heldout printer word check then fail 0/2, with exact hex values asserted.

## Entire first-cycle 160-bit source-only phase model closed

Combine this last p564 gate with existing independently source-target-free results:

| Absolute p interval / phase | Reference | Status for CPython n5 |
|---|---|---|
| 396..563 | [Agent14 three-window reconstruction](h17-k04-160bit-three-window-seed-reconstruction.md) | EXCLUDED |
| **564** | **This report: first/second init-loop wrap seed completion** | **EXCLUDED** |
| 565 | [Agent50 S0 mandatory high-bit contradiction](h17-k04-n5-boundary-567-elimination.md) | EXCLUDED |
| 566 | [Agent18 new X1/X2/X3 four-state branch contradiction](h17-k04-n5-p566-printer-only-exclusion.md) | EXCLUDED |
| 567 | [Agent50 exact i4 reverse step](h17-k04-n5-boundary-567-elimination.md) | EXCLUDED |
| 568..620 | [Agent14 crosscycle key3 discriminator](h17-k04-crosscycle-160bit-residual-phase-gate.md) | EXCLUDED |
| 621 | [Agent18 new X54 highbit contradiction](h17-k04-n5-p621-source-only-boundary-exclusion.md) | EXCLUDED |

**Every integer `p=396..621`, all 226 first-cycle phases, is now excluded for an exact five-word/160-bit CPython `random.Random(int)` seed by source evidence, without any additional assumption about contiguous AX position10→11.** The premise that original printer and the AX-originated state bridge belong to a common CPython generator remains unverified; other producer families, seed-array sizes and later-cycle phases remain open.

This closes a coherent candidate historical **producer family**, while it determines **zero of the four K04 coupon output words** and no K08 final caption words. Original acceptance remains **six PASS, K04/K08 MISSING, combined INCOMPLETE, `accepted: false`**. No original source or commitment changed.
