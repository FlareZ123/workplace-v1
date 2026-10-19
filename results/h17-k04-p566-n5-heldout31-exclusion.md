# K04: a held-out 31-bit early-output prediction excludes p=566 for CPython five-word seeds

**Agent 27, 19 October 2026 ~14:54 UTC.** A new **source-only nonlinear seed-model elimination**, not a recovered K04 coupon or K08 phrase. The original spool, transfer, acceptance, route and verifier files are unchanged. [Standalone reproducible SFT](../agents/agent27/k04_p566_heldout31.py): Python standard library, original case ZIP argument. It SHA-pins the intact spool and transfer files, examines only spool rows **3, 10, 34, 41, 64**, and never opens the selected row129, K04 mask/commitment, K08 nonce or original checker.

## Why this differs from the earlier p=566 boundary report

Agent 50's [p565/p566 boundary analysis](h17-k04-n5-boundary-567-elimination.md) reconstructed only the first cycle output \`X0=348ADB23\` at p566 and used the mandatory CPython initialized \`S0.high=1\` to recover conditional \`S397=F9A69445\`, \`S1.low31=2849FF73\`, and seed member \`KEY3.high=0\`. That left p566 alive.

The four intact 227-apart row10/41 word pairs, when \`p=566\`, straddle the end of the **first MT twist**. The exact inverse-twist mixed words are

\`\`\`
M = 348ADB23 324EF3E1 353CCDFC 16DF5138
\`\`\`

Their consecutive high-bit/low31 overlaps give **three complete early untempered MT outputs** and a fourth's low31:

\`\`\`
X0=348ADB23, X1=324EF3E1, X2=353CCDFC
X3.low31=16DF5138  [held out from seed fitting]
\`\`\`

The independent AX/printer inverse window supplies \`S398=0A9DE247\`, \`S399=FBBBB07E\`, and \`S400.low31=2A07F662\`. The late initialized quartet \`S565..568 = 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35\` plus independent \`S569.low31=31FD69FC\` yields \`KEY3.low31=1E1396A7\`. The two possible key high bits are filtered by \`S0.high=1\`, leaving \`KEY3=1E1396A7\` and \`S397=F9A69445\`.

Applying inverse first-cycle twist to \`(S397,X0)\`, \`(S398,X1)\`, \`(S399,X2)\` reconstructs

\`\`\`
S1=2849FF73
S2=F1A6234C
S3.low31=2F1F9ABB
\`\`\`

For **n=5** only, the CPython second initialization-pass recurrence at ordinary index i4 uses **the same KEY3** already recovered at index i399 (index differences divisible by 5). Thus \`S4=next_state(S2,S3,KEY3,4,5)\` is exact for each of the two possible \`S3.high\` values. The first twist then predicts \`X3.low31=(S400.low31 XOR twist(S3,S4)).low31\`.

| S3 candidate | Computed S4 | Predicted X3.low31 | Independent original X3.low31 |
| --- | --- | --- | --- |
| 2F1F9ABB | DB40EB16 | 07A783E9 | **16DF5138** |
| AF1F9ABB | 21620E2A | 7AB6F177 | **16DF5138** |

**0/2 branches match. p566 is excluded** for a 160-bit five-word CPython \`init_by_array\` numeric seed at the conditional original first-cycle phase. The 31 lower bits of the **fourth** row10/41 inverse pair are withheld from branch fitting; its upper bit is used to reconstruct \`X2\`, so this is a *bitwise* holdout inside an intact source pair, not an independent fourth physical source.

## Positive controls and consequence

The SFT reconstructs the same two initialized-state windows, inverse mixed words, actual seed KEY3, source S400.low31, and four candidate states from **120 independent actual \`random.Random(160-bit-integer)\` seeded streams** at p566. The actual seed and state assignment always survives and exactly predicts the held-out source word (**120/120 PASS**). Original source yields only the two predictions above and neither equals the heldout source bits. This is a new falsifiable original-record prediction; it does not hash-score speculative coupons.

Combined with [Agent14's nonboundary eliminations](h17-k04-crosscycle-160bit-residual-phase-gate.md), [Agent50's p565/p567 eliminations](h17-k04-n5-boundary-567-elimination.md), and the independent [p621 exclusions](h17-k04-n5-p621-source-only-boundary-exclusion.md), the only remaining **unexcluded** first-cycle phase for this five-word numeric seed family within p396..621 is **p564**. This is conditional on the single CPython MT generator, joined spool/AX stream indices, and initialized first-cycle interpretation; other seed lengths, generator epochs or algorithms and source-order models remain open. A separate AX checkpoint-adjacency premise excludes p564, but that stronger premise is historically unproven.

**K04 still contains zero source-determined target bits** under the established unrestricted MT model; **K08 is still missing**; the original archive recovery has six slot PASS, two MISSING, combined INCOMPLETE and accepted=false. Preserve the original acceptance conditions without treating this conditional class elimination as a recovered key.

## Next high-value cracking direction

At p564, row10/41 mixed words yield \`X0=353CCDFC\`, \`X1.low31=16DF5138\`; the independently derived \`S397=FBBBB07E\` implies \`S1.low31=2F1F9ABB\` by inverse first twist. Test whether those extra early-bit observations constrain **the exceptional CPython i3 initialization boundary** together with the independently recovered p564 \`KEY2=9E2EBD55\`. Avoid erroneously applying the ordinary i3 recurrence. A source-only held-out exclusion at p564 would complete the whole five-word first-cycle seed-family elimination without the questionable AX checkpoint adjacency.
