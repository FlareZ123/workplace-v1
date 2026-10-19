# K04: AX-7778 enables a second CPython initialized-state window spanning an MT output-cycle boundary

**Agent 9, 19 October 2026 ~10:53 UTC.** This is a new **constructive two-cycle seed-state inversion**, derived from already source-authenticated printer/AX-7778 checkpoint alignment, with a separate five-case seeded Python positive control. It is **not** a recovered K04 target or an accepted eight-component key. Reproducer: [`agents/agent9/k04_ax7778_cycle_seed_bridge.py`](../agents/agent9/k04_ax7778_cycle_seed_bridge.py). It reads a locally extracted original 43-member case export; selected printer row129, K04 mask, desk nonce, acceptance and verifier remain untouched and unread.

## New relation: invert a *second* twist through two adjacent source groups

[Agent 36's AX-7778 four-checkpoint MT bridge](h17-k04-transfer-checkpoint-16bit-bridge.md) fixes, **conditional on a shared MT19937 stream and the discovered source assignment**, intact printer **s64 − s34 = 227**. Its related source recurrence group also fixes **s10 = s34 − 170**. These relations supply an attack that had not been used by the first-cycle seed-fragment reports: two layers of inversion on the **same** source-pinned group, with one layer deliberately crossing MT's 624-output boundary.

For MT untempered output `X[t]`:

`X[t+624]=X[t+397] XOR twist(X[t],X[t+1])`

Let `p` be the **unknown absolute first MT output index of intact printer row34**. Define `Y[j]=X[p+j]` and inverse mixed input

`V[j]=untwist(Y[j] XOR Y[j+227])`.

The first inversion uses four intact source words from each row34 and row64, and reconstructs three full ancestral output words:

`Y[-396..-394] = BFD3ACA1 EF2DD8BC 611914B2`.

All three retemper to the **original AX-7778 positions 11–13 high16 checkpoints**, already source-confirmed by Agent36; the additional fourth source checkpoint selects the upper bit of `Y[-393]`. Crucially, `Y[-396..-394]` lie **227 output indices before the three source-recorded words `Y[-169..-167]` in row10**. A second application of the inverse twist to those paired words yields **two initialized-state words of CPython's pre-first-twist state** when the absolute phase is within the stated first-cycle bounds:

`S[p-168] = 0A9DE247` and `S[p-167] = FBBBB07E`.

These are **64 new initialized-state bits in a previously unconstructed window**; they are algebraic functions of previously source-reconstructed output words, not 64 *additional independent external evidence bits*. They must not be counted as newly independent constraints on an unrestricted MT recurrence state.

The known row3/34 five-pair bridge from Agent1 independently supplies `S[p-1..p+2]`:

`6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`.

The **new source-seeded-state geometry** therefore consists of two disjoint initialized-state windows, indices `p-168..p-167` (two words) and `p-1..p+2` (four words), both derived from original retained printer/AX transfer bytes, separated by **167 positions**. Existing single-cycle fragments recover only the later quartet; the new earlier two-word window is a potential **held-out nonlinear seed-initialization constraint** for future cycle-aware numeric or SHA512-expanded text-seed models.

## Positive control and phase restriction

Five *independent* synthetic CPython `random.Random(384_bit_numeric_seed)` cases use `p=535,555,584,605,621`. They explicitly sample an ordinary output stream through `p+231` then apply the **same two-stage inversion**, and compare each recovered word against a separately implemented CPython `init_by_array` initialized state. **All five cases pass**, including cases whose later inverse pair reaches the second output cycle.

The historical pre-spool phase is unobserved. Conditional on Agent48's isolated recorder prefix being chronological in the same generator, `s0≥292`. Original source printer graph has `s34−s0∈[243,297]`, so `p≥535`. If the first row3/34 initialized-state window belongs to the **first** 624-output cycle, its endpoint `p+2≤623` gives `p≤621`. Thus `p=535..621` is an explicit **conditional 87-phase window** for testing the two source-derived initialized-state blocks simultaneously. The window is not an unconditional claim about actual spool production; the recorder timestamps challenge on-demand chronological production. The new earlier window alone can be valid over a somewhat larger phase range.

## Information and attack limits

- The new pair currently has **no direct affine information about the four row129 output words**. The other joined original-source MT group containing row43/44 remains disconnected, and Agent47 already showed all 128 K04 target bits free for the unrestricted state under AX-7778 additions. **K04 target bits determined: zero.**
- Two isolated initialized-state words do **not by themselves supply a new integer seed word**. A length-specific `init_by_array` hypothesis must bridge the 167-step gap to the quartet, and then predict independent **intact original printer bytes** before a candidate K04 is tested. Arbitrary MT initial states need not satisfy such a seed restriction.
- The extra source words are a novel **derived seed-state window**, not a newly authenticated original source. AX transfer checkpoint order does not independently prove physical RNG production order or the historical seed.
- If the prefix/first-cycle hypotheses are false, the fixed initialized-state interpretation cannot be used as stated; the reconstructed **output** ancestors remain a valid conditional recurrence result.

Reproducer reads and SHA-pins only the untouched original spool and transfer-audit sources; it executes no original acceptance hash. It verifies the synthetic seeded-state identity at five distinct two-cycle placements, prints the source state words, and reports the lack of determined K04 bits.

**Research recommendation:** use this earlier window as a strict source-derived **seed-class/fingerprint discriminator** for a hypothesized producer, especially when row10→41 first-cycle inversion is invalid due to a positive recorder prefix. Before claiming target recovery, require a long-key seeded inversion linking these two windows or a new source observation that increases actual K04 target rank. The original REC8 result remains six PASS, K04/K08 MISSING, combined INCOMPLETE.
