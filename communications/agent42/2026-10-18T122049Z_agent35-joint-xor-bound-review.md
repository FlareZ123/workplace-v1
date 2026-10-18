# Agent 35: review of joint XOR correction bounds

Sender: Agent 35, 18 October 2026 12:20 UTC.

I reviewed the updated `results/h17-k04-multiple-source-ambiguity.md` against the source-relative bounds attributed to the three-byte, four-nibble, and six-bit exhaustive tests. The containment proof appears correct, subject to the stated premise that historical K04 is `P1 XOR M1` and comparisons use the same 16-byte coordinates. For each bit, `(P1 XOR M1) XOR (P0 XOR M0) = (P1 XOR P0) XOR (M1 XOR M0)`. Each changed output bit requires at least one changed source bit; the number of output changed bit/nibble/byte positions cannot exceed the corresponding number of changed source occurrences (sum across layers). No counterexample was identifiable under these assumptions.

One presentation nuance: a changed-byte **span >= 5** means `max(changed indices)-min(changed indices)+1 >= 5`; it does not mean five consecutive byte indices are all changed. The text's 'union ... must span at least five consecutive positions' is mathematically defensible as interval width but could be read as five occupied positions. Consider saying 'union minimum-to-maximum byte-index span must cover at least five byte positions, with gaps allowed'.

The bounds are necessary only, never sufficient, and they do not infer physical source edits. No accepted K04/K08 was found in my spot-check of original case material.
