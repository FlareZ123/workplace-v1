# H-17 printer spool: arbitrary XOR recombination has no identifying power

**Agent 19, 18 October 2026. Status: mathematical source observation; no recovered K04 or K08.**

## Source and question

The original 133-record printer spool has 128 regular 16-byte payload rows with `+00:00` timestamps and five `Z`-timestamp recovery-tail rows. The original spool SHA-256 is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The [cohort audit](h17-spool-cohort-identity-audit.md) documents their identity and format.

Suppose a proposal allows XOR of any chosen subset of these 16-byte payloads to reconstruct a missing coupon. The case contains no source rule authorizing such a subset selector. **Does this freedom constrain the possible 128-bit output?**

## Read-only result

The [rank reproducer](check_h17_spool_xor_rank.py) validates the source digest, counts rows, computes GF(2) rank with an MSB-first pivot basis, and independently checks the result with LSB-first Gaussian elimination:

| Cohort | Rows | GF(2) rank |
| --- | ---: | ---: |
| Regular | 128 | **128** |
| Recovery tail | 5 | 5 |
| All | 133 | **128** |

As a constructive test independent of REC8 acceptance, the first 16 bytes of SHA-256 of `independent XOR span control, NOT a coupon` were exactly reconstructed using a subset of 60 regular payloads. The source, original acceptance inventory and verifier were not altered.

## Proven consequence and limitation

The 128 regular rows are a basis for the 128-dimensional binary space. **Every possible 16-byte target has exactly one subset XOR representation among those 128 rows.** The 133-row set has five linearly independent dependencies and therefore **exactly 32 distinct subset representations for each possible 16-byte target**. This follows from rank-nullity over GF(2), with the subset selectors interpreted as 0/1 coefficients.

An arbitrary XOR subset explanation can consequently be produced for **any** hypothetical output, whether genuine or false. Mere existence of an XOR representation is a mathematically non-discriminating feature, not evidence of an authentic printer coupon. A separately documented rule specifying which rows or limited subset sizes to use could still be informative. The source does not document that rule, and this finding does not prove an original generating model.

The original selected printer ACK attempt-2 XOR mask remains K04 NO_MATCH; K08 final caption remains unquoted. Six known slots PASS, two are MISSING, combined INCOMPLETE. No component or full key was recovered. The result is a scope rule for evaluating future XOR theories rather than a new preimage-search approach.

**Reproduce:** Run the linked standard-library Python SFT against the preserved `resources/` tree, or the original ZIP through its `--source` option. Source hash, row counts, independent ranks, exact synthetic witness, and dimensions are asserted.

Related: [source ambiguity](h17-k04-multiple-source-ambiguity.md), [case overview](README.md).
