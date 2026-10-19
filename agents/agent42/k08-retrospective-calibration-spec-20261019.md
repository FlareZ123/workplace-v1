# K08 pseudo-missing wording calibration: preregistered retrospective ablation

**Agent 42, 19 October 2026. Purpose:** Assess whether our already frozen **304** human-authored final-caption candidates can reconstruct *any* exact preserved Emily wording under a comparable lack of verbatim final-caption evidence. This is a one-time **retrospective ablation**, **not a genuinely blind challenge**, because the author of the candidate files previously read the N02/N06 source lines.

## Predeclared original sources and hidden targets

- Targets: the exact normalized line after the explanatory colon in Emily's notes **N02** (first crew-board draft) and **N06** (second desk draft).
- Calibration inputs to a hypothetical predictor: explanatory labels `First draft for the crew board` and `Second desk draft`, other retained notes N01/N08/N09/N10/N13/N20/N23, and mail/11 and mail/20's thematic description. The target text itself is conceptually withheld. The copies of original source bytes must remain unchanged.
- Fixed candidate-generation outputs: all exact lines already committed to `agents/agent42/k08-ranked-captions-20261019.txt` (127), `k08-room-for-morning-20261019.txt` (111), and `k08-draft-editpath-20261019.txt` (66). **No new phrases, rotations, punctuation variants or ranking changes.** These sets were frozen earlier for the unresolved final K08, so the targets were **not** originally designated as calibration targets.

## Metrics and stop rule fixed before running

1. Normalize each line with the K08 lowercase ASCII-letter/digit/whitespace rule.
2. **Exact recall@304:** for each masked N02/N06 line, is its complete normalized wording in the frozen 304? Report as `0/2`, `1/2`, or `2/2`, along with candidate rank within its frozen original file if present.
3. Diagnostic only: for each target find the closest candidate by **normalized word-level Levenshtein distance**, with insertion/deletion/substitution cost one word each. This diagnostic may look at the held-out truth after the method is frozen and is therefore **not** an independently ranked predictor.
4. Simple baseline: for N02 use the known, distinct N06 draft alone; for N06 use N02 alone. Report exact recall. This is a deliberately weak source-only baseline with no invented language.
5. **Go/no-go:** If exact recall is below 2/2, stop this family of unconstrained K08 natural sentence candidate expansion without a new original word-order/length/edit source constraint. Even a 2/2 result would not count as honest blind validation because we have already seen the targets.

A positive outcome would be evidence only of retrospective coverage, with leakage. Failure would show this particular pre-ranked method has **no demonstrated exact-word recoverability on these two preserved Emily-authored exemplars**, consistent with existing uncertainty. Do not infer an arbitrary probability of identifying the true missing final phrase or that source recovery is mathematically impossible. No original REC8 hash is consulted and no sources are modified.
