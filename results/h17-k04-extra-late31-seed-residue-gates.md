# K04: extra late initialized-state 31-bit witness excludes two seed lengths without AX-order assumption

**Agent 18, 19 October 2026 ~14:25 UTC.** Genuine source-conditioned CPython MT19937 `init_by_array` cracking result, with no original selected printer ACK (row129), K04 mask/commitment, K08 nonce or verifier used. The first-cycle / shared-PRNG printer grouping and its AX-7778 bridge are explicitly **conditional historical producer premises**. This report neither determines K04 coupon bits nor recovers K08.

## Previously underused direct source pair: S[p+3] low31

Take `p` as the absolute first MT output index of intact printer row34. The source-pinned joined geometry places row3 at `p−228`; in particular original intact spool **row3 word3** is untempered `D47006FA` at `p−225`, and **row34 word2** is untempered `CC8EB204` at `p+2`. The 227-output MT recurrence and its exact inverse give

```text
untwist(D47006FA XOR CC8EB204) = 31FD69FC
S[p+3] & 7FFFFFFF              = 31FD69FC
```

This is **31 bits directly present in an original intact-printer pair**. **Agent14 had already derived and used the same trailing-low31 witness in his 160-bit three-window/crosscycle gate** ([earlier result](h17-k04-crosscycle-160bit-residual-phase-gate.md)); the new contribution here is the independent all-phase **13/169 modular seed-length exclusion** plus the six-length conditional AX predecessor gate. It was not included in Agent9's published four-word initialized-state quartet `S[p−1..p+2]=6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`, whose fifth inverse mixed pair contains this trailing low31 value. It also appears in Agent50's near-contemporaneous boundary analysis of `p=566`; the new contribution here is a **different, all-phase seed-residue gate** using the 31-bit source observation.

For `396≤p≤620`, the source pair refers to genuine CPython initialized-state index `p+3≤623`. `p=621` is **excluded from this particular gate's test scope**, since index 624 wraps into the first tempered-output cycle and does not denote a valid initialized-state word. This removes a potential seed-stage off-by-one.

The other original two-cycle derived window is `S[p−168]=0A9DE247`, `S[p−167]=FBBBB07E` and `S[p−166].low31=2A07F662`, from original printer rows10/34/64 and independently aligned AX checkpoint records. The previously reconstructed quartet and early pair remain subject to the documented common-stream / first-cycle bridge premises; *this result does not assume the AX record at transfer position10 is chronologically contiguous with position11* for the first tier.

## Tier 1: printer-only independent heldout for key-array lengths 13 and 169

CPython `init_by_array` updates index `i` with key word at residue `(i−1) mod n`, with nonlinear odd-multiplier reversible mixing. The full initialized-state operands `S[p+1]`, `S[p+2]` and newly recovered `S[p+3].low31` recover exactly **KEY[(p+2) mod n].low31**, independently of its unknown high bit.

The early pair `S[p−168]`, `S[p−167]` uses **KEY[(p−167) mod n]** when predicting `S[p−166].low31`. These residues coincide exactly when **`n | 169`**. The two previously unexcluded positive divisors are **n=13 and n=169** (n=1 was already eliminated using the earlier source gate).

For every absolute `p=396..620` inclusive, the new late key-low31 determines an early third-state-low31 prediction. Compare against **independent original** `2A07F662`; no seed-word enumeration and no K04 acceptance digest is involved:

| CPython numeric seed-array words | Valid first-cycle phases | Low31 original-source matches |
|---|---:|---:|
| 13 | 225 | **0** |
| 169 | 225 | **0** |

This upgrades the previous Agent18 [backward checkpoint sieve](h17-k04-ax7778-31bit-seed-length-sieve.md#second-new-cross-cycle-gate-backwards-initialization--unused-ax-high16-19-october-1204-utc), which eliminated these sizes only under the **additional** assumption that transfer checkpoint position10 directly precedes position11 in the generator stream. The new Tier 1 does **not** require that extra local checkpoint-adjacency premise and covers a broader 225-phase first-cycle range instead of only p535..621. It still depends on the original cross-source MT alignment underlying the initialized-state windows.

## Tier 2: conditional local AX predecessor excludes six more sizes

The same late key-low31 residue is also the key for the **backward** update into `S[p−169]` when `(p+2) ≡ (p−168) mod n`, namely **`n | 170`**. For lengths `5,10,17,34,85,170`, enumerate the **two possible high bits** of that late key word. Each yields a complete reconstructed `S[p−169]`. The original earlier mixed inverse pair independently fixes that state's high bit; independently preserved original `X[p−170]` and the AX-7778 two-byte checkpoint `(seq=5,attempt=1)=537A` test the reconstructed predecessor under both unknown top bits of `S[p−170]`.

This test makes one **additional source-generation-order assumption**: AX transfer checkpoint position10 was the generator draw immediately before the already source-matched four-checkpoint run at positions11–14. It does **not** require all 16 AX checkpoints to be globally contiguous or assume any source creation chronology beyond that local adjacency. If that predecessor assumption is false, this exclusion does not apply.

| CPython key-array lengths | Valid first-cycle phases | Surviving highbit **and** AX-high16 matches |
|---|---:|---:|
| 5, 10, 17, 34, 85, 170 | 224 each (p397..620) | **0 for every length** |

The `p=396` boundary cannot have source position `p−397≥0`, and p621 is outside the valid initialized-state trailing-low31 window. This Tier 2 usefully narrows Agent50's residual n5 phase 564/566 branches **under the extra AX local-adjacency hypothesis**; it does not contradict his source-only statement that they have not been eliminated without that assumption.

## Reproducibility, controls, limits

- [Read-only SFT](../agents/agent18/k04_extra_late31_residue_sieve.py) imports existing original-SHA-pinned [first Agent18](../agents/agent18/k04_ax_31bit_seed_sieve.py) and [backward Agent18](../agents/agent18/k04_ax_backward_checkpoint_sieve.py) modules; derives the new low31 directly from untouched printer rows3/34; reads original transfer audit only for Tier 2. The source original hashes and direct untempered source words are asserted. Original selected row129 is not accessed.
- **40 actual CPython random.Random seeded positive cases**: 2 word lengths × 5 phases for Tier1, 6 word lengths × 5 phases for Tier2, all passing. A separate independent local all-in-one derivation including iterative full-state source closure reproduces `31FD69FC` and **all eight zero-match tables**, likewise with 40 actual seeded positives.
- Inference applies only to CPython's **first initialized-state cycle** at the conditioned absolute output phase, under the established single-generator source positioning. Other seed lengths, C++ `seed_seq`, alternate generators/seed stages, advanced cycles, restarted streams, and false AX or spool alignment all remain open. Neither tier reveals K04 original coupon bytes or K08's missing final caption.

**Original accepted REC8 state unchanged:** K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING; combined INCOMPLETE, accepted false. No original source record, original acceptance commitment or verifier was altered.
