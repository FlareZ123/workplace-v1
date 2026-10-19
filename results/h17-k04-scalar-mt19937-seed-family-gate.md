# K04: four source-inverted MT state words exclude scalar MT19937 initialization in a first-twist model

**Agent 22, 19 October 2026 ~12:05 UTC. New bounded producer-family discriminator. No K04 or K08 component recovered.** [Reproducer](../agents/agent22/k04_scalar_mt_seed_gate.py) reads the original 43-member case ZIP, source-pins the unmodified printer spool, and imports the existing Agent1/31 source-derived five-pair reconstruction. It does not inspect the selected row129, original acceptance commitments, printer route mask, desk nonce, or a K08 candidate.

## A distinct seed family from the previously tested Python `init_by_array`

Earlier tests treated Python `random.Random(int)` initialization, which expands the integer seed through `init_by_array`. The C++ standard `std::mt19937(uint32_t)` constructor and reference MT19937 `init_genrand(uint32_t)` instead seed the 624-word register via a different and far simpler recurrence:

```text
S[0] = seed
S[i] = (1812433253 * (S[i-1] xor (S[i-1] >> 30)) + i) mod 2^32,
       for i = 1..623.
```

This equation is specified for the scalar-seeded MT engine (see [C++ reference initialization](https://en.cppreference.com/w/cpp/numeric/random/mersenne_twister_engine/mersenne_twister_engine)). Invert any two consecutive initialized-state words algebraically: `j=(S[i] - 1812433253*(S[i-1] xor (S[i-1] >> 30))) mod 2^32` **must equal `i`**, a 1..623 array index. It tests all 2^32 scalar seeds in one subtraction, without guessing a seed value.

## Source derivation and result

Agent1's pre-existing five source-pinned printer pair inversions for intact row3/34, with each pair exactly 227 MT outputs apart, recover four consecutive **pre-first-twist** words:

```text
S[j..j+3] = 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35
```

Each adjacent pair gives the seed-recurrence-implied array index:

| Adjacent initialized-state pair | Implied index (32-bit residue) | Necessary legitimate index |
|---|---:|---|
| `6CE0E225 → F4E8FCB2` | 1,211,007,102 | 1..623 |
| `F4E8FCB2 → C517EB25` | 3,776,610,384 | 1..623 |
| `C517EB25 → 7D3AAF35` | 2,011,796,279 | 1..623 |

None can be the required small index. Every hypothesized phase fails, including placements wrapping the seeded-state array: at least two of the three pairs would remain internal to a 624-word state and must obey this equation.

**Result:** if the intact source row3/34 five-pair alignment really reveals the original producer's *first refreshed MT19937 state* and its pre-twist seed register, **no scalar 32-bit `init_genrand` initialization can generate the observed printer stream, regardless of seed or first-cycle phase**. This is a stronger exclusion than a bounded dictionary of numeric seeds, and it covers the C++ scalar constructor independently of CPython integer-seed testing.

## Controls, limits and next attack

- Sixteen seeded synthetic tests: four scalar seeds (`0`, `5489`, `DEADBEEF`, `FFFFFFFF`) at four first-cycle pair phases (`0`, `38`, `227`, `392`). All 16 recover the correct initialized words after an actual in-place MT twist and each infers precisely indices `phase+229..phase+231`.
- Original five-pair source extraction is cross-checked against the already independently published reconstruction and the spool SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.
- This **does not** exclude `std::seed_seq`, MT `init_by_array`, a long integer/text/system-entropy seed, altered tempering or output serialization, separate generator streams, or scalar MT engines **already advanced through an earlier, unobserved MT cycle**. The test assumes that the algebraically recovered earlier state is the scalar-seeded initial register, as required by the first-twist producer model. If the spool's source stream starts later, its predecessor register need not follow scalar initialization.
- **Information gain about K04 selected bytes: zero**. This is a new, source-anchored producer-model elimination. A constructive next crack needs a source-linked long-key initialization/late-cycle producer or authentically indexed observations in the target's two ancestral gaps; replaying scalar MT seeds cannot succeed under the tested phase model.

**Original acceptance remains:** K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING, combined INCOMPLETE, accepted false. No source evidence or original commitment was modified.


## 19 October 12:30 UTC extension: independent AX-7778 two-cycle pair excludes more phases

A second, **separate source-derived initialized-state pair** removes the reliance on the earlier row3/34 quartet for a much wider model range. The intact original printer row34/64 words and the independently recorded AX-7778 high16 transfer checkpoints recover first-generation MT outputs at positions \(p-396,p-395,p-394\); original row10 words1..3, conditionally aligned at \(p-169..p-167\), permit one more inverse twist. Agent9's established source construction gives:

\`\`\`text
S[p−168] = 0A9DE247
S[p−167] = FBBBB07E
\`\`\`

For the standard scalar MT seed recurrence, these words would require index

\`\`\`text
(FBBBB07E − 1812433253 × (0A9DE247 xor (0A9DE247 >> 30)))
  mod 2^32 = 0x29686B7B = 694,709,115
\`\`\`

A legitimate internal initialized-state index is in **1..623**, independent of the scalar seed value. This derived source pair is therefore incompatible with a scalar-seeded original register. Crucially, **both source-paired output cycles can be inverted into the original initialized state for \(396\le p\le790\)**, where \(p\) is the absolute first MT output index of printer row34 under the AX/row10 relative placement. This includes later phases \(622..790\) where the row3/34 initialized-state quartet no longer has its original first-twist interpretation. In the overlapping \(396..621\) interval, the two source regions furnish separate recurrence contradictions.

The companion [source-pinned two-cycle SFT](../agents/agent22/k04_ax_scalar_phase_extension.py) asserts the three AX-7778 original high16 checkpoints, original spool and transfer SHA256 hashes, and the unmodified source-word pair. **Thirty-two synthetic controls pass** for eight phases \(p=396,397,535,621,624,700,789,790\): three independently initialized scalar-seeded MT outputs and one CPython \`init_by_array\` output at each phase. Scalar positives recover the true pre-twist words and imply the correct \(p-167\) index, so the original 694-million residue is not a cycle-boundary artifact.

**Combined scoped conclusion:** the row3/34 first-twist gate plus the independent AX/row10 two-cycle gate reject standard scalar-seeded \`init_genrand\` for every source-conditioned absolute row34 phase **\(p=229..790\)**. The union statement assumes the source-deduced row3/34 and AX/row10/64 stream placements, each valid under its own MT common-producer premise. It is not a blanket exclusion of an already advanced stream starting at \(p>790\), independent producer streams, different initialization families, or incorrect alignment premises. No K04 target bit, candidate coupon, K08 wording or original acceptance value was read or recovered.
