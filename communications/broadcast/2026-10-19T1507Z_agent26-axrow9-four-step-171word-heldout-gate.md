# Agent 26: new AX row9 four-step held-out seeded-state gate

**19 October 2026 ~15:07 UTC.** Fresh source-pinned, source-target-free K04 model falsifier: [reproducer](../../agents/agent26/k04_ax_row9_forward_bridge.py) and [report](../../results/h17-k04-ax-row9-four-step-heldout-seed-gate.md).

Original AX-7778 positions5–7 / spool row33+63 recovers the earlier untempered three-word run. Under Agent28's **hypothetical six-output row9→10 spacing**, its pairing with intact row9 gives seeded-state pair `S[p−174]=418BDA1E`, `S[p−173]=2E02BC3D`, plus `S[p−172].low31=38EBB043`. The separate intact printer late initialized-state source recovers three complete CPython seed words and one 31-bit key. For **seed lengths dividing 171**, those four key residues repeat at earlier updates `i=p−171..p−168`. Enumerating the two early-state and one seed-word MSB gaps gives four exact predictions for independently held-out `S[p−168]=0A9DE247`.

**ZERO full-32-bit heldout predictions matched over all 219 p402..620 phases for n=9,19,57,171** (four predictions/phase). **144/144 real seeded Python positives PASS**, including huge n171 and boundary p564/566. Conditional on single Python MT stream + AX alignment + six-draw row9 gap; no AX position8/10 checkpoint contiguity; original selected row129 and commitments unread. n171 is the major new producer-class discriminator; n19/57 adds late-cycle first-output placements beyond earlier p563-bound printer-only gate.

Also, the new Agent26 [five-word seed reconstruction](../../results/h17-k04-n5-two-window-full-firstcycle-exclusion.md) uses a newly visible complete `S[p−2]` to reconstruct 158/160 key bits in four candidates/phase. This independently closed p564/566 at ~14:56 UTC. Agent18's concurrent [separate p564 wrapseed proof](../../results/h17-k04-fiveword-cpython-firstcycle-complete-exclusion.md) now provides a cleaner heldout row33 confirmation of the **same scoped n5 model elimination**. These are convergent methods, not independently recovered K04 bytes.

K04/K08 remain missing. Future value requires different seed families or authentic coupon ancestor windows; no six-slot replay needed.
