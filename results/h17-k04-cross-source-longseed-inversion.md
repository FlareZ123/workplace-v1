# K04: cross-source initialized-state windows and 288–352-bit CPython seed inversion

**Agent 7, 19 October 2026 ~07:12 UTC.** This is a new source-conditioned cracking method and bounded negative result, not a recovered K04 printer coupon or an accepted REC8 slot. [Read-only reproducer](../agents/agent7/k04_cross_source_longseed.py), original surviving H-17 ZIP, selected printer row129 completely withheld from MT reconstruction. All source bytes, acceptance commitments, and original verifier remain unmodified.

## New input: the recorder/RC-17 state words extend CPython initialization windows

[The separate full-word control analysis](h17-k04-cross-source-fullword-upgrade.md) found five *independently reconstructed* 32-bit ancestral MT state words agreeing with all 32 bits of the original auxiliary control bytes. Four more control values reveal the formerly unknown highest bit conditional on the hypothesis that these cross-equipment fields are full state words, not merely accidental matches of their low 31 bits.

Crucially, two of those conditionally promoted high bits continue *existing* 227-output-spaced MT inversion windows into **four adjacent initialized-state words**:

| Source-relative pair anchor | Initialized-state words in one consecutive run | First-cycle numeric seed-array updates obtainable |
|---|---:|---:|
| printer row3, predecessor pair | 4 | 2 |
| printer row10, pair starts at payload | 4 (fourth from TRP2 record45, CRC-valid) | 2 |
| printer row13, predecessor pair | 4 | 2 |
| printer row14, predecessor pair | 3 | 1 |
| printer row28, predecessor pair | 4 (fourth from withdrawn Rev B PURGE strip) | 2 |
| **Total** | **19** | **9** |

The original 42 MT printer witnesses fix five short relative group alignments. Three earlier cross-source recorder/RC-17 pair matches link additional groups. Applying the independently proposed conditional floor of six RNG draws per ordinary printer row (four payload + one CLASS + one DEST) to those exact difference constraints yields the following **relative** first-pair phase windows, with spool row0 payload start defined as zero:

```text
row3  = 20..24       row10 = 74..84
row13 = 101..111     row14 = 109..119
row28 = 207..211
```

All pairwise distance constraints admit only **2,799 simultaneous relative phase tuples**. These windows and the six-draw floor remain *model assumptions*, not authenticated historical printer source code.

For first-cycle CPython `random.Random(integer_seed)`, the three successive initialized-state words `I[i-2], I[i-1], I[i]` invert the two `init_by_array` mixing rounds and recover the key word at slot `(i-1) mod n`. Agent 1 introduced that inversion and Agent 8 introduced algebraic bridging across one or two unknown adjacent key updates; the fresh improvement here is using the independent TRP2/RC-17 controls to gain **two more complete, separated, initialized-state seed constraints**. Nine key-word indices can now be recovered under compatible phase placements, so a **288-bit numeric integer seed** is reconstructable without enumerating 288 bits. For 320-/352-bit seeds, the reproducer also attempts Agent 8's existing short-window bridge across row13→14 or row10→11.

## New global phase offset, not previously fixed at spool row0

A further improvement is **not assuming the first printer payload was generated at the beginning of the CPython output cycle**. For each of the 2,799 relative phase tuples, the reproducer tries all nonnegative whole-output global offsets that retain the five observed initialized-state windows inside the first 624-output cycle. This evaluates **513,553 phase-and-offset assignments for each seed class** (up to offset 185).

Every reconstructed complete seed is checked against an original intact spool word, **row34 payload word3**, withheld from seed-fragment fitting and key-bridge construction. This is an output prediction: all 32 tempered bits must agree, without consulting K04/K08 commitments, the selected row129 payload, or source-dependent mask candidates.

| CPython integer seed size | First-cycle phase+offset placements | Fragment-compatible placements | Complete reconstructed seed assignments | Held-out output matches |
|---|---:|---:|---:|---:|
| 288-bit, 9 words | 513,553 | **2,022** | **2,022** | **0** |
| 320-bit, 10 words | 513,553 | **6,986** | **0** with the two tested bridges | **0** |
| 352-bit, 11 words | 513,553 | **7,110** | **8,935** across the two bridges | **0** |

The 352-bit bridge may reconstruct the same assignment more than once from different routes; counts above are **candidate assignments**, not necessarily distinct numeric seeds. The 320-bit row13→14 bridge was attempted 6,986 times and row10→11 18,185 times, without a complete candidate. For 352 bits, 7,110 and 23,884 bridge attempts respectively produced 2,188 and 6,747 complete assignments. All 8,935 complete assignments fail the held-out word.

The reproducer includes actual Python `random.Random(seed)` synthetic positive controls for **288, 320 and 352 bits**, recovering the exact integer keys, including the more difficult n=10/11 bridging cases.

## What this establishes, and what remains

1. **Constructive:** Independently preserved control fields can extend inferred MT initialization runs. The original *source evidence* yields two additional 32-bit key-array constraints, elevating the direct algebraic reconstruction to nine seed words.
2. **New bounded exclusion:** Under the explicit first-cycle CPython integer-seed, six-draw-floor and full-control-word hypotheses, the exhaustive 288-bit phase/offset scan yields **no source-consistent seed**. For 320- and 352-bit arrays the specific tested bridge family yields no held-out match; unbridged assignments remain unresolved.
3. **Unexcluded:** 384+ bit numeric keys, `str`/`bytes`-derived CPython seeds, alternate generator implementations, later output cycles or nonuniform draw histories, missing or incorrect source controls, and any scenario violating the proposed six-draw floor. In particular, recorder/RC-17 control values are not authenticated as printer PRNG state by the historical records.
4. **Next targeted crack:** Add additional independently labelled cross-source initialized-state words, or generalize the algebraic bridge to **three or more separated unknown key-word updates** for a 384+ bit source seed. Use surviving intact tail outputs for prospective checking before deriving selected K04. K08's exact final keeper caption remains separately missing.

**REC8 acceptance remains unchanged:** K01/K02/K03/K05/K06/K07 PASS; K04 and K08 MISSING; combined INCOMPLETE, accepted false.
