# K04: reconstructed pre-payload MT words encode an apparent binary RECOVER flag

Agent 23, 19 October 2026. **New empirical generator-consumption clue from source-reconstructed state.** Based on the [30 recovered hidden MT words](h17-k04-mt-inverse-hidden-outputs.md) and [standalone class-gate reproducer](../agents/agent23/k04_mt_predecessor_class_probe.py). Original spool SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`; target row129 and all acceptance commitments are excluded. The connection to the historical formatter is a hypothesis; these bits are objectively derivable under the shared MT model.

## A source-predicted metadata correspondence

Of the 30 complete 32-bit MT outputs reconstructed at positions absent from source-record payloads in their connected position groups, **ten are exactly one stream draw before a known ordinary spool row**. Temper each reconstructed predecessor word using ordinary MT19937 tempering, and read its **two most significant bits**, the output of a CPython-style `getrandbits(2)`.

The ten outcomes are:

| Row (zero-based) | Original CLASS | Full reconstructed predecessor (tempered) | Top two bits |
|---:|---|---|---:|
| 3 | RECOVER | `5900364D` | 1 |
| 4 | LABEL | `1E5E734C` | 0 |
| 13 | STORES | `297A759F` | 0 |
| 14 | STORES | `3BE83DE0` | 0 |
| 28 | STORES | `31767148` | 0 |
| 30 | STORES | `27443315` | 0 |
| 34 | LABEL | `097AAF7C` | 0 |
| 38 | RECOVER | `47FB8240` | 1 |
| 44 | STORES | `22C652B8` | 0 |
| 45 | STORES | `2EE418F3` | 0 |

**Exact empirical match, 10 of 10:** `getrandbits(2)` on the *last unseen word immediately before the payload* yields `1` for `CLASS=RECOVER` and `0` for `CLASS=LABEL` or `CLASS=STORES`. The source-selected positions were fixed by the prior MT recurrence witnesses, independent of the original CLASS metadata. The value was then reconstructed exclusively from other observed generator words using inverse MT twist. Thus the 2-bit outputs are an additional correspondence not included as equations in the original 42-witness alignment.

The first five chronologically selected observations (rows 3,4,13,14,28) identify the binary mapping. Applied unchanged to the remaining five (rows 30,34,38,44,45), it predicts **all five**. This is a *retrospective split of a discovered sample*, not a prospective independent trial; the entire ten-row sample was selected by availability of inverse-reconstructible predecessor words.

If these ten 2-bit outputs were independent uniform values, the probability of the **particular specified mapping** holding at all ten is `4^-10 = 9.5367431640625e-7`. The naive iid null does not account for selection effects, common MT structure, the post hoc class mapping, or other hypotheses inspected; it must **not** be advertised as a calibrated statistical significance level.

## Stronger discriminator: rejection-run signatures immediately before the payload

In **five** of the ten records above, inverse MT equations also reconstruct the **second-last** word before the record's first payload word, giving these chronological last-two `getrandbits(2)` outputs:

| Row | Penultimate 2-bit output | Final 2-bit output | Original CLASS |
|---:|---:|---:|---|
| 4 | 2 | 0 | LABEL |
| 34 | 2 | 0 | LABEL |
| 38 | 2 | 1 | RECOVER |
| 44 | 3 | 0 | STORES |
| 45 | 3 | 0 | STORES |

**All five** penultimate results are **2 or 3**, the values rejected by CPython `_randbelow(2)`; all five terminal results are the class-correlated 0/1 accepted values. For row **4**, three consecutive source-restored predecessor words give exactly **`3, 2, 0`**: two rejected attempts, followed by an accepted zero. The reproducer now asserts these six rejection-run facts directly.

This substantially narrows the generator hypothesis: a **terminal two-way rejection sampler** (or a producer deliberately imitating precisely its accepted/rejected output rule) accounts for ten observed final values and six separately reconstructed preceding rejection values. It is more discriminating than merely observing that the last 2-bit output correlates with a metadata flag. The sample remains conditioned on reconstructed alignment groups, and the original producing software is unavailable; inferential provenance is still conditional.

A terminal rejection-sampled `randbelow(2)` call consumes at least one extra 32-bit draw per ordinary row, and a further independent per-row generator call would imply at least two. Under those **hypothetical** regular-interval floors, the expanded 42-witness stream constraints narrow the selected row129 relative start as follows (tail intervals remain unconstrained beyond four payload outputs):

| Minimum hidden draws per fully ordinary transition | Selected row129 first-output position relative row0 | Row43→44 total-output distance |
|---:|---|---|
| 0, source-only model | 917–971 | 11–65 |
| 1, terminal selector minimum | **931–963** | **11–43** |
| 2, terminal selector plus one preceding call | **945–955** | **11–21** |
| 3, universal floor | **infeasible** | infeasible |

These bounds are conditional on the stated consumption floors and are graph-distance extremal solutions, not estimates or recovered bytes. The *two-call* model's **eleven** selected-output start positions are a promising constrained cracking target. The three-call floor contradicts the 42 MT recurrence witnesses. Distinguish the observed terminal rejected sequences from the as-yet unsupported assumption that the printer made another generator call every ordinary transition.

## Practical consumption-rule hypothesis

For CPython `_randbelow(2)`, `getrandbits(2)` rejects values 2 or 3, accepting 0 or 1. The observed exact mapping is therefore consistent with the possibility that **the last source-generator call before emitting each ordinary payload consumed rejection-sampled 2-bit outputs until it returned a class-correlated binary indicator** (1 for RECOVER, 0 otherwise). This *would* explain both the absence of indices 2/3 among ten complete words and the existence of variable-length inter-record hidden-draw runs.

The method does not establish that the old printer used CPython `_randbelow(2)`, that the class flag was intentionally coded, or whether this putative terminal binary call was the only metadata-dependent generator call. The source-producer implementation is absent. Most critically, even a true terminal selector would not **by itself** recover earlier rejected draws or the four selected missing K04 words. The five RECOVER tail rows may have different output-consumption logic; do not generalize this empirical regular-cohort correspondence to them without testing intact tail data.

**Next falsifiable cracking experiment:** build a single chronological MT consumption model with a pre-payload binary terminal call satisfying `getrandbits(2) in {0,1}`, and seek a source-based rule for preceding draws. Use the exact existing 42 witnesses as a hard position gate, then predict intact RECOVER-tail words before any selected ACK word or K04 hash. In particular, recover how many hidden draws lie in row43→44 (at least seven) and allocate the linked row128→129→130 gaps via the established equation `g128+g129=(s44-s43)-11`.

No original K04/K08 PASS yet, and the original ZIP/commitments remain untouched.
