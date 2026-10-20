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

**Stronger six-word option:** If the independent historically indexed witness instead contains six consecutive words `X1410..X1415`, its final three still have the same 96-bit predeclared signature. Source-derived `(X957 XOR X1411) AND 9FFFFFFF = 8B3B35C1`, together with the full `X958 XOR X1412` relation, constrains **62 independent selected-coupon dimensions**. Specifically, `X957` has four possible untempered values after observing `X1411`, and `X958` is uniquely reconstructed from `X1412`; the earlier two coupon words remain unspecified. This 62-dimensional donor quotient was previously measured by Agent4's rank atlas; the new component is the **96-bit full-output suffix fingerprint** to vet that six-word index assignment *before* consulting its unknown donors. Do not confuse quotient dimensions with 62 individually fixed tempered bits.

Only **after** such an indexed original witness passes its predeclared suffix test should its first tempered 32-bit value `W` be untempered to `U`, and then

```text
X958 = U XOR 24D1E0F2
selected K04 fourth payload word = little_endian_4bytes(temper(X958))
```

would recover **32 actual selected coupon bits** in this one conditional chronology. An independently indexed `X1866` carrier would offer the second route `X958 = X1866 XOR 99F6810A`; two accepted donors must also obey `X1412 XOR X1866 = BD2761F8`, the prior exact source-derived consistency check. None of those future donors is actually in hand.

## Executed checks and current negative

The source-only calculation on the unchanged 43-member original export reproduces the full 15,305-rank basis, all five fixed future words above and both existing donor constants, plus the original full-source masked 30-bit `X957/X1411` difference. A local method-equivalent seeded control, independent of original data, tested CPython MT seeds **7, 198603, 8131**: at each seed all five predicted suffix words exactly matched the actual future generator words, and using the independently sampled donor `X1412` reconstructed the withheld selected `X958` word exactly. This is a **synthetic algorithm test**, not a recovered historical coupon.

The [new SFT](../agents/agent29/k04_future_suffix_witness_sft.py) preserves the source-only computation, exact expected signature, original row129 exclusion and three seeded tests. It imports the existing [source-pinned index955 SFT](../agents/agent29/k04_future_donor_sft.py), uses the saved [original-index fixture](h17-k04-source-consistent-index955.json), and is intended to run on the original ZIP. The calculation was executed locally in a method-equivalent Python session; a full repository-checkout execution of the newly committed import-based SFT is **not** claimed.

An independently preserved historical carrier that supplies 32-bit words at the specified future positions has **not been found**. Previous original 100-field recorder/procedure and 64-field AX source-carrier sweeps already yielded no authenticated future index1412/1866 donor. The new source-fixed suffix is useful for testing a *future newly received* 4-word or 3-word record; it does **not** justify re-searching the same unindexed original pools or treating a synthetic MT match as an observed external source.


## Stronger 160-bit content beacon: original future carrier need not have an independently logged absolute index

The same untouched-original state projector yields **five consecutive completely fixed future words at `X1418..X1422`**, only **six state draws after** target-informative unknown `X1412`. This is a qualitatively different evidence-acquisition capability: a newly received, contiguous *original* generator trace can be recognized by a highly distinctive known-output segment even if its historical sequence counter cannot be directly translated to global `X[1418]`.

| Stream index | Fixed untempered word | Fixed tempered output |
| --- | --- | --- |
| 1418 | `85BDFD0D` | `9CC93D80` |
| 1419 | `036F15CB` | `300760A8` |
| 1420 | `9955A20E` | `7606C13B` |
| 1421 | `066B505D` | `D4A5BA9E` |
| 1422 | `36C8808C` | `3C241095` |

**Predeclared content-match fingerprint**, 160 continuous output bits:

```text
9CC93D80 300760A8 7606C13B D4A5BA9E 3C241095
```

Little-endian raw 20-byte stream: `803DC99CA86007303BC106769EBAA5D49510243C`. Its values are derived wholly from original intact printer payloads in the same conditional index955 MT model, independent of the missing coupon, hash, mask, accepted six components or newly supplied external values.

For an independently authenticated future MT generator **contiguous 11-word run `X1412..1422`**, the final five outputs must match the beacon and the run's first word then fixes **32 actual selected-coupon bits** under `X958=X1412 XOR 24D1E0F2`. A contiguous **12-word run `X1411..1422`** also supplies the unknown `X1411` and its 30-bit source-affine `X957` relation, constraining **62** coupon dimensions. The original clock/index need not be numerically present in that *new* artifact if the 160-bit beacon and source provenance establish its relative position in the candidate contiguous generator trace. Without an original production-link witness, an exact numerical match would still not alone prove the generator historically produced the incident coupon.

A bounded byte-level test against every original member of the 43-file ZIP found **zero direct raw little/big endian, contiguous hex or base64 representations** of the 160-bit beacon; this is a new exact-fingerprint check with no loose phrase/word permutations, not a proof that no differently encoded or omitted future carrier exists. The new SFT asserts all five words and their synthetic exact MT future values as well as the earlier 96-bit suffix. This is an *independent-output source recognition opportunity*, with **0 actual new K04 bits** in the currently received evidence.

## Outcome and decision

**Actual new selected K04 coupon bits: 0/128; exact K08 final-caption words: 0; original REC8 combined status: INCOMPLETE.** This incremental result answers the missing `historically indexed future-state donor` question with a **specific 96-bit prospective independent-output fingerprint** and a precise conditional 32-bit extraction path. The current obstacle remains obtaining a genuinely original independently indexed target-bearing carrier or the original physical RECOVER coupon/keeper margin. Preserve acceptance, all original source bytes, and the distinction between conditional algebra and historical proof.
