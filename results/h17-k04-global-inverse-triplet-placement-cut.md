# K04: globally aligned MT inverse-triplet contradiction, independent of the disputed coupon

**Agent 4, 19 October 2026, 16:20 UTC. Result: a new source-only, three-observation placement exclusion. K04 target bits recovered: 0/128.** Reproducer: [`agents/agent4/k04_global_inverse_triplet.py`](../agents/agent4/k04_global_inverse_triplet.py). The original 43-member case export, all original commitments, and the original verifier are unchanged.

## Source and model

Use only the original 133 printer lines in `evidence/print/spool-reconstruction.log` (SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`). Suppress selected disputed row 129 **before** recovering any MT equations or output values.

The previously established source discovery yields 25 intact-word and 17 row-start inverse-twist recurrence witnesses. Treat each printer payload as four consecutive *untempered*, little-endian MT19937 32-bit words, and assume those witnesses refer to one monotone generator-output order. Place rows under those 42 exact equalities, with row-to-row start gaps in [6,24] for transitions 0..126 and [4,24] for transitions 127..131. The 6-draw floor is **conditional** on the post-payload DEST and pre-payload CLASS sampling interpretation from the prior source observations; neither this floor nor the 24-output cap is authenticated generator source code.

A 133-row feasible position vector has first start at 0 and final start at **957**, and a separate longest-path/difference-constraint certificate proves 957 is the minimum final position under the stated constraints. Merely satisfying all 42 discovered *positive* witnesses does not establish global consistency with MT19937.

## New exact source-only exclusion

The inverse recurrence is

```
X[t+624] = X[t+397] XOR twist(X[t].MSB, X[t+1].low31)

D = X[t+624] XOR X[t+397]
b = D >> 31
mixed = (((D XOR (0x9908B0DF if b else 0)) << 1) | b) mod 2^32
```

Here `mixed.MSB` must equal `X[t].MSB` and `mixed.low31` must equal `X[t+1].low31`. This gives an additional **three-observation** condition whenever surviving words occupy `t,t+397,t+624`, even if no observation exists at `t+1`. It is a local arithmetic exclusion requiring no full MT state inversion, no source-selected coupon, and no REC8 acceptance oracle.

Under one 42-witness-compatible **minimal-span** placement:

| Original intact spool source | Proposed stream index | Untempered word |
|---|---:|---|
| row 0, word 3 | 3 | `8A037AD0` (high bit 1) |
| row 54, word 0 | 400 | `AF4CF577` |
| row 83, word 3 | 627 | `A52674B5` |

The two later words imply `D=0A6A81C2`, `mixed=14D50384`, with high bit **0**. Original first word at index 3 has high bit **1**. Therefore no common MT19937 stream can satisfy **both** `s54-s0=400` and `s83-s0=624` with these three original words. This is a **joint, disjunctive placement cut**. It does not reject either record, the MT19937 model in general, or all possible global placements.

The reproducer checks all similarly triply anchored inverse conditions in the same complete position vector. **106** high-bit/low31 conditions are evaluable, and **38** are contradicted. The 42 positive discovery witnesses themselves still match exactly. Thus a globally valid source placement needs further ordering constraints beyond the 42 positive triples, even if its numeric total draw count is minimal.

## Evidence calibration and precise limits

- The code reads the original source with the existing SHA-pinned Agent23 witness scanner; it **never accesses** selected row129 content, the K04 XOR mask, the K04/K08 commitments or verifier. It explicitly verifies all 42 source equalities against the proposed vector and independently certifies its minimum span under the stated bounded-draw hypothesis.
- An independent synthetic `random.Random(20261019)` untemper/untwist check passes every index `t=0..275` against genuine output, including cases where one word is effectively hidden. Five separately generated seeded positive streams, 2,880 inverse cases in total, also passed during local investigation.
- The tested position vector is **one** feasible minimum-span assignment before this additional 3-observation filter, not the set of all minimizers, let alone all plausible historic producer assignments. This result does not establish a new lower bound for the authentic K04 coupon start or a recovered target bit.
- Prior pairwise group-stitching research already examined some inverse contradictions at *adjacent candidate gaps*; the present exclusion tests a **simultaneous global row assignment** and gives an explicit nonadjacent three-source disjunction. It must not be added to earlier gap-floor counts as though it were a new recorded word.

## Cracking leverage

A global MT placement/search should incorporate the inverse-triplet cuts while jointly deciding the two missing ancestor windows. A positional solver that accepts the positive 42 relations alone may put the missing coupon at a mathematically impossible stream phase. The 38 new contradictions give a checkable family of **no-good constraints on candidate stream alignments** before expensive GF(2) target-state inversion and original K04 acceptance testing.

The highest-value continuation would combine these constraints with independently indexed TRP2/RC-17/AX records and require an unseen intact printer prediction. The exact original K04 ancestor donor runs have **not** been found, so this is an improved cracking filter rather than an accepted coupon.

**REC8 remains six individual PASS, K04/K08 MISSING, combined INCOMPLETE, `accepted: false`.** K08's authenticated final desk-caption wording remains unquoted in the surviving export.
