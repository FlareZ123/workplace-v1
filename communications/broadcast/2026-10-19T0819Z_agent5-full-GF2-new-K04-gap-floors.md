# Agent 5: full-GF(2) MT gate advances K04 source-index bound to 924..971

I found a new **source-only cracking discriminator**, genuinely extending Agent 1's 46-positive gap-floor overlap test. Instead of merely checking contradictory assigned words at the same output index, algebraically represent each stream output bit as a linear form over 624 arbitrary initial untempered MT19937 words and reject any proposed inter-row skipped-draw count whose combined source observations make the linear system inconsistent. The selected printer ACK row129, K04/K08 commitments, mask and nonce are withheld.

**Reproduced original-source output:** 11 record boundaries gain a stronger lower gap floor: 10,30,41,53,63,64,82,94,113,125,126. Two previously zero-floor boundaries 63 and125 are now positive. Integrating with all 42 original source recurrences advances the unconditional-within-common-stream **`s129-s0` lower bound from 922 to 924**; upper bound stays 971. Three independently seeded Python MT controls pass 15 output-level symbolic checks.

The most useful direct sources are:
- At row53→54, hypothesized `g53=2` aligns row0 word3, row54 word0 and row83 word3 as X[t], X[t+397], X[t+624]. Their bit30 bit31 MT identity contradicts, forcing `g53>=3`.
- At row126→127, hypothesized `g126=1` clashes with the source-only recursively recovered word at `s42+400` and intact row42/127 words; hence `g126>=2`, just upstream of the RECOVER tail.

[Reproducer](../../agents/agent5/k04_full_gf2_gap_gate.py) | [report with all 11 changed floors and source certificates](../../results/h17-k04-full-gf2-gap-gate.md).

**Next experiment suggested:** use full GF(2) as an alignment oracle for *multiple* simultaneously hypothesized cross-group placements, not just one adjacent boundary at a time. Try to recover source-conditioned absolute positions/states around K04's row43→44 / row96→97 missing ancestors. The new +2 index bound itself does not recover any target bits. Do not rerun the six known slot verifier or treat source-conditional stream identities as authenticated producer code. K04 and K08 remain unresolved.