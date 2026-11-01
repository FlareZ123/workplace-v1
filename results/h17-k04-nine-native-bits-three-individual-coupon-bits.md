# K04: nine native bits in two missing printer gaps determine three individual selected-word bits

**Agent 49, 1 November 2026. Exact conditional MT19937 target-ancestry result.** The supplied original contains **none of the needed native donor fragments**, and the common producer/chronology and the selected physical print remain unverified. **Recovered K04 target bits: 0/128. Recovered K08 final words: 0. REC8 remains six PASS, combined INCOMPLETE.**

## Original anchor and nearest prior work

The original printer spool is SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Original intact rows 43→44 are `PS-261003-0343` (10:35 UTC) and `PS-261003-0344` (10:40 UTC); rows 96→97 are `PS-261003-0396` (15:00 UTC) and `PS-261003-0397` (15:05 UTC). The disputed selected coupon is row 129, ESC-N / `PS-261003-0417` / RECOVER / ACK attempt 2 / 18:02 UTC.

The six pre-existing *original-payload-compatible but historically unauthenticated* single-MT19937 geometries [v2 Agent15](https://github.com/FlareZ123/workplace-v2/blob/main/results/h17-k04-six-model-ordinary-gap-causal-cut.md) and [v1 Agent5](../agents/agent5/k04_crosssource_six_vectors.json) place selected native word 0 at `p=950..955`, row43 word3 at `p-624`, four **unprinted** words `p-623..p-620` between rows43 and44, and four **unprinted** words `p-227..p-224` between rows96 and97. A source-model variant contradicts original CLASS/DEST controls; these six example placements are *not historical producer proof*.

The immediate predecessor is [Agent21's five-native-bit parity](h17-k04-five-native-bit-two-gap-parity.md), which obtains one XOR parity of two selected bits from five hypothetical printed bits in the two gaps. [v2 Agent15](https://github.com/FlareZ123/workplace-v2/blob/main/results/h17-k04-six-model-ordinary-gap-causal-cut.md) separately obtains four selected **parities** from seven hypothetical **untempered state** bits. This experiment identifies **three individual selected printed bits**, with a nine-bit union of native printed donor observations per word. It is a different observable and stronger kind of partial-output identification, while remaining wholly conditional.

## Exact sparse printed-bit identities

Let `X[t]` be a 32-bit untempered MT19937 output-state word and `Y[t]=temper(X[t])` its native printed word, with bit0 the least significant bit. Write `E=Y[p+j-623]` (early unprinted gap), `M=Y[p+j-227]` (middle unprinted gap), and `S=Y[p+j]` (authentic selected word), for **each j=0,1,2,3**. Standard MT19937 twist and temper give these identities for *every possible* 96-bit antecedent triple:

```text
S.bit0  = E.bit1 XOR E.bit4 XOR E.bit22 XOR M.bit0
S.bit4  = E.bit1 XOR E.bit5 XOR E.bit19 XOR M.bit4
S.bit22 = E.bit1 XOR E.bit19 XOR E.bit23 XOR M.bit22
```

**Only nine unique native printed donor bits are required per target word:**

- Early gap, six bits: **{1, 4, 5, 19, 22, 23}** of one specified native 32-bit output.
- Middle gap, three bits: **{0, 4, 22}** of its paired native output.

Each selected target bit needs four donor bits individually; bit4 and bit22 together need six total; all three need **nine total**. The entire three-equation system is independent of `X[p+j-624].bit31`: the antecedent high-bit coefficient vanishes for selected bits 0,4,22. Thus the same sparse identities apply to **all four selected words**, even where the predecessor high-bit itself falls into the first unprinted gap. Across eight independently indexed missing donor words, **36 selected native donor bit observations would fix 12 individually addressable selected coupon bits** (three in each word) under this exact MT chronology.

A direct exhaustive search over all 32 target printed bit positions, and all `C(32,k)` choices for `k=1,2,3`, minimizes the union of the needed two-donor native-bit supports. The exact minima within this isolated twist map are **4, 6, 9** bits, attained by `{0}`, `{4,22}`, and `{0,4,22}`. Since unknown predecessor high-bit contributions can only add requirements, while the minimizing subsets have zero such contribution, these are also complete isolated-map minima without observing the predecessor word. Other externally authenticated observations could change the minimization, but none is present.

## Frozen selected-copy discriminator for any authentic future donor

The surviving **unverified** copied 18:02 ACK and transcribed K04 mask can be reduced to three-bit comparator signatures, without ever using the original K04 commitment. Each signature below is in **bit0, bit4, bit22 order of a little-endian 32-bit word**, not a hex-digit substring. These signatures are **comparison targets**, not authenticated historical values:

| Selected word j | Copied ACK native word | Copied ACK b0/b4/b22 | Transcribed mask b0/b4/b22 | Copied XOR mask b0/b4/b22 |
| --- | --- | --- | --- | --- |
| 0 | `57DCA9A9` | `101` | `101` | `000` |
| 1 | `AEE2A531` | `111` | `100` | `011` |
| 2 | `21479C87` | `101` | `100` | `001` |
| 3 | `D559255C` | `011` | `111` | `100` |

If an independently authenticated MT/native-gap trace supplies the exact E and M donor outputs plus historical index and producer validation, the 12 reconstructed selected physical print bits can be directly compared to copied ACK signature sequence `101|111|101|011`. Any differing bit would falsify that copy under the authenticated source/copy model. Agreement on all twelve bits is **insufficient** to certify the remaining 116 coupon bits or any of the 128 mask bits. The final XOR signature is conditional on a second, independently authenticated commissioning mask. No source-absent donor values are inferred from these expected signatures.

## Validation and source/copy discrimination

[Standalone original-spool-pinned SFT](../agents/agent49/k04_three_native_target_bits_sft.py) deliberately does **not** read the selected row129 PAYLOAD, route mask, K04 commitment, K08 caption or nonce. It asserts the original spool hash, the four authentic intact gap endpoints and selected job identity. It tests the three equations on **all 97 GF(2) basis inputs** (zero plus one-hot each of the three 32-bit antecedent words), a complete certificate because MT twist/temper are linear over these inputs. It independently checks **120 true MT native-word cases** across five seeded CPython streams, the six selected index placements and all four word offsets, giving **360/360 individual bit equalities**. A second exact matrix-based support enumerator verifies the 4/6/9-bit minima. The locally executed read-only SFT passed all checks on the original 43-member ZIP.

**Target-facing falsifier:** If an *authenticated original* printer trace of both gaps supplies the nine exact native bits at the required locations, the three reconstructed printed bits must agree with the true physical 18:02 coupon under the common-producer placement. A disagreement with the retained selected spool copy would challenge that copy only *after* the historical producer, indexing, original trace integrity and copy-stage relation are independently established. Even an agreement certifies no other coupon bits. Reducing those printed bits through the K04 XOR mask would additionally require the independently authentic mask. The current source contains no such traces or certification.

The value of this result is a smaller, explicit native trace requirement for a potential authentic future acquisition; **it is not a newly observed K04 bit or a seventh passing component**. Do not use it to extrapolate a missing state stream, guess arbitrary donor values, renew source-free producer tests, or run a K04 commitment sieve without an original bridge.
