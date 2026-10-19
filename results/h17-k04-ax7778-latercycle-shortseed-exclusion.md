# Later-cycle K04 seed inversion: AX-7778 six-word bridge rules out 32/64-bit integer seeds in a conditional phase window

**Agent 18, 19 October 2026 ~11:45 UTC. Source-conditioned negative for a new seed regime; no original K04/K08 key bytes.**

## Investigative change

Existing numeric CPython seed-fragment exclusions mostly treated 227-separated MT output pairs as wholly first-cycle and then inverted `init_by_array`. But source-linked TRP2 recorder-prefix placements put many of those pairs across the first MT twist boundary; earlier first-cycle eliminations cannot simply be reused for that model.

Agent 9's [AX-7778 cross-cycle source construction](h17-k04-AX7778-cross-cycle-seed-window.md) now provides two *independent-location* windows of pre-first-twist initialized-state words relative to the unknown row34 absolute MT output phase `p`:

- `S[p-168..p-167] = 0A9DE247 FBBBB07E`;
- `S[p-1..p+2] = 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`.

Under the published recorder-prefix and first-cycle alignment hypotheses, `p=535..621` (87 candidates). This is **later output positioning**, with a 227-offset pair crossing the generator's output-cycle boundary. The two windows are derived from intact original spool, AX-7778 checkpoints and previous source-pinned recurrence bridges. They are **not six independent new original-source words**.

## A complete short-seed inversion at those later phases

[Standalone Python standard-library SFT](../agents/agent18/k04_latercycle_shortseed.py) inverts two consecutive `init_by_array` seed words from the known source quartet, at each phase `p`, using the CPython mixing constants and indexed key recurrence from [Agent 1's first-cycle seed-word identity](h17-k04-python-initialization-inversion.md). For one 32-bit seed word, both derived values must agree. For two 32-bit seed words, they recover the complete 64-bit seed. Each candidate is independently regenerated using Python's actual `random.Random(seed).getstate()`; its four source quartet positions must match exactly. The disjoint early two-word window is reserved as an additional strict held-out test.

Five independently generated synthetic phases `p=535,555,584,605,621` for each of the 32-bit and 64-bit seed classes, **10 positive controls**, recover the original numeric seeds *exactly*.

| Seed class | Source phase choices | Reconstructed candidates that regenerate the late source quartet | Early-window matches |
|---|---:|---:|---:|
| CPython numeric 32-bit (`k=1`) | 87 | **0** | **0** |
| CPython numeric 64-bit (`k=2`) | 87 | **0** | **0** |

These are exhaustive across **the stated 87 absolute phases and two seed lengths**, without a brute-force loop over seed space. No original K04 selected ACK, route mask, REC8 digest, verifier, or K08 inputs are consulted. The original case bytes and commitments remain untouched.

## What this does and does not change

This excludes **a previously untested later-cycle placement of 32/64-bit CPython integer seeds** conditional on the original AX-7778/recorder alignment and the source-backed two-cycle state reconstruction. It is an informative *producer-class elimination*, not a K04 coupon or direct recovered target bit. It neither excludes 96-bit-or-longer integer seeds, SHA-512-expanded text/bytes seeds, an MT epoch after a restart, other generator implementations, other absolute phase placements, nor any departure from the cross-source ordering premise.

The same quartet exposes **two indexed key words for longer seed arrays**, so a source-derived constraint on a *third* adjacent initialized-state word or a verified producer seed recipe would enable a meaningful extension. The existing early pair supplies a held-out 64-bit consistency check, without claiming an independent seed-array word yet. Continued unbounded seed volume is not justified absent such a new anchor.

**Acceptance:** K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING; combined incomplete and not accepted.
