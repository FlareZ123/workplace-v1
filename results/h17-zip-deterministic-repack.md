# H-17 original ZIP is an exact standard-library repack

**Agent 13, 18 October 2026.** This is a reproducible, bounded source-packaging audit; **no K04 or K08 value was recovered**.

## Question

Can the source ZIP's bytes contain distinct information in its compression choices or ZIP structure, beyond the 43 decompressed evidence files and their ordinary metadata? Previous raw-member equivalence and ZIP comment/extra-field checks do not alone establish that the compressed representation is ordinary.

## Test

Using the **original supplied 39,426-byte** `c-energy-group-documents2026.zip` (SHA-256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`), read all 43 original members in their original order. Create a fresh in-memory ZIP with Python `zipfile.ZipFile` and `compresslevel=6`; for each member copy its recorded filename, timestamp and relevant standard `ZipInfo` metadata, but recompress **only the extracted contents** using the normal `zlib` backend. Compare the regenerated ZIP to the original byte-for-byte.

The read-only [reproducer](check_h17_zip_repack.py) also pins the original ZIP digest. Original reproduction environment: Python 3.13 with zlib runtime 1.3.1. Compressed-stream equality can vary across zlib builds, so a mismatch on another implementation would need interpretation rather than retroactively proving hidden data.

## Observations

- All **43 individual compressed streams** independently match the output of normal zlib compression at level 6 (some also match other levels).
- Recreating the entire ZIP gives **39,426 bytes**, identical at **every offset** to the source; regenerated SHA-256 equals original `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`.
- The complementary [DEFLATE end-padding audit](h17-zip-deflate-padding.md) counted 151 trailing slack bits across the members, all zero, with a scratch mutation positive control; source container regeneration reproduces those bits without any hidden input.

## Interpretation

For this exact local export and compressor version, all ZIP-level bytes are accounted for by the 43 extracted file bytes, ordinary ZIP metadata and deterministic standard compression. No *additional ZIP-container witness* for the missing printer coupon or final desk phrase was found. This is a statement about this particular source container. It says nothing about evidence omitted prior to packaging, possible semantic encodings *inside* extracted files, or cryptographic recoverability from acceptance commitments. The six-source-confirmed candidate stays unchanged; K04 and K08 remain unresolved.
