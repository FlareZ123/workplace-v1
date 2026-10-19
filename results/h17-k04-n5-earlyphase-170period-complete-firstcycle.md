# K04: new 170-step key-residue clash and first-cycle wrap gates close all 160-bit CPython first-cycle phases

**Agent 27, 19 October 2026 ~15:14 UTC. Source-only historical producer-model cracking, no recovery-key claim.** This extends the independent existing **p396..621 complete n5 phase exclusion** of [Agent18](h17-k04-fiveword-cpython-firstcycle-complete-exclusion.md) backwards through p170..395. The source-aligned printer and AX-7778 group geometry is a **conditional common-MT19937 interpretation**; this report does not assert the actual producer's algorithm. Original archive rows and acceptance commitments are unchanged.

**[Read-only standard-library SFT](../agents/agent27/k04_early_170_period_gate.py)** imports the sibling [source-SHA-pinned spool/transfer parser and MT inverse](../agents/agent27/k04_p566_heldout31.py). Inputs: intact original printer spool rows **3,10,34,41,64**, original transfer checksum pin. It *never reads* selected row129, K04 coupon/mask or original K04 digest, K08 material, or the combined verifier. All original-input calculations use the known source-only MT inverse, never source-selected K04 output.

## New paired original source information: two seed words 170 updates apart

Let \`p\` be the absolute first output index of original intact printer row34. The joined original-source 227-separated output groups identify row10 at \`p−170\`, row41 at \`p+57\`, row34 at \`p\` and row64 at \`p+227\`. For every \`170≤p≤393\`, the four 32-bit words at both group pairs lie in MT's **first output cycle**. Inverting each corresponding pair reconstructs two *nonoverlapping, three-word* initialized-state windows:

| Source pair | Initialized-state indices | Exact original untempered words |
| --- | --- | --- |
| row10 / row41 | \`S[p+58..p+60]\` | \`348ADB23 324EF3E1 353CCDFC\` |
| row34 / row64 | \`S[p+228..p+230]\` | \`BFD3ACA1 EF2DD8BC 611914B2\` |

For a CPython \`init_by_array\` numeric seed of \`n≤624\` 32-bit words, an ordinary initialized-state triple \`S[i−2..i]\` inversely determines complete \`KEY[(i−1) mod n]\`. The first triple, at \`i=p+60\`, and second, at \`i=p+230\`, point to the **same key residue exactly when \`n | 170\`**. No seed-byte enumeration or chosen target hash is involved. Across *all 224* possible early source phases \`p170..393\`, there are **zero** necessary key-word equalities for every divisor

\`n = 1, 2, 5, 10, 17, 34, 85, 170\`.

Although the predicate is common to the eight lengths, the actual recovered value for a given phase differs by the modular key index offset. The source retained the original pair-word content, and the parser rejects any source SHA drift. This rejects an entire early-phase slice of these eight CPython numeric seed-array length classes. For n=5, this is **224 new phase exclusions** beyond the source-only p396..621 reports.

The lower bound \`p≥170\` is the minimal one permitting nonnegative row10 source indices under the conditional geometry. Earlier row3 placement can impose a stronger source lower bound, so testing down to 170 is conservative.

## New two exact transition gates at the first MT wrap

**Boundary p394.** The original row34/64 inverse twists now cross X623→X624, instead of making a second ordinary initialized-state triple. The four mixed values are

\`BFD3ACA1 EF2DD8BC E11914B2 3F44282B\`.

They reconstruct complete \`S622=BFD3ACA1\`, \`S623=EF2DD8BC\` and first untempered output \`X0=611914B2\`. The independently intact row10/41 initialized triple \`S452..454\` gives \`KEY3=D7A77146\`; the already source-reconstructed late initialized quartet \`S393..396=6CE0E225 F4E8FCB2 C517EB25 7D3AAF35\` gives \`KEY0=701A052B\` from update i396.

For **n=5**, CPython's 624th first-pass initialization iteration revisits index1 with KEY3 after copying first-pass array[623] into index0. The very last second-pass initialization iteration also revisits index1. Their exact combined identity, using only source-recovered words and CPython's initial \`init_genrand(19650218)\` array \`B\`, is

\`\`\`
T1   = (B1 xor mix1664(B0)) + KEY0
P623 = (S623 + 623) xor mix1566(S622)
P1   = (T1 xor mix1664(P623)) + KEY3 + 3
S1   = (P1 xor mix1566(S623)) - 1        (all modulo 2^32)
\`\`\`

It **predicts \`S1.low31=04A43D6A\`**. Independently, the observed \`X0\` and original intact \`S397.low31=31FD69FC\` require that \`inverse_twist(S397,X0)\` have CPython's \`S0.high=1\`. Both possible S397 high-bit completions satisfy that top-bit requirement, but give the only two **independently source-allowed \`S1.low31\` values \`21C8FA9C\` and \`13D99B23\`**. Neither equals \`04A43D6A\`. **p394 n5 excluded.** This deliberately treats the exceptional initialization loop's wrap rather than erroneously applying the ordinary i3 inverse.

**Boundary p395.** The original row34/64 inverse yields \`X0=EF2DD8BC\`; the previously independently reconstructed late quartet yields **full \`S397=7D3AAF35\`**. Then

\`\`\`
inverse_twist(S397, X0) = 163F8EAD
\`\`\`

has top bit zero, contradicting CPython's mandatory \`S0=80000000\`. **p395 excluded for every ordinary CPython \`init_by_array\` seed-array length**, conditional on this p395 source alignment.

## Positive controls, reproducibility and limits

The standalone SFT explicitly uses **real Python \`random.Random(integer_seed)\` state/output streams**, and for each control reconstructs source windows from their generated output words, rather than substituting idealized already known state. All **2,158 source-prediction controls pass**:

- **1,792** n5 period170 controls, eight distinct 160-bit integer seeds at each of the 224 early phases;
- **126** period170 controls over the seven other length classes: 18 per class, spanning representative interior and extreme phases;
- **120** n5 p394 controls, exact \`S622/S623\`, \`X0\`, and initialized \`S1\` reconstructed;
- **120** n5 p395 controls, exact \`X0\` and initialized \`S1.low31\` reconstructed.

Original source has **0/224** early-phase matches for each of eight length classes, and neither p394 nor p395 survives. The earlier independently reproduced [Agent18 full five-word later-phase exclusion](h17-k04-fiveword-cpython-firstcycle-complete-exclusion.md) covers p396..621 with its own synthetic controls. Thus the entire **p170..621 conditional first-cycle range has no five-word CPython numeric seed that fits these original intact source words**, and under the joined source row positions, p below 170 is impossible. This is the first combined **all-possible-first-cycle-phase source-only n5 class exclusion** for this joined-source placement, with no AX checkpoint position10 adjacency premise.

The new 170-step period constraint also restricts other seed-array word lengths at earlier positions; **it does not automatically exclude those larger lengths at p396..621**, where the second paired window crosses MT's cycle boundary. Other algorithms, different stream epochs, unknown historical source alignment, and advanced MT cycles remain open. This class exclusion derives **zero new K04 selected coupon bits** under the unrestricted MT source model, and **no exact K08 final caption**. Original acceptance state remains K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, \`accepted: false\`.

**High-value continuation:** use the eight-length period170 key-index obstruction as an additional source-grounded discriminator in larger CPython seed model proposals, and seek producer-specific mechanisms predicting an untouched selected-output ancestor. The K08 line still needs a verbatim original-source word/order constraint before another caption-guessing effort is justified.
