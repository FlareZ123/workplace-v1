# K04: inversion recovers 30 complete unobserved MT19937 output words (source-only)

Agent 23, 19 October 2026. **New constructive positive source analysis, not a K04 commitment match.** Original spool `evidence/print/spool-reconstruction.log`, SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Reproducer: [`agents/agent23/k04_mt_inverse_peel.py`](../agents/agent23/k04_mt_inverse_peel.py) with original ZIP; it imports the source-only [42-witness reproducer](../agents/agent23/k04_mt_rowstart.py). The selected K04 payload row129 is explicitly **withheld** throughout; no acceptance hashes, K04 mask or nonce are loaded.

## Recovery identity

For untempered MT19937 words, the source-supported recurrence is

`X[k+624] = X[k+397] XOR T(X[k], X[k+1])`.

The 32-bit `T` mixes **one high bit of `X[k]`** with the **31 low bits of `X[k+1]`** and then shifts/XORs them. Consequently, two source-observed words at exact positions `k+397` and `k+624` reveal the entire 32-bit mixed input:

`z = X[k+624] XOR X[k+397]`

`lsb = z >> 31`

`mixed = (((z XOR (0x9908B0DF if lsb else 0)) << 1) | lsb) & 0xFFFFFFFF`.

The recovered `mixed` supplies `X[k]`'s high bit and `X[k+1]`'s 31 low bits. For **two consecutive** such known middle/end pairs, the supplied bit subsets overlap to reconstruct one entire missing untempered 32-bit word. No initial MT seed or brute force is required. Cross-record witness equations fix local relative stream positions in connected groups; outputs in different groups have no established absolute relative alignment.

## Original-source reconstructed values

The standalone program discovers all 25 within-row and 17 row-start witnesses while withholding selected row129, assembles connected row-start-index groups, and inversely propagates every pair of known outputs separated by exactly 227 positions. Across the connected groups it constructs:

- **30 full 32-bit output values** at positions absent from that connected group's input records; and
- **34 partially known 32-bit output values**, each with either the highest bit or the lower 31 bits.

These are group-relative reconstructed values and may overlap words in other groups whose offsets are currently unknown. Do not add them as 30 independently sampled original printer records or claim unique global stream positions.

A particularly relevant group anchors row44 at relative index 0 and includes row13 at -227, row67 at 168, row97 at 394, row130 at 620 and row131 at 624. It yields **six unobserved full words**, including these adjacent outputs immediately before row44's first observed word:

| Index relative to row44 | Full recovered untempered MT word |
|---|---|
| -2 | `27D820C7` |
| -1 | `0ACF4761` |

For instance, `X[621] XOR X[394]` gives the mixed input at index -3; `X[622] XOR X[395]` gives index -2; and `X[623] XOR X[396]` gives index -1. Stitching the high/low-bit pieces reconstructs the two full missing words above. Rows130 and97 are intact witnesses, not the selected target.

**Internal source consistency test:** Taking the *low 31 bits* of row44 word0 from `X[623] XOR X[396]`, and independently the *high bit* from `X[624] XOR X[397]`, reconstructs **`ED6D44FC`** exactly, equal to the original row44 word0 after untempering. This test did not use that row44 word as one of the two inputs to the reconstruction, although the relative alignment was discovered from source witnesses that included row44, so it is a post-selection consistency check rather than preregistered holdout evidence.

## Consequence for attacking the selected K04 ACK

The [new row-start gap bridge](h17-k04-mt-rowstart-gap-bridge.md) proves that for every of row129's four missing words, the directly required prior output at `q+j-623` lies in the unseen **row43→44 inter-record gap**, with index at most -4 relative to row44. The two newly reconstructed full words at -2 and -1 lie later in that gap. They therefore do **not yet** independently determine any row129 word. Nonetheless they provide actual source-derived state data at the far end of the precise missing interval, which can be fed to a model reconstructing the earlier gap words, rather than testing guesses for a seed or random byte corruption.

The inverse identity also allows a further productive line: use independently constrained relative alignments between connected row-index groups to reconstruct missing `X[-4]` through the row43→44 gap, then apply the recurrence to row129 with position/consumption rules inferred from intact records. 42 witnessed triples remain a model-conditional single-stream hypothesis, not a physical confirmation of the original generator's seed or historical source-layer integrity.

**Acceptance unchanged:** K04, K08 unresolved; no complete key; original original source bytes, verifier, acceptance commitments unmodified.
