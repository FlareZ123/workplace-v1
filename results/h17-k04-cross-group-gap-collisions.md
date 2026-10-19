# K04: 46 source-derived cross-group MT gap-floor constraints

Agent 1, 19 October 2026. Reproducer: [agents/agent1/k04_cross_group_gap_bounds.py](../agents/agent1/k04_cross_group_gap_bounds.py). SHA-pinned source: \`evidence/print/spool-reconstruction.log\`, \`7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083\`. All observations from the unmodified original 133-line spool; selected row129 omitted and original K04 commitment not consulted.

## New source-index intersection technique

Agent 23 and Agent 31's already-established **42 unwithheld MT19937 recurrences** partition printer record start indices into separately anchored but internally fixed groups. Their recursive MT inverse/forward solver reconstructs additional **full and partly known hidden generator words** within each group.

Let row \`r\` begin at global unknown stream position \`s[r]\`, let \`g[r]=s[r+1]-s[r]-4\` count unobserved full 32-bit outputs, and let each connected group's recovered stream positions use its existing local coordinate system. Every proposed integer \`g[r]\` aligns the local output maps on opposite sides of a record boundary. If those maps disagree in any bit known on **both** sides of an overlapping position, that proposed gap is impossible under the common-stream MT model. Scan \`g[r]=0,1,...\` in order; the first conflict-free value supplies a rigorously justified **lower bound** for that particular boundary, without knowing the seed, output-consumption code, or historical K04 bytes.

This is additional information from **cross-group bit consistency** beyond Agent 23's source-only ten-inverse-word collision floors, which compared a more limited set of immediate ancestors. The source-selected target row129 and its two adjacent boundaries are excluded from the scanning phase.

## Output

Of the 132 adjacent source-record boundaries, 46 have a provably positive gap floor in the scanned range 0..64. Example: for row92→93, proposed gaps \`g92=0,1,2\` all assign conflicting fully reconstructed MT words to the same global stream position; therefore **\`g92>=3\`**. Other individually informative floors include \`g12>=5\` and \`g42>=4\`. For boundaries with no conflict-free position among the first 65 possibilities, this reproducer retains the conservative zero floor rather than claiming impossibility.

Feeding the new 46 floors into the original 42 recurrence equality/difference graph produces:

| Conditions | Selected row129 stream start \`s129-s0\` |
|---|---|
| Original 42 recurrences, chronological four-word payloads | 917..971 |
| Same recurrences, plus 46 inter-group conflict floors | **922..971** |

This is a five-index improvement in the unconditional-within-the-common-MT-model K04 **position bound**, independent of assuming any particular CLASS/DEST sampler mechanism. It does not infer target row129's four payload words or yield a recovered K04 key.

## Validity limits and next use

The contradiction is exact *conditional on* each original 42 triple being a genuine single-stream MT recurrence and the four visible words of each retained record being sequential outputs. The historical common-stream interpretation itself is not yet independently authenticated. The added comparisons do not provide source evidence about an original printer program, so the reported lower bounds should remain separate from causal interpretation.

The strong new Agent 2 DEST post-payload sampler and Agent 31 CLASS pre-payload selector suggest exploiting these collision constraints with a **single coherent variable-draw producer rule**. Such a rule must reproduce known intact tail words before predicting K04 row129. No accepted K04/K08 component has been recovered.
