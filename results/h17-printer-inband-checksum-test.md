# H-17 printer payload: small checksum-structure audit

Agent 17, 18 October 2026. **Narrow negative result.**

The printer spool has 133 complete 16-byte PAYLOAD fields, including 128 regular timestamp entries and five Z timestamp entries. The custodian says a dispatch ACK does not independently validate a payload. I tested a limited potential source structure: a common CRC32 or Adler32 in the first or last four bytes, stored in big- or little-endian order. A fixed XOR offset was also considered, because if a cohort used it, two or more intact entries would have the same observed-versus-calculated offset.

The read-only standard-library implementation is [check_h17_spool_inband_checksums.py](check_h17_spool_inband_checksums.py). The original input hash is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. It tests all 133 lines and the regular (128), Z-tail (5), RECOVER (40), and RECOVER Z-tail (5) subsets. Every one of the eight checksum-format combinations gave zero plain matches and no duplicated fixed offset within any cohort. Synthetic positive controls validate both direct CRC32 and a fixed-offset CRC32.

**Interpretation:** none of these specific common in-band four-byte checksum models is supported by the retained records. The test cannot confirm the selected K04 printer bytes. Other checksum encodings and all unavailable original media remain out of scope. The case record never states that the opaque 16-byte PAYLOAD format embeds a checksum. The original K04 acceptance mismatch persists; K08 remains absent; six other components remain accepted. No source file or acceptance commitment was changed.
