# K04 source-fixed 96-bit suffix: authenticating a future donor before using its unknown first word

**Agent 29, 20 October 2026, ~09:04 UTC.** This is a new **target-adjacent, original-source-predicted witness authentication mechanism**, conditional on the already published source-consistent index955 common-MT chronology. It does **not** recover any currently missing coupon byte or quote the missing K08 caption. The historical generator/epoch and strict CLASS/DEST sampler are not authenticated; the selected layout has known conflicts with stronger producer assumptions. Do not promote it to source provenance without an independently indexed original witness.

## Concrete future-witness test

The exact `p=955` original-printer GF(2) basis is computed from **all 528 intact source payload words**, with disputed row129 wholly omitted. Its rank is 15,305. The prior target-directed equations give `X958 = X1412 XOR 24D1E0F2 = X1866 XOR 99F6810A`, for *untempered* MT19937 words. The new calculation reduces subsequent future-word expressions against those **original-source-only** equations. In this specific chronology, the original spool fixes the following *future* words **without reading row129 or the K04 hash**:

| Conditional state index | Fixed untempered state | Fixed tempered 32-bit value |
| --- | --- | --- |
| 1413 | `CFF3A43D` | `758243A9` |
| 1414 | `6F07E907` | `C4CA6CC8` |
| 1415 | `B81B7C89` | `BAE2035E` |
| 1867 | `81F4D6E4` | `7EC6E1CF` |
| 1868 | `E7D8B701` | `40A25EBF` |

**Target-first discriminating prediction:** If a *new, independently preserved, originally indexed* four-word MT output record is identified with its first word at `X1412`, its following three values, in normal 32-bit tempered numeric order, **must be exactly**
`758243A9 C4CA6CC8 BAE2035E`.
In little-endian raw serialized word bytes, those final 12 bytes must be
`A9438275C86CCAC45E03E2BA`.
For a three-word record beginning at `X1866`, the two-word 64-bit suffix instead must be `7EC6E1CF 40A25EBF` (little-endian `CFE1C67EBF5EA240`).

These are **source-derived predictions for withheld independent material**. They are deliberately computed *before* any putative future carrier is compared or its first, target-bearing word is used. An external suffix match would strongly discriminate a proposed exact MT stream index from arbitrary time-based or unindexed carrier assignment, although original provenance and production order would still need corroboration.

Only **after** such an indexed original witness passes its predeclared suffix test should its first tempered 32-bit value `W` be untempered to `U`, and then

```text
X958 = U XOR 24D1E0F2
selected K04 fourth payload word = little_endian_4bytes(temper(X958))
```

would recover **32 actual selected coupon bits** in this one conditional chronology. An independently indexed `X1866` carrier would offer the second route `X958 = X1866 XOR 99F6810A`; two accepted donors must also obey `X1412 XOR X1866 = BD2761F8`, the prior exact source-derived consistency check. None of those future donors is actually in hand.

## Executed checks and current negative

The source-only calculation on the unchanged 43-member original export reproduces the full 15,305-rank basis, all five fixed future words above and both existing donor constants. A local method-equivalent seeded control, independent of original data, tested CPython MT seeds **7, 198603, 8131**: at each seed all five predicted suffix words exactly matched the actual future generator words, and using the independently sampled donor `X1412` reconstructed the withheld selected `X958` word exactly. This is a **synthetic algorithm test**, not a recovered historical coupon.

The [new SFT](../agents/agent29/k04_future_suffix_witness_sft.py) preserves the source-only computation, exact expected signature, original row129 exclusion and three seeded tests. It imports the existing [source-pinned index955 SFT](../agents/agent29/k04_future_donor_sft.py), uses the saved [original-index fixture](h17-k04-source-consistent-index955.json), and is intended to run on the original ZIP. The calculation was executed locally in a method-equivalent Python session; a full repository-checkout execution of the newly committed import-based SFT is **not** claimed.

An independently preserved historical carrier that supplies 32-bit words at the specified future positions has **not been found**. Previous original 100-field recorder/procedure and 64-field AX source-carrier sweeps already yielded no authenticated future index1412/1866 donor. The new source-fixed suffix is useful for testing a *future newly received* 4-word or 3-word record; it does **not** justify re-searching the same unindexed original pools or treating a synthetic MT match as an observed external source.

## Outcome and decision

**Actual new selected K04 coupon bits: 0/128; exact K08 final-caption words: 0; original REC8 combined status: INCOMPLETE.** This incremental result answers the missing `historically indexed future-state donor` question with a **specific 96-bit prospective independent-output fingerprint** and a precise conditional 32-bit extraction path. The current obstacle remains obtaining a genuinely original independently indexed target-bearing carrier or the original physical RECOVER coupon/keeper margin. Preserve acceptance, all original source bytes, and the distinction between conditional algebra and historical proof.
