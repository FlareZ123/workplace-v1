# K04: a seven-bit complete coupon solver from two low31 MT ancestor runs

**Agent 41, 19 October 2026 ~11:16 UTC. Constructive K04 algorithm with an exact synthetic PASS, conditional on recovering two new original-source word runs. This is not an accepted original K04 value.**

## The new cracking simplification

The [source-only target-leverage atlas](h17-k04-target-leverage-paired-hidden-windows.md) proved that eight full untempered MT19937 ancestor words in **two gap-separated four-word runs** recover the 128 K04 payload bits under the source-compatible minimum-gap index placement `d=11,p=627`. Its less-obvious result: retaining only the **lowest 31 bits of each of those eight words** already fixes **121 of 128** target bits. The remaining **seven bits** are precisely identifiable and can be enumerated in **128 candidates**, with one original SHA256 acceptance comparison per candidate.

Let `U[j]=X[4+j]&0x7fffffff` and `V[j]=X[400+j]&0x7fffffff`, for `j=0..3`. Let `X[3]` be the already intact printer row43 final word. The MT19937 generator recurrence is

`X[627+j] = X[400+j] XOR twist(X[3+j],X[4+j])`.

`twist(a,b)` depends on **a's highest bit**, **b's low 31 bits**, and **b's lowest bit**. Therefore reconstructing four target words from the two low31 runs requires exactly:
- The upper bits of early `X[4]`, `X[5]`, `X[6]`: **three bits**; early `X[7]` upper bit does not enter any of the four target outputs.
- The upper bits of late `X[400]` through `X[403]`: **four bits**.

All eight source low31 values are treated as *independently recovered candidate observations* with justified stream placement, never inferred from the disputed original row129 bytes. For each of the 128 seven-bit assignments, reconstruct `X[627..630]`, apply MT tempering and little-endian serialization to obtain the sixteen printer payload bytes, XOR the original route-sheet K04 mask, and compare the 16-byte component with the **unchanged original K04 SHA256**. No 128-bit hash preimage brute force remains once the eight correct low31 observations are available. Even if the historical printer ACK bytes were corrupted, the reduction could recover a computationally accepted coupon from authentic ancestor witnesses.

## Executable demonstration

[Self-contained Python stdlib SFT](../agents/agent41/k04_low31_seven_bit_completion.py) implements `recover(x3, early_low31, late_low31, mask, expected_sha256)`, returning the exact 16-byte coupon candidate and the seven recovered high bits for matching assignments. It generates a real CPython MT19937 stream from integer seed 20261019, retains only the true low31 bits at the eight ancestral indices, computes an independent ground-truth coupon at indices 627..630, and recovers that complete coupon with **exactly one SHA256 hit among 128 hypotheses**. The recovered seven-bit assignment matches the true seed's MT output highs. A false SHA256 target produces zero matches. This is a rigorous constructive positive control; it does **not** claim the synthetic seed is historically relevant.

The earlier [source-run candidate experiment](h17-k04-paired-window-source-run-attack.md) exhausted **88,804** ordered full-word pairings from original TRP2/RC-17 sources and found zero original K04 hits. Each previous full-word pairing tested only its four literal source upper bits. A **128-branch low31 closure can succeed with different upper bits** even when the literal complete-word pairing failed. Thus the new method defines a distinct finite original-source candidate class, with **88,804 low31 pairings × 128 high-bit assignments = 11,366,912** SHA checks. Those branches were **not** tested in the previous literal full-word run; the independently completed source-derived seven-bit exhaustive run is now documented below. This targeted alternative is motivated by the documented cross-source low31 inverse-twist witnesses, whose high bits were not always independently determined.

## Research value, limits and next action

This is a direct completion engine for any future matched **eight** low31 ancestral observations, including ones algebraically inferred by inverse-twist of intact printer words or from independent recorder controls whose highest bit is unreliable. It is sensitive to exact stream placement. The original historical printer producer, its absolute phase and common-stream chronology are not authenticated; all 128 original K04 bits remain unrecovered under the currently retained observations. The candidate K04 bytes and acceptance hash are only used after new source observations are supplied.

The shortest supported next step is to identify source-grounded low31 word runs with positive held-out index predictions at both `X[4..7]` and `X[400..403]`. If either run genuinely appears, the other gap becomes the precise remaining investigative target. K08's original signed final caption remains unquoted in the supplied export, and no new K08 word information has been recovered.

**Original REC8 state remains six PASS, K04/K08 MISSING, combined INCOMPLETE, `accepted: false`.** Original evidence, routing, verifier and commitments remain untouched.


## Original-source seven-bit closure completed at 11:18 UTC

Executed [the new original-source driver](../agents/agent41/k04_low31_crossrun.py) and [optimized OpenSSL C inner scanner](../agents/agent41/k04_low31_crossrun.c) against SHA256-pinned unchanged spool, TRP2 and RC-17 records. The 298 run **assignments** comprise 291 unique natural recorder sequences, the explicitly repeated K05 latest-latch sequence (already among those 291), and six RC-17 page sequences. There are therefore **297 distinct ordered source runs**, but 298 enumerated entries including the named K05 duplicate. The exhaustive algorithm checks every ordered source pair and each of the 128 missing high-bit assignments:

`298 × 298 × 128 = 11,366,912` complete 16-byte K04 components.

Actual finished original-slot-SHA result: **`TESTED=11366912 HITS=0`**; exit zero; unchanged original source members SHA pinned; selected row129 never accessed. The mathematical seven-bit completion SFT independently recovers its exact synthetic target. This excludes all source-defined paired low31-run assignments at the specific `d=11,p=627` phase, including any alternative high-state bits invisible in the earlier literal full-word source scan. Other original source windows, phases, noncontiguous witnesses, producer models and alternate historical mask hypotheses remain open. No further arbitrary permutation/hash-volume expansion is justified without a different source relation.

This completed experiment preserves the **constructive discovery**: authentic low31 ancestor observations at both required historical stream windows, should they be found through a new independent index witness, would make the K04 coupon derivable with at most 128 unchanged-original-commitment tests.
