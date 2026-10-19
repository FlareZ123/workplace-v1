# K04: first-cycle reference MT19937 `init_genrand` excluded algebraically

**Agent 47, 19 October 2026 ~06:54 UTC.** Source-pinned negative discriminator, not a recovered K04 coupon. Read-only reproducer: [`agents/agent47/k04_initgenrand_gate.py`](../agents/agent47/k04_initgenrand_gate.py). Original 43-member ZIP printer spool SHA-256: `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Selected row129, K04 acceptance hash and XOR mask, and K08 nonce/commitment are all excluded.

## New source-conditioned seeding-family test

Agent 1 previously reconstructed five-pair and four-pair 227-draw-separated MT19937 output runs, then inverted **CPython `init_by_array` integer seeds** of 32–192 bits. This independent test instead asks whether the recovered seeded-state windows can come from the reference MT19937 **single 32-bit seed `init_genrand`** used by the standard reference C generator and the scalar-seeded `std::mt19937` family.

Under the assumption that the 42 source-discovered MT19937 witness alignments identify the **first 624 outputs after standard initialization**, each pair of original untempered output words `X[p], X[p+227]` algebraically reveals one high bit of seeded-state `I[p+227]` and the 31 low bits of `I[p+228]`. Five consecutive such pairs recover four adjacent seeded-state words without their absolute phase or seed.

The classic `init_genrand` seeding recurrence requires each adjacent seeded-state pair to obey:

```text
I[i] = (1812433253 * (I[i-1] XOR (I[i-1] >> 30)) + i) mod 2^32
```

Consequently, subtracting the nonlinear multiplication from each neighboring reconstructed word pair must give **the small physical seeded-state index `i` in 1..623**. This is a direct arithmetic test of the seed family, without enumerating seed candidates or consulting the K04 target.

| Intact source row anchor | Recovered consecutive seeded-state words (hex) | Implied required `i` per adjacency |
|---|---|---|
| 3 | `6CE0E225 F4E8FCB2 C517EB25 7D3AAF35` | 1211007102, 3776610384, 2011796279 |
| 10 | `348ADB23 324EF3E1 353CCDFC` | 1716241426, 2221681975 |
| 13 | `3880F01D 6D1A1F58 F3F2CCC0 CCAB65DC` | 1425071847, 2255408547, 3237429741 |
| 14 | `34219D2E 477213AE 51440BF4` | 80704136, 3069223145 |

All ten implied indices are outside 1..623, including the smallest, 80704136. **A single adjacency suffices to falsify this family under the first-cycle interpretation.** Four separately source-anchored runs supply redundant checks.

## Synthetic control and limitations

The reproducer implements the reference 624-word `init_genrand` seeding recurrence, in-place standard MT19937 twist, exact inverse-twist reconstruction, and the index test. It tests three known 32-bit seeds (`1`, `0x12345678`, `0xFFFFFFFF`) at four first-cycle phases each (0, 30, 100, 390), and verifies all 12 reconstructed windows match the actual initialized state and yield the correct consecutive seed-state indices.

This rejects **only the reference single-32-bit-seed, first-cycle MT19937 initialization** for the existing 42-witness common-stream interpretation. It does not exclude CPython's different `init_by_array` path, longer/multiple-word `seed_seq` families, a stream advanced beyond its first twist cycle, a distinct generator, or malformed source. It provides no selected row129 output word and no original acceptance PASS.

**Cracking implication:** there is no reason to brute-force the classic 2^32 reference MT seed under this source hypothesis. Prioritize inverse recovery of the shared larger seeded state, or metadata-supported stream-index equalities that bridge the row43→44 target-ancestor gap. Original source, verifier and commitments remain unchanged. K04/K08 MISSING.
