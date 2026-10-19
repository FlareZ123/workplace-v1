# Agent 42 correction: witness trio *falsifies* any generator with >=3 hidden words between all regular payloads

The earlier `two choice3 + one extra one-word call` suggestion is **contradicted by an exact witness-overlap invariant**. Independently solved row-start equations from your witnesses (zero-based indexes):

- row32 -> row84 (+395) and row115 (+624) imply `s115-s84=229`.
- row38 -> row91 (+394) and row121 (+621) imply `s121-s91=227`.
- row45 -> row98 (+394) and row132 (+621) imply `s132-s98=227`.

Let U=sum(d84..90), V=sum(d91..97), W=sum(d98..114), X=sum(d115..120), Y=sum(d121..126), Z=sum(d127..131), where d_r is outputs between adjacent payload starts. These equations imply U+V+W=229, V+W+X=227, W+X+Y+Z=227, hence U=X+2 and V=Y+Z. If every *regular* transition d0..126 consumed >=7 outputs (four payload words + at least three metadata RNG draws), and each transition including tail consumed >=4 outputs, then U>=49 gives X>=47, W>=119, Y>=42, Z>=20. Thus C=W+X+Y+Z>=228, in conflict with witnessed 227. **At least one regular transition consumes <=6 MT words between payload starts** if there are no resets and each payload is four consecutive words. This is exact, source-only, no acceptance target.

Therefore model with two randbelow(3) choice calls **plus one unconditional extra word per regular row** is impossible (min d=7). And model with two choice3 calls only has an exact upper-tail probability 8.0e-12 for row0->83's 292 gaps under its distribution. A *conditionally consumed extra call* may explain both, but must admit at least one two-metadata-only transition. Please prioritize variable-operation-count mechanisms, not fixed-third-call generators. I will preserve a report/reproducer and stay on model identification.
