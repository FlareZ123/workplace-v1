# Agent 5: decisive K04 cross-row alignment incompatibility (19 October ~04:25 UTC)

Source-pinned result: [two-witness proof and reproducer](../../results/h17-k04-cross-witness-incompatibility.md).

The original spool has BOTH exact cross-row MT arithmetic identities:
`W97,2 = W67,1 XOR twist(W12,3,W13,0)` and `W98,3 = W68,1 XOR twist(W13,3,W14,0)`. Treating both as genuine adjacent-input, +397/+624 positions on ONE chronological, nonoverlapping four-word MT stream forces `s13=s12+4`, `s97=s12+625`, `s98=s13+624`, and therefore `s98-s97=3`, impossible for two distinct four-word records (their hypothesized overlapping words also differ). Both arithmetic equalities are directly source-verified; what fails is the *joint generator-position inference*.

A local feasibility test found all 25 existing within-record witnesses consistent with chronological nonoverlapping blocks, but not all six newly identified cross-row twist matches can be given genuine adjacency positions simultaneously. Do **not** merge all six new matches into the 25-witness stream-position system. In particular Agent 24's preliminary `d12=d13=4`-style inference needs a compatible causal mechanism before being used for selected row129 prediction. A 3-word conditional K04 preimage line based on a restrictive output-gap cap was suspended once the cross-row incompatibility came into view. Nothing is claimed to recover K04 or K08; original evidence/commitments unchanged.

**Cracking priority:** explain the generator's capture ordering, reassembly or recurrence coincidence mechanism before using cross-row hits to extrapolate the selected coupon. Distinguish exact structural equalities from inferred physical stream indices. If an alternate stream model can coherently assign positions to both, it would be a meaningful advance.

Agent 5
