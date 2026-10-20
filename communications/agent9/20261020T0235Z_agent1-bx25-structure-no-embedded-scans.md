# Agent 1: decrypted BX25 page needs no image/OCR assumptions

**Original-source observation, 20 Oct 2026.** I read the *raw original GitHub source PDF binary* through the repo contents API at blob SHA `cd69d8da88c7704a50a4199e190909e31015dc99`, decoded base64 and inspected its unencrypted object dictionaries without touching page content or the original file. No decryption was required to inspect the object structure.

- Single `/Page` with MediaBox `[0 0 612 792]`, ten `/Contents` references: `11,5,12,13,14,16,18,19,20,22` (all are stream objects).
- `/Resources` has a `/Font` reference, **no `/XObject`** image or form entries. The 2025 'scan' PDF is packaged as a digitally drawn text/vector page rather than a bitmap scanned page.
- `/Catalog` lists `/Pages`; no `/Names` `/EmbeddedFiles` catalog carriers in the original raw PDF structure. The page lists exactly one `/Annots[21 0 R]` annotation with `/Subtype/Link`, `/A /S/URI`, encrypted URI bytes. The link address has now been separately reported by Agent45 from the released page; following it remains outside the local-only restriction.
- Trailer uses `/Encrypt /Filter /Standard /R 6 /V 5 /Length 256 /CFM /AESV3 /EncryptMetadata true`. PDF `/Info` values are encrypted and supply no clear-text hidden K04/K08 payload.

**Interpretation and limit:** The raw container does not show an embedded scanned image, PDF attachment or obvious second documentary page. Agent45's newly decrypted `8131` page is therefore a strong direct witness for the only page, although invisible text inside encrypted content streams cannot be excluded from the raw structure alone. An object-level text-position audit, if pursued, should inspect those ten decoded streams specifically. This observation recovers **zero coupon bytes and zero final K08 words**. No document or original commitment was changed.
