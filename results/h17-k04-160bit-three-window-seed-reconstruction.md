# K04: four-candidate reconstruction of a 160-bit CPython seed from three intact printer windows

**Agent 14, 19 October 2026 ~12:05 UTC. New source-conditioned constructive seed reconstruction; original K04/K08 remain missing.**

## Why this differs from previous seed and MT scans

Prior source-only inverse-twist work [Agent 9](h17-k04-AX7778-cross-cycle-seed-window.md) obtained two initialized-state windows of a hypothesized CPython `random.Random(int)` generator and no K04 target bits. The [new 31-bit partial-key gate](h17-k04-ax-seed-divisor-gate.md) extracted one overlooked high-bit-truncated state. This follow-up identifies a **second** overlooked 31-bit edge and a **third** initialized-state window, and uses their positions modulo a five-word seed to **complete the full 160-bit seed with two remaining binary choices**.

All values are from original intact printer row3, row10, row34, row41 and row64, in the source-aligned AX-7778 227-output-pair hypothesis. Source SHA256 and transfer SHA256 are pinned; selected printer row129 and all acceptance commitments are withheld. No K04 payload or K08 language guessing is involved.

## Original-source state observations

Let `p` denote the absolute first MT output index of intact printer row34. Under the AX-7778 printer model:

| CPython *initialized-state* observation | Source relationship | Value |
|---|---|---|
| `S[p-168:p-166]` | row34/64 inverse twist, paired with row10 suffix | `0A9DE247 FBBBB07E` |
| `S[p-166] & 0x7fffffff` | unused third inverse pair from row10 word3 | `2A07F662` |
| `S[p-1:p+3]` | intact row3/34 five-pair inverse twist | `6CE0E225 F4E8FCB2 C517EB25 7D3AAF35` |
| `S[p+3] & 0x7fffffff` | **new fifth inverse pair**, row3 word3 and row34 word2 | **`31FD69FC`** |
| `S[p+58:p+61]` | **new third window**, row10/41 four-pair inverse twist | **`348ADB23 324EF3E1 353CCDFC`** |

Here `S` is CPython's post-`init_by_array`, pre-output-twist 624-word initialized state. The third window interpretation requires `p+60<=623`, hence `p<=563`. The rest of this experiment examines all `p=396..563`, the initial-phase span in which these source-constrained windows can all be interpreted as first-cycle seed state. The especially relevant recorder-origin conditional range `p=535..563` is included.

## Exact key recovery: only two unknown bits

The CPython `init_by_array` recurrence inverts three consecutive complete initialized-state words to the corresponding 32-bit `KEY[(i-1) mod n]` without brute force. Two complete triples in the late quartet recover `KEY[p mod 5]` and `KEY[(p+1) mod 5]`. The third complete window recovers `KEY[(p+4) mod 5]` from the update at `i=p+60`. Separately, two initialized-state pairs plus a next-state low31 determine **31 bits** of the individual key for the corresponding update:

- Earlier edge `i=p-166` recovers `KEY[(p+3) mod 5] mod 2^31`.
- Newly recognized late edge `i=p+3` recovers `KEY[(p+2) mod 5] mod 2^31`.

All five key residues are thereby covered, 158 of 160 seed bits are fixed for each phase, and exactly **four** integer seeds remain (two unknown high bits). This is a source-only, nonlinear recovery algorithm over the real CPython initialization construction.

The [standalone SFT](../agents/agent14/k04_n5_three_window_seed.py) uses [the shared AX 31-bit module](../agents/agent14/k04_ax_seed_divisor_gate.py). Eight independent synthetic `random.Random(160-bit integer)` cases at `p=396,400,500,535,545,555,560,563` recover the **exact original seed**, uniquely among four 160-bit candidates when tested against the real synthetic state. All eight PASS.

## Original-source outcome

The source-only run at each `p=396..563` enumerated `4` fully specified 160-bit integer seeds:

- **168** absolute phase placements.
- **672** total complete 160-bit seeds.
- **0** reproduce all five intact initialized-state observations.
- Consequently **0** survive an additional intact row34 fourth-word holdout.

The first-cycle shared-MT CPython `Random(int)` model with five 32-bit key-array words is therefore **excluded over this precise 168-phase interval**, by independently source-grounded word relations and exhaustive 2-bit completion. This is not a universal exclusion of 160-bit seeds: `p=564..621` makes the third state window cross the 624-output boundary; producer topology, absolute alignment, caching, or generator family could differ. The AX-7778 checkpoint correspondence and recorder chronologies do not authenticate the exact physical RNG mechanism.

## Cracking value

This demonstrates how high-leverage **31-bit partial state observations** and a third initialized-state window solve an otherwise infeasible 160-bit seed-class problem with 672 inexpensive candidates, rather than relying on K04 hash volume. The surviving `p=564..621` interval is the most immediate **new** target: reconstruct a seeded-state window before the 624 boundary or bridge the cyclic successor without losing the source relationship. Another route is to test a different source-supported integer seed length with more diverse key-index residues, always requiring a held-out intact source word.

**Original acceptance unchanged:** six PASS, K04/K08 MISSING, combined INCOMPLETE, `accepted: false`. No original sources or verifier were mutated.
