# K04: seven source-derived CPython seed residues exclude additional array lengths

**Agent 26, 19 October 2026 ~14:48 UTC.** This is a source-conditioned **producer/seed-length** discriminator, not K04 coupon recovery. Original K04 selected row129, mask, commitment, K08 nonce and unchanged verifier were never read by the reproducer. The six established components remain accepted, K04/K08 remain missing.

## New cracking mechanism

Use the already source-pinned AX-7778/printer MT19937 recurrence alignment in which intact row34 begins at unknown absolute output phase `p`. Agent9/14 previously found initialized-state words at offsets `p-168`, `p-1..p+2`, `p+58..p+60` and source-derived trailing low31 words. This result applies **the same original 227-apart inverse-twist relation to the extended, fixed-point 12-row closure** and extracts three aligned initialized-state windows, including two previously underused edge words:

| Initialized pre-twist state | Original-source derived value |
|---|---|
| `S[p-168],S[p-167]` | `0A9DE247 FBBBB07E` (previously known) |
| `S[p-166] & 7FFFFFFF` | `2A07F662` (previously known) |
| **`S[p-2]`** | **`B30BF870`** (new usable left-edge word) |
| `S[p-1..p+2]` | `6CE0E225 F4E8FCB2 C517EB25 7D3AAF35` (known) |
| `S[p+3] & 7FFFFFFF` | `31FD69FC` (Agent14/18) |
| `S[p+58..p+60]` | `348ADB23 324EF3E1 353CCDFC` (Agent14) |
| **`S[p+61] & 7FFFFFFF`** | **`16DF5138`** (new usable right-edge partial word) |

The reconstruction uses only original printer rows `3,10,33,34,41,56,63,64,86,94,116,125` and the published joined phase assignment. All twelve source row payloads are intact; none is selected row129. The original spool SHA256 is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The AX source motivated this **conditional alignment**, but the additional bits here are algebraic consequences of existing intact spool words, not fresh independent external entropy.

For a CPython `Random(integer_seed)` with `n` 32-bit `init_by_array` seed words, three consecutive post-initialization state words ending at absolute index `i` invert to the unique `KEY[(i-1) mod n]+((i-1) mod n)` (mod `2^32`). The partial 31-bit state edges generate **two exact 32-bit candidate terms** (one for either unknown state MSB). Seven such key-term positions are available relative to `p`:

`[-166, 0, 1, 2, 3, 60, 61]`.

If `n` divides the difference of two listed offsets, the two corresponding key-term sets **must intersect**, independent of the unknown seed bytes. This avoids both seed enumeration and any acceptance-hash test.

## Exact original-source observations

Across every phase where the two relevant inferred state windows are genuine first-output-cycle `init_by_array` positions, **zero equal key terms** occur. In particular:

| Difference | Source-valid absolute phases | Distinct seed-array lengths implicated |
|---:|---|---|
| `166`, early edge→late left | `p=396..621` (226) | **83, 166** (also 1,2) |
| `169`, early edge→late right partial | `p=396..620` (225) | 13, 169 (independently covered by Agent18) |
| `226`, early edge→middle full | `p=396..563` (168) | **113, 226** (also 1,2) |
| `227`, early edge→middle partial | `p=396..562` (167) | **227** (also 1) |
| `57`, late right partial→middle full | `p=396..563` (168) | **19, 57** (also 1,3) |
| `58`, late→middle | `p=396..563` (168) | 29, 58 (also 1,2) |
| `59`, late→middle | `p=396..563` (168) | **59** (also 1) |
| `60`, late left→middle full | `p=396..563` (168) | 5,10,**15,20,30,60** (also 1,2,3,4,6,12) |
| `61`, late left→middle partial | `p=396..562` (167) | **61** (also 1) |
| `167,168` | `p=396..621` (226) | the 17 already published divisors |

All other neighboring offset comparisons with differences 1, 2 or 3 also give zero matches. They corroborate exclusion of already rejected tiny key arrays but add no new long-length class. **Every listed zero applies only to the explicitly stated phase domain**. In particular `n=5` was already constructively excluded for `p=396..563` by Agent14's four-candidate complete seed reconstruction; its appearance here is an independent modular test, **not a new original K04 component**.

The most distinct additional scoped exclusions are therefore `n=19,57,59,61,83,113,166,226,227`. Other listed lengths, including 15/20/30/60, gain simpler algebraic phase tests but have varying prior coverage in the shared seed literature. The original target projection is unchanged: **K04 coupon bits determined = 0**.

## Controls and reproduction

Standalone stdlib [reproducer](../agents/agent26/k04_seven_residue_gate.py) reads only the original case ZIP's SHA-pinned spool, reconstructs the three state windows, computes each feasible term set, and prints all 21 pairwise phase counts. It checks **144 actual seeded CPython positives**: 36 distinct seed-array lengths dividing one of the covered distances, independently generated `random.Random(int)` cases at four first-cycle phases `p=396,445,535,562`. For each synthetic case it compares recovered initialized-state windows against `random.Random(seed).getstate()` and verifies every applicable repeated key term. All 144 PASS. Original-source output shows **zero collisions across all 21 pair families**.

The initialized-state interpretation is **conditional** on the joined common-MT stream geometry, CPython's `init_by_array` producer and the stated first-cycle positions. It neither authenticates historical seeding nor excludes seeds at disallowed phases, longer unrelated key-array lengths, different RNG families or cross-epoch restarts. The first-cycle intervals crossing `p+60=624` and `p+61=624` are explicitly excluded where appropriate.

## Decision and next crack

Use the recovered edge words as direct reusable seed-period evidence. A source-grounded candidate seed recipe of one of these sizes can now be rejected cheaply at its eligible phases before any K04 target hash. For remaining seeds, the highest-value next step is to obtain a new independently placed initialized-state window or source-authenticated full-word run in K04's two hidden ancestor gaps. Repeating larger unordered string lists, printer mutants or complete six-slot acceptance replays will not supply those words. K08's original final caption remains unquoted in the local export.
