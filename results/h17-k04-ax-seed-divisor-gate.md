# K04: unused 31-bit second-cycle seed-state witness eliminates 17 CPython key lengths

**Agent 14, 19 October 2026 ~11:54 UTC. New source-conditioned nonlinear discriminator, not a K04 recovery.** All source records and original REC8 commitments remain unchanged. Source-only, read-only reproduction: [agent14/k04_ax_seed_divisor_gate.py](../agents/agent14/k04_ax_seed_divisor_gate.py).

## New observation

Agent 9's AX-7778 / intact printer reconstruction previously reported two separate CPython initialized-state windows for the conditional absolute row34 first-output phase `p`: `S[p-168:p-166] = 0A9DE247 FBBBB07E` and `S[p-1:p+3] = 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`. It did not use the **low 31 bits of the next initialized-state word**. That value is already present in the **third** exact inverse-twist pair joining inferred X[p-394] with intact printer row10's final output word X[p-167]:

`S[p-166] & 0x7fffffff = 0x2A07F662`.

The standalone reproducer independently extracts spool row10, row34 and row64 from the original ZIP (SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`), reconstructs ancestral states `X[p-396:p-393] = BFD3ACA1 EF2DD8BC 611914B2`, and evaluates the third pair. Transfer archive SHA256 `32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf` is pinned as provenance for the prior AX row34/64 alignment. The four late initialized-state words are pinned to Agent 9's published, independently source-derived source reconstruction. **Neither selected row129, K04 mask, REC8 acceptance commitments nor K08 caption/nonce enter this gate.**

## Nonlinear one-step phase test

For a hypothetical CPython `random.Random(int)` seed represented by `n` little-endian 32-bit key-array words, the ordinary `init_by_array` recurrence has `K[(i-1) mod n]` in the update for `S[i]`. The late quartet reveals two exact key words from triples, at key indices `p mod n` and `(p+1) mod n`. The earlier full pair then predicts the complete `S[p-166]` without knowing any other key word **if**

`(p-167) mod n = p mod n` or `(p-167) mod n = (p+1) mod n`.

Equivalently, **`n | 167` or `n | 168`**. Compare only the predicted low31 state bits with the third authentic inverse-twist pair. This is a 31-bit check of a nonlinear *seeded-state* relationship, stronger than a generic MT output-state consistency check. It adds no independent original evidence bytes; it uses 31 previously underexploited bits already implied by intact source pairs.

The synthetic control reconstructs all initial-state words via an independent pure-Python `init_by_array`, compares to actual `random.Random(seed).getstate()`, reconstructs the earlier pair and unused low31 observation from independent real MT outputs, and verifies the predicted state for **56** cases (8 phases 396,400,500,535,555,584,605,621 × 7 short key lengths). Every control PASS.

## Original-source outcome

Withheld original row129 and all commitments, scanned every integer phase **p=396..621 inclusive (226 placements)** in the first-cycle initialized-state interpretation. Every phase failed for all **17** distinct seed-array lengths dividing 167 or 168:

`1,2,3,4,6,7,8,12,14,21,24,28,42,56,84,167,168`.

For `n=1`, the two late key words themselves conflict at all 226 phases. For the other 16 lengths, their calculated next `S[p-166]` disagrees with the **0x2A07F662 low31 witness** at all 226 phases. Thus **3,842 phase/length assignments are eliminated** within this precise source/alignment/producer family, without enumerating unknown seed words or using a hash oracle. The source-only recorder-origin hypothesis restricts the especially relevant late-first-cycle range further to p=535..621; it is fully contained in this tested interval.

## Significance and limits

This is a new **nonlinear initialized-state source test** rather than another K04 payload mutation or six-slot replay. In particular, the 96-bit (`n=3`) and 128-bit (`n=4`) later-first-cycle seed variants can be rejected cheaply even though their missing key word(s) prevent direct reconstruction. For key counts **not dividing 167 or 168** (including n=5,9,10,11), the next update uses an unknown key word and this 31-bit one-step gate does not exclude them. Another independently placed original initialized-state triple or a stronger long-gap nonlinear solver is needed. Long-output-cycle variants where the interpreted windows no longer refer to CPython initialized state, other RNG families, non-integer seed construction, and unproven shared generator origins remain possible.

**Acceptance unchanged: K01/K02/K03/K05/K06/K07 PASS; K04 and K08 MISSING; combined INCOMPLETE, accepted false.** No original verifier run was requested or needed.
