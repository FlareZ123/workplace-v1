# K04: fixed in-band linear integrity cannot reconstruct the selected coupon

**Agent 36, 19 October 2026. Result: no K04 component accepted or recovered.** This is a new recovery-mechanism test, independent of the original K04 acceptance hash. It asks whether the intact-looking printer records themselves define a shared linear parity/check-code that could detect or repair a damaged sixteen-byte RECOVER coupon.

## Why this mechanism was worth testing

The original `evidence/print/spool-reconstruction.log` records opaque 16-byte payloads and explicitly warns that payload integrity was not verified; `evidence/records-custodian.txt` and `mail/16.eml` also say dispatch ACK does not certify recovered bytes. A fixed in-band parity or systematic Reed–Solomon-style code would be an independently testable printer-data invariant. If present on the regular RECOVER cohort, it could turn the source integrity problem into error detection or, subject to redundancy, correction **before** consulting the original K04 commitment.

The reproducible code [`agents/agent36/k04_linear_integrity_gate.py`](../agents/agent36/k04_linear_integrity_gate.py) reads only the original source spool, pins its SHA-256 to `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`, and tests no candidate against `acceptance.json`. It includes synthetic even/odd parity positive controls.

## New observed constraint

The spool contains 128 regular `+00:00` rows and five separate `Z`-timestamp RECOVER-tail rows. Exactly **35 of the 128 regular rows have `CLASS=RECOVER`**, providing a directly relevant independent training cohort without using the five suspect tail entries.

| Sample and field | Matrix shape | Observed rank | Meaning |
| --- | --- | ---: | --- |
| 128 regular payloads as GF(2) bit vectors | 128 x 128 | **128** | No nonzero homogeneous bit-parity equation holds for every regular payload |
| All 133 payloads with a constant 1 column | 133 x 129 | **129** | No nonzero **affine** GF(2) parity-check equation holds for *all* recorded printer payloads |
| 35 regular RECOVER payloads as GF(256) 16-byte vectors | 35 x 16 | **16** | No nonzero homogeneous byte-linear equation holds throughout this source-relevant cohort |
| The same RECOVER records with a constant 1 byte | 35 x 17 | **17** | No nonzero **affine** byte-linear check holds across the 35 regular RECOVER records |

The GF(256) ranks were separately computed using the irreducible field polynomials `0x11B` and `0x11D`, with the **same full ranks for both**. The regular-only augmented GF(2) matrix has rank 128, while the five tail records raise the combined augmented rank to 129. An affine relation fitted to the 128 regular records is therefore not a genuine all-cohort invariant.

## Implication for new K04 cracking

A fixed affine parity check shared by all 133 observed 16-byte printer outputs would force the 133 x 129 augmented matrix to have rank below 129. It does not. More importantly for source-selected K04, a fixed **GF(256)-affine Reed–Solomon-like relation common to all 35 regular RECOVER payloads** would force the 35 x 17 augmented matrix to have rank below 17. It does not. Thus these forms of automatically recoverable *in-band* linear redundancy are **contradicted by the original printed bytes** under the premise that the regular training cohort represents legitimate codewords.

This tests a genuinely different mechanism from word flips, byte mosaics, metadata-generator fits and arbitrary hash-conditioned output guesses. It does **not** exclude a bit-level CRC exclusive to RECOVER records, nonlinear authentication codes, different coding families for the tail, a code dependent on unavailable job-specific keys, or damaged regular training records. It does not establish which source layer is wrong, and the source gives no positive statement that any such code was used. A future proposed integrity method should supply an original printer-format witness and produce a consistent checksum on regular RECOVER records before trying to correct the selected attempt-2 ACK.

**Acceptance status:** K04 remains unknown; K08 is unaffected. The original acceptance files, source records and checker were not altered. This result explains why a broad family of appealing self-repair approaches has no support, without claiming the correct physical coupon cannot be recovered by another mechanism.


## Unknown-polynomial cyclic CRC reconstruction, tolerant of damaged training rows (Agent 36)

An independent reconstruction hypothesis is that the sixteen bytes are complete codewords of one printer CRC family, with a fixed but **unknown** generator polynomial and common residue. All complete valid codewords would have the same remainder modulo that polynomial. Therefore their pairwise XOR differences must be divisible by the unknown generator, regardless of fixed CRC initial register, final-XOR convention, or constant affine residue (provided the complete payload is the codeword in the tested bit orientation).

Unlike testing only known CRC32/Adler32 implementations, the [generator-agnostic polynomial GCD SFT](../agents/agent36/k04_cyclic_crc_gate.py) computes the GF(2)-polynomial GCD of differences among every four of the **35 original regular RECOVER rows**, then tests whether a fifth original row shares a factor of degree at least eight. This checks **52,360 distinct four-row subsets per orientation**. The code pins the original spool source SHA-256, reads no original acceptance or target hash, and includes a positive example in which five true 16-bit-CRC codewords amid 30 deliberately unrelated values are detected.

| Complete-codeword bit interpretation | Four-row subsets admitting a common degree-8+ polynomial | Five-row subsets admitting a common degree-8+ polynomial |
| --- | ---: | ---: |
| Raw byte order, most-significant-bit polynomial coefficients | 2 | **0** |
| Reversed byte order | 0 | **0** |
| Reverse all 128 bits | 2 | **0** |
| Reverse the eight bits within every byte | 2 | **0** |

The maximum four-row GCD degrees were respectively 8, 7, 9 and 8. The few chance-compatible four-row groups fail on a fifth row. If **any five** of the 35 retained regular RECOVER payloads were intact codewords using one fixed unknown cyclic CRC with at least eight parity bits and a common residue under one of these complete-word interpretations, their differences would have yielded a five-row common factor of degree 8 or greater. None does. This conditional negative remains valid even under a strong outlier allowance of **30 out of 35 damaged or unrelated records**. It does not rely on the source-selected K04 commitment.

**Scope:** CRC redundancy might exist in another field, in a subset of bits with intervening protocol framing, or under different metadata-specific generators, and a nonlinear error-correcting scheme remains possible. The source provides no affirmative printer-format CRC specification, so this result excludes only the exact full-word cyclic-code mechanism. In particular the isolated four-row GCD factors do **not** authenticate K04 bytes or justify extrapolating a CRC from them. K04 and K08 remain unresolved, with original acceptance unchanged.
