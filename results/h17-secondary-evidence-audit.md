# H-17 secondary evidence audit: ZIP container and K08 caption fragments

**Researcher:** Agent 8. **Date:** 17 October 2026. **Source:** supplied 4 October 2026 export 06, compared with the repository `resources/` copy already shown byte-identical in [export equivalence](h17-export-equivalence.md).

## 1. ZIP container examination

Question: could the two missing components be preserved as ordinary ZIP metadata, appended bytes, or an unreferenced data region even when the extracted member files do not reveal them?

The supplied `c-energy-group-documents2026.zip` has SHA-256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`. Parsing local headers, central directory and the end-of-central-directory record with Python's `zipfile` and `struct` yielded:

- 43 unique member paths; all 43 DEFLATE-compressed; `ZipFile.testzip()` returned `None`, meaning no member CRC failure.
- No archive comment, member comments, member extra fields, encrypted member flags, or bytes after the end-of-central-directory record.
- First local file header begins at byte 0. All local records are contiguous as measured by their recorded compressed sizes and local-header filename/extra lengths; last stored member ends at the central-directory start, byte 36,311. No gaps between those regions.
- Central-directory size 3,093 bytes; offset 36,311; EOCD offset 39,404; file length 39,426. Its member count is 43.

This rules out simple recovery of extra source bytes from **those standard ZIP metadata fields or unallocated intervals** in the supplied copy.

A further raw-DEFLATE inspection, reproducible using [the ZIP driver](audit_h17_zip.py) and [zlib helper](measure_raw_deflate_slack.c), used zlib's documented `inflate(..., Z_BLOCK)` end-of-block status and `z_stream.data_type` unused-bit count to identify the unused high bits of each final compressed byte ([zlib manual](https://zlib.net/manual.html)). Across 43 complete streams, 151 unused final-byte padding bits were identified (bit-count distribution: 0:3, 1:7, 2:3, 3:10, 4:6, 5:5, 6:4, 7:5). **All 151 padding bits were zero**; no excess compressed bytes remained after the DEFLATE end marker, and recompression decoded to precisely the recorded file contents. This excludes another simple carrier: nonzero content in final-byte DEFLATE slack bits, without asserting that arbitrary compressed-stream steganography is impossible.

**Bit-for-bit compression reproduction:** For every one of the 43 known original member payloads, Python's standard-library `zlib.compressobj(level=6, wbits=-15, strategy=Z_DEFAULT_STRATEGY)` produced exactly the original raw-DEFLATE compressed stream. There were 43 matches, 0 differences. This indicates the ZIP's compressed streams can be explained fully by ordinary default zlib compression of the known member contents. The [ZIP audit driver](audit_h17_zip.py) now reports exact comparison counts in its output. This is evidence against alternate-bitstream covert content for these stored entries; it does not authenticate the underlying extracted records or prove the trim includes all originals. It does not prove there is no steganographic information within member contents or compressed bitstreams. It also says nothing about the unavailable original coupon or keeper's desk margin. [The prior copy equivalence audit](h17-export-equivalence.md) establishes this ZIP and the repository's 43 source members have the same file bytes.

## 2. Bounded K08 fragment-composition test

Hypothesis: the keeper's final caption may have been formed by joining two contiguous verbal fragments from Emily's surviving numbered desk notes. This is a source-grounded hypothesis; the records **do not** establish that Emily did so.

The read-only, standard-library program [test_h17_k08_splices.py](test_h17_k08_splices.py) uses only Emily-authored notes `N02, N06, N10, N13, N20, N23`; it deliberately excludes the two explicitly rejected labels `N17` and `N18`. Extracting every normalized contiguous span of 2 through 12 words yields 1,030 distinct fragments. Every **ordered pair** is tested after joining with one of five separators: a space, " and ", " while ", " as ", or " when ". Each resulting phrase is tested using the exact K08 HMAC-SHA-256 derivation and SHA-256 slot acceptance, without altering the nonce or target.

**Result: 5,304,500 candidate evaluations; zero K08 acceptance matches.** The notes' SHA-256 is `13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb`. This excludes only the defined two-fragment construction class. It leaves three-fragment captions, different connectors, reformulations, other source passages, and unknown original wording unresolved. The original acceptance commitment cannot supply missing text by itself.

## 3. K04 independent coupon intake

The new read-only [check_h17_coupon.py](check_h17_coupon.py) accepts an independently recovered **16-byte original coupon RECOVER payload** in hex, XORs it with the unchanged recorded K04 mask and compares SHA-256 with the untouched slot target. Testing the export 06 ACK-attempt-2 payload `A9A9DC5731A5E2AE879C47215C2559D5` produces component `2CFF149C50E54557228E7DE60B3EB7C9`; its SHA-256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b` is different from K04 target `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`. Output is **NO_MATCH**. The new checker does not imply that any new authenticated coupon has been found.

## Conclusion

The six proven components remain unchanged. The unchanged verifier still reports K04 and K08 missing, combined incomplete, accepted false. Remaining decisive evidence would be an independently integrity-checked original ESC-N coupon/buffer and an authenticated exact final keeper caption or contemporaneous quotation. No such evidence was found in this run. Avoid promoting failed or merely plausible candidates.
