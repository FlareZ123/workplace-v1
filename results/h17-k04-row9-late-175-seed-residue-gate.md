# K04: new 175-state CPython seed-word residue gate

**Agent 15, 20 October 2026 ~14:49 UTC. Conditional original-source producer falsifier, not recovered coupon bytes.**

## Distinct original source anchors

The source-pinned printer/AX-7778 alignment used by Agent26 derives a first initialized-state fragment from intact printer rows 9/33/63 and three observed AX high-16 checkpoints:

- S[p-174] = 418BDA1E, S[p-173] = 2E02BC3D, low31(S[p-172]) = 38EBB043.
- Independently, intact-printer MT recurrence yields S[p+1] = C517EB25, S[p+2] = 7D3AAF35, low31(S[p+3]) = 31FD69FC.

These states are conditioned on the common-MT/first-cycle source chronology. Original spool SHA256: 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083. Original transfer-audit SHA256: 32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf.

For a CPython random.Random(int) seed with n 32-bit key-array words, the init_by_array update at index i consumes KEY[(i-1) % n]. Each displayed two-fullwords-plus-next-low31 fragment allows algebraic inversion of its consumed key-word low31, using the fixed CPython mixing multipliers and initial state. The update indices p-172 and p+3 differ by exactly **175 draws**. For every n dividing 175, namely **1,5,7,25,35,175**, they must use the **same key word** and yield identical low31 bits; both partial inversions are exact modulo 2^31 without guessing high bits.

## Executed original-data discriminator

An independent standalone read-only Python implementation extracted both original fragments from the unchanged 43-member ZIP (never reading disputed row129). It tested all 219 phase placements p=402..620, where the two fragments can be first-cycle initialized state. **All six key-array lengths yielded zero matching phase placements.** Illustrative original n=5 values:

- p=535: row9-derived 518215E1 versus late-derived 30D5813B;
- p=564: row9-derived 43E0D367 versus late-derived 14F6FDDB.

The SFT reproducer [source-linked test](../agents/agent15/k04_row9_late_175_seed_sft.py) pins the two original file digests, reconstructs original rows and AX checkpoints using Agent26's established source-only routines, then performs the new paired-residue inversion. 72 synthetic positive tests across all six key sizes, six phases and two numeric seeds use actual CPython random.Random initialization and recover the correct shared key-word low31 bits.

**New class-level implication:** Earlier Agent14 five-word/160-bit reconstruction excluded p=396..563 under its conditional model but left p=564..621 unexamined. The new source-anchored row9↔late identity extends the n=5 exclusion through **p=620**, adding p=564..620 under the extra AX row9 alignment. Key sizes 25,35,175 are additional conditional exclusions; sizes 1,7 were previously excluded by other source-conditioned relations and serve as controls here. At p=621 the late S[p+3] would cross the initial-state boundary; this gate makes no claim there.

**Limit:** This does not authenticate a historical shared CPython generator or a physical ordering of AX and printer outputs, and it does not recover original coupon bytes. Actual selected K04 bits **0/128**, K08 exact final words **0**. Six established slots pass, K04/K08 missing and original combined acceptance still incomplete. Prefer an independently held original target witness over further seed-length sieve expansions.
