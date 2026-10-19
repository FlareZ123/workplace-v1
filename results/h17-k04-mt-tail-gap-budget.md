# K04: source-fixed MT tail witnesses constrain hidden output consumption (19 October 2026)

**Agent 37; new conditional derivation, not a recovered component.** Source: original 43-member export, `evidence/print/spool-reconstruction.log` SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Does not consult any acceptance commitment. The [standalone reproducer](../agents/agent37/k04_tail_gap_discriminator.py) checks the two already observed Agent 8 MT19937 twist triples directly against source bytes.

## Exact row-gap result

Let `s[r]` be the unknown position of the first of the four contiguous **little-endian, untempered** 32-bit MT outputs stored in spool row `r` (zero-based), and `g[r]=s[r+1]-s[r]-4 >= 0` the number of RNG draws skipped between payloads.

The original two tail witnesses are `((44,0),(97,3),(131,0))` and `((45,0),(98,3),(132,3))`. Each satisfies the seed-independent MT recurrence `x[k+624] = x[k+397] XOR twist(x[k],x[k+1])`. Their index equations, conditional on each match really representing that recurrence in a shared stream, are:

- `s[97]-s[44]=394`, `s[131]-s[44]=624`.
- `s[98]-s[45]=394`, `s[132]-s[45]=621`.

**New exact discriminants:** `g[44]=g[97]` and `g[131]=g[97]-3`. Summing the witnessed spans gives `sum(g[97:131])=94` for rows 97→131, and `sum(g[98:132])=91` for rows 98→132. The selected target is row 129, and **neither witness predicts its four words**.

## Generator-model cracking implications

- The first span has **30 wholly regular adjacent intervals** (97→98, …, 126→127) plus four boundary/tail intervals. Every draw count is nonnegative. A model that consumes **at least four skipped outputs in every regular-to-regular interval** is **mathematically incompatible**: those 30 alone would use at least 120, exceeding the source-forced total 94. This rules out that precise uniform-overhead class, not MT19937 itself.
- Under the proposed alternative of **one fixed extra 32-bit draw plus exactly two Python-style `randbelow(3)` choices per wholly regular interval**, the 30 interior intervals have at least 90 skipped draws, leaving **at most four rejection draws among the 60 `randbelow(3)` calls**, even if the boundary/tail consume nothing. Conditional on independent uniform 2-bit candidate draws, the exact negative-binomial probability of at most four rejections is `9.720959483087328e-5`. This strongly challenges the proposed uniform fixed-extra-draw model, even though its *global mean* resembles earlier observed spans. The conditional probability is a model likelihood calculation, not a p-value for a pre-registered physical printer mechanism.
- The 31st regular→tail boundary interval (127→128) is **not** assumed to have regular metadata overhead. Hence the 30-interval lower bound is robust to a producer switching logic for the tail. If that boundary also consumed the same three minimum skips, a sharper bound follows, but that stronger assumption is not needed.

## Limits and action

All conclusions about `s` and `g` depend on two MT recurrence hits being correctly placed in one continuous stream; the recurrence matches are observed, but historical output consumption remains inferred. No original seed, original coupon or exact K04 masked component is obtained. In particular, a class/destination-dependent draw model with some zero-cost calls remains viable. For further cracking, use this **late-window draw budget** when designing any consumption rules; reject rules that consume more than 94 extras over the 97→131 interval *before* K04 hash testing. Derive a complete model that predicts intact held-out tail words, ideally with row129 withheld. Source evidence and original acceptance files were not modified.

## Second exact constraint: a minimum of five skips locally

The regular MT witness ((42,0),(95,1),(126,2)) forces s126-s42=622, hence sum g42..125=286. The tail witness ((45,0),(98,3),(132,3)) forces s132-s45=621, hence sum g45..131=273. Subtract the overlap: g42+g43+g44=13+g126+g127+g128+g129+g130+g131. Every g is nonnegative, so **at least one of intervals 42 to 43, 43 to 44, 44 to 45 must skip at least five MT outputs**. This uses two witnessed source relationships and no seed, slot hash, or generator-overhead assumption. In conjunction with the separate 94-draw tail budget, the data contradict both a universal maximum of four skipped outputs and a universal minimum of four over every fully regular interval. It identifies a necessary variation in gaps, without predicting K04 row129.
