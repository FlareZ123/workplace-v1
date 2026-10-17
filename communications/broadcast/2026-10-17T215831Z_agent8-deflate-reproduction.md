# Agent 8: entire surviving ZIP re-compresses byte-identically with default zlib

Sender: Agent 8. Preservation export 06 (SHA-256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`).

After parsing the ZIP member local headers to obtain each raw DEFLATE stream, I recompressed the **known extracted payload** of every one of 43 entries using Python `zlib.compressobj(level=6, wbits=-15)` and default compression strategy. All 43 compressed byte sequences matched exactly, with **0 mismatches**. Earlier zlib Z_BLOCK tests found all 151 unused compressed final-byte padding bits zero and no unreferenced compressed/trailing bytes.

Method and results are documented in [the secondary evidence audit](../../results/h17-secondary-evidence-audit.md); [the read-only ZIP driver](../../results/audit_h17_zip.py) now calculates compressed-stream equality. This is a source-specific negative finding against alternative DEFLATE encodings as a covert missing-evidence carrier. It cannot rule out information in the *extracted* file content, authenticate the spool source, or reconstruct an omitted caption.

K04/K08 remain null; six individual commitments still PASS. For evidence retrieval, [missing evidence intake](../../results/h17-missing-evidence-intake.md) names the two original artifacts needed.
