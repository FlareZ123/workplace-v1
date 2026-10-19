# K04: algebraic 224/256-bit CPython integer-seed stitching from separated MT state windows

**Agent 8, 19 October 2026 ~06:40 UTC.** This is a new, bounded **source-conditioned cracking method and negative result**, not an accepted K04 component. Reproducer: [`agents/agent8/k04_seed_stitch.py`](../agents/agent8/k04_seed_stitch.py); run with the original 43-member local H-17 ZIP. Selected original spool row129 is excluded by the underlying witness parsers; the experiment neither reads K04/K08 commitments nor K04 mask. Source spool SHA-256: `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.

## Novel algebraic bridge

Agent 1 previously reconstructed four short runs of seeded-state MT19937 words from 227-output-separated source-only pairs, and directly excluded selected first-cycle **one- through six-word (32–192-bit)** CPython numeric seed-array assignments. Its earlier method did not reconstruct all eight words of a hypothetical 256-bit integer key. This investigation uses the same independently anchored row3, row10, row13, and row14 runs and **adds the three-pair initialized-state run anchored to original intact row11**.

For CPython `init_by_array` in its first initialization cycle, write successive initialized-state words as `I[i-2], I[i-1], I[i]`, with fixed `INITIAL[i]` and key-array index `k=(i-1) mod key_length`. The exact recurrent expression inverted by the reproducer is:

```text
first  = (I[i-1] + i - 1) XOR (((I[i-2] XOR (I[i-2] >> 30)) * 1566083941) mod 2^32)
second = ((INITIAL[i] XOR (((first XOR (first >> 30)) * 1664525) mod 2^32))
          + KEY[k] + k) mod 2^32
I[i]   = (second XOR (((I[i-1] XOR (I[i-1] >> 30)) * 1566083941) mod 2^32)
          - i) mod 2^32
```

Both multipliers are odd, so have modular inverses mod `2^32`. Given a known key word, the recurrence advances two state words forward or reverses two state words backward **exactly**. Where two reconstructed state windows bound a contiguous run of at most **two adjacent unknown key-array updates**, reverse the right-hand window, advance the left-hand window and algebraically derive both unknown 32-bit key words. That is a constructive recovery of 64 missing key bits with **no enumeration of their values**. It is useful for 224- and 256-bit seed classes and may generalize to additional source windows.

Synthetic end-to-end controls generated with actual `random.Random(seed)` for both seven- and eight-word distinct integer seeds reconstruct the exact seeded state, recover all key words and reproduce the original integer seed. The test withholds **row34's fourth 32-bit payload word** from seed-fragment reconstruction: it lies at phase `pa+232` and is not one of the five inferred 227-spaced input pairs. Every complete candidate is checked against that original held-out intact word, using an independent CPython `random.Random(seed).getrandbits` implementation before further observed-pair checks. The source-only full-word holdout rejects all tested candidates. This control was rerun after correcting an earlier quick check that had reused the already-inferred first pair word.

## Source-conditioned bounded output

This search uses Agent 1's existing four-group relative-phase ranges, together with the row11 three-pair group. Key fragments from the four original groups must not conflict before trying the two-window bridge. A `full seed candidate` means that a phase assignment's recovered key dictionary covers all key words; it is **not** an accepted historical seed or unique integer.

| CPython integer seed class | Four-group phase-compatible assignments | Complete seeds from row13→14 short bridge | Complete seeds from row10→11 short bridge | Exact retained-source matches |
|---|---:|---:|---:|---:|
| 224-bit / seven key words | 29,916 | 0 | 0 | 0 |
| 256-bit / eight key words | 43,218 | **4,437** | **118,426** | **0** |

The n=7 scan considered 17,281 and 441,492 short-bridge phase assignments at the two boundaries respectively. For n=8, it considered 23,223 row13→14 short-bridge assignments, plus 648,270 row10→11 short-bridge assignments. Across both n=8 bridges, **122,863** complete reconstructed seed assignments failed an independently evaluated retained-source MT output (some assignments or seeds may recur between branches). The upper phase windows are deliberately bounded at **18 generator positions** and may contain possibilities that the particular two-unknown contiguous-block inversion cannot close. Consequently **this does not exclude the entire 224-/256-bit first-cycle seed family**. It directly excludes the completed candidate set under the first-cycle CPython numeric-seeding and existing source-position assumptions. It does not say anything about a string seed, entropy-seeded MT, later cycle, a different source generator, longer integer seeds, or source-layer integrity.

## New link to CLASS+DEST producer geometry

Agent 6's pre-payload CLASS selector and Agent 2's post-payload DEST selector make **six MT words per ordinary source record** a plausible conditional floor (four payload outputs and at least one draw for each selector). Integrating this floor into all 42 source-only recurrence equalities using standard shortest-path difference constraints gives an **exact maximum chronological start distance of 18 outputs** for each of row10→11 and row13→14. Under the weaker generic four-word floor, those upper distances are 60 and 62; under a five-word floor, 39 and 40. The min-six bounds justify looking at these two windows as a priority **if** the same two-selector producer logic holds uniformly on ordinary rows. They do not prove that logic was used in the original printer, and a short gap does not guarantee that two-window inversion recovers the missing key words.

The important structural distinction: a 256-bit key space that is infeasible to enumerate directly can be converted into a small source-phase compatibility problem plus an algebraic bridge, provided the available windows flank the unresolved key words. The next useful step is to add other partially recovered row-start windows or generalize the bridge for separated unknown key updates, then infer a source-consistent key and predict intact tail words *before* attempting any K04 commitment check.

**Acceptance:** K04 and K08 still missing; no complete eight-slot key; original source and REC8 commitments unchanged.
