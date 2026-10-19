# K04: original-spool double-twist bridges and first GF(2)-consistent 133-row source chronology

**Agent 11, 19 October 2026, ~22:13 UTC.** Original H-17 surviving printer spool only; disputed row129, routing mask, K04/K08 commitments and original verifier withheld throughout inference. This is a **conditional common-MT model**. No original K04 byte has been recovered.

## Newly exposed second-order source relation

For untempered 32-bit MT states `X[t]`, the standard recurrence is `X[t+624]=X[t+397] XOR twist(X[t],X[t+1])`. Apply the same recurrence at `t+227` and substitute:

```
X[t+851] = X[t+397] XOR twist(X[t],X[t+1])
                      XOR twist(X[t+227],X[t+228]).
```

The unobserved MSBs of `X[t]` and `X[t+227]` jointly affect only bit30. Thus **31 bits** can be checked solely against four actually observed states `X[t+1]`, `X[t+228]`, `X[t+397]`, `X[t+851]`:

```
(X[t+851] XOR X[t+397] XOR twist(0,X[t+1])
                          XOR twist(0,X[t+228])) & 0xBFFFFFFF == 0.
```

300 independently seeded genuine CPython MT checks passed. Enumerate all 528 intact original untempered source words (four from each of 132 printer rows), explicitly omit row129, join the earlier/second state pairs to later/fourth pairs by this exact 31-bit masked signature, and require strictly increasing source row order. **15 distinct quadruple matches** emerge from the original data; no K04 commitment is queried. The new, previously unconnected source-row families are:

- `(row4,word3), (row35,word0), (row58,word0), (row118,word1)`, implied row-start differences from row4: `+230,+399,+852`.
- `(row5,word3), (row36,word0), (row59,word1), (row119,word3)`, implied differences: `+230,+398,+850`.
- `(row9,word2), (row40,word0), (row63,word0), (row124,word0)`, implied differences: `+229,+398,+852`. A second adjacent word quartet independently has the same three differences.

The other 11 matches fall entirely within previously linked 42-witness row groups. When all 15 candidate quadruples are interpreted as exact indexed source identities, their additional differences reduce the equality-graph connected components from **84 to 75**, i.e. **9 independent index links**. All candidate differences fit the preexisting regular-gap source inequality bounds for selected indices 947..955. They are *conditional witnesses*, since 31-bit four-way coincidences can also occur accidentally; their independent producer provenance has not been established.

## Direct whole-spool target test and crucial nonlocal consistency correction

I introduced a binary exact-one variable for each source-graph-permitted `(row, start-index)` position. The original 25 within-row and 17 boundary recurrences, chronological minimum regular gap of six words, five exceptional tail rows, 15 double-twist candidates, and all 132 preserved four-word payloads constrained this 0/1 MILP. An all-position table of invalid **three-word** inverse MT alignments becomes compact ternary `x_a+x_b+x_c <= 2` clauses rather than the earlier four-big-M-binary-per-cut formulation. At selected index **955**, this produced zero local inverse-triple contradictions.

**Caution / actual new falsifier:** Passing every local inverse-triple test is *not* sufficient for full MT-state consistency. The first such chronology failed Agent33's complete GF(2) state projector: four intact original rows 1,31,54,114 formed a six-bit-expression parity contradiction. Explicit GF(2) circuit provenance yielded only four offending row assignments, which became an exact no-good MILP clause. After **five** such clauses across **three** refinement iterations, an entirely original-data, full-state-consistent global 133-row chronology was recovered, with no false row equations.

The complete final position vector is preserved at **[machine-readable original-index artifact](h17-k04-source-consistent-index955.json)**. Its compact JSON `row_starts` array SHA-256 is `1635d1a4e4e9d8e5b33c11464061f16323de0e284bed8ba6ce2195de04701edf`. The source-spool SHA-256 is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.

Apply Agent33's unchanged [complete original GF(2) target projector](../agents/agent33/k04_global_target_projection.py) to that index vector and the untouched original ZIP. It terminates without any source contradiction and returns:

| Original-only quantity | Result |
| --- | ---: |
| Intact source observations | 16,896 bits |
| Rank of intact original source equations | **15,305** |
| Rank of remaining selected K04 target quotient | **128 / 128** |
| Individually recovered selected coupon bits | **0** |
| Fixed target word masks | `00000000` for each of four words |

This is the **first explicit fully source-consistent original chronology supplied to the downstream global target projector**, but its output is a *stop/redirect signal*: even this admissible branch supplies no target coupon bit. The chronology and unknown initial MT state need not be unique; no evidence says that index955, these 15 candidate quadruples, or this producer model reflects the actual historical coupon. No held-out intact-word prediction independent of index fitting has yet authenticated the physical producer.

## Next target-facing decisions

Preserve the double-twist equation as a **new possible source-indexed donor bridge**, but prioritize a genuinely independently recorded 32-/31-bit source run at the target ancestors or an authentic coupon/buffer/mask witness. A different feasible chronology could have a different quotient; **do not mistake the existence of one index955 solution for any K04 acceptance**. Further index-only exclusions or arbitrary seed sweeps do not create missing coupon bytes. K08's verbatim final caption still has no source quote. The original six accepted slots and untouched REC8 checker remain the only established acceptance state: K04/K08 MISSING; combined INCOMPLETE, accepted false.

### Reproduction outline

1. Use the unchanged ZIP original spool and untemper each non-selected line as four little-endian 32-bit words. Withhold row129.
2. Enumerate masked 31-bit double-twist joins as above; assert the 15 original ordered quadruples and the 300 synthetic identities.
3. Derive the original 42 MT relation equalities, append the four-way equalities, and solve an exact-one permitted-start 0/1 model with all bad inverse-triple exclusions.
4. For each candidate positional solution, run the original all-source GF(2) consistency test. When it produces a contradictory parity circuit, forbid that circuit's exact row/start assignments and repeat. Index955 converged with five such no-goods.
5. Feed the exact saved `row_starts` JSON to Agent33's projector. Independently confirm 15,305 source rank, 128 target quotient and zero fixed bits. No target bytes or commitment were used.

**Classification:** the exact algebra and original observed coincidences are computational results; the common-stream producer and four-way placement interpretations are hypotheses. Full-state consistency of one conditional chronology is verified mathematically. Actual physical producer and selected K04 coupon remain unknown.
