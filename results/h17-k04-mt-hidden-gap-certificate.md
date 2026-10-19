# K04: ten seed-free, source-only hidden-draw lower bounds from inverse-restored words

Agent 23, 19 October 2026. Reproducer [`agents/agent23/k04_mt_preword_collision_cert.py`](../agents/agent23/k04_mt_preword_collision_cert.py), original ZIP and source SHA-256 as in [inverse-output report](h17-k04-mt-inverse-hidden-outputs.md). This certificate **does not assume the printer made any particular metadata RNG calls**. It assumes the existing 25+17 MT19937 recurrence witnesses represent one chronological stream of four-word payload blocks. It excludes selected K04 row129 completely and does not use an acceptance hash.

## Source-only new lower bounds

The inverse-twist recovery produces complete original-generator words immediately **before** ten ordinary payload blocks. For each row `r`, let `s[r]` denote its unknown output start. If the preceding source row `r-1` were adjacent, `s[r]-s[r-1]=4`, its **fourth recorded word** would occupy `s[r]-1`. For all ten identified rows, the fully reconstructed unobserved `X[s[r]-1]` differs from that specific preceding source payload word. Therefore an adjacent transition is impossible without knowing *why* the generator drew more words. Where two or three consecutive hidden words have been recovered, direct unequal-overlap comparisons similarly exclude distances five and six.

Exact certified minimum number of inter-row skipped 32-bit MT words `g[r]=s[r+1]-s[r]-4`:

| Regular transition | Certified `g[r]` minimum | Source-recovered suffix before next row |
|---|---:|---:|
| 2→3 | 1 | 1 word |
| 3→4 | **3** | **3 words** |
| 12→13 | 1 | 1 word |
| 13→14 | 1 | 1 word |
| 27→28 | 1 | 1 word |
| 29→30 | 1 | 1 word |
| 33→34 | **2** | **2 words** |
| 37→38 | **2** | **2 words** |
| 43→44 | **2** | **2 words** |
| 44→45 | **2** | **2 words** |

The program compares the literal original untempered words at every potential overlapping stream index, asserts that each hypothesized shorter gap produces a mismatch, and then adds the certified floor to the 42-witness integer difference graph. The reported source-only tight selected-row bounds improve from **917–971 to 919–971** inclusive, and the possible output distance `s44-s43` reduces from **11–65 to 11–63**. These are source-only conditional lower bounds; a binary rejection-sampling explanation is **not required** to establish them.

## Separate exploratory producer insight

The very same ten reconstructed immediate predecessors, after MT tempering, have upper two bits `1` exactly when the original record says `CLASS=RECOVER` and `0` for LABEL/STORES. Of the five predecessor pairs reconstructible from distant source anchors, the preceding two-bit output is `2` or `3`, the exact reject set for a CPython `randbelow(2)` call; row4 supplies **`3→2→0`**. The independent analysis is [the predecessor class gate](h17-k04-mt-predecessor-class-gate.md). It is a promising conditional generator-consumption hypothesis; the spacing exclusions above stand separately on byte inequality and fixed relative source positions.

A universal terminal binary call would imply at least one hidden draw per ordinary row, reducing the selected stream-start interval to **931–963**. One additional generator call per ordinary transition would imply at least two, further reducing it to **945–955** (eleven values). These stronger numbers explicitly depend on output-consumption assumptions. The original 42 witnesses plus ten directly unequal overlaps are the current model-conditional source evidence.

No K04 or K08 accepted bytes recovered, no unchanged original acceptance PASS. Original spool, mask, nonce and verifier remain untouched.
