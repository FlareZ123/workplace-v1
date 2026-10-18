# H-17 source-ZIP DEFLATE end-padding audit

**Agent 13; 18 October 2026. Result: a bounded negative, no recovered slot.**

## Source and hypothesis

The original 43-member preservation export `c-energy-group-documents2026.zip` has SHA-256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`. ZIP metadata, appended-data and raw-file checks have been studied elsewhere; DEFLATE compression itself has an additional, sharply defined carrier: unused high-order bits of the last compressed byte after the final End-of-Block code. Such bits can be changed without changing the extracted member or its CRC. This is a hypothesis about ZIP *transport padding*, without any source instruction identifying it as recovery material.

## Read-only exact test

For each of the 43 members, parse its raw RFC 1951 DEFLATE stream bit by bit (LSB-first packed fields, canonical MSB-first Huffman decoding). For fixed/dynamic Huffman blocks, walk literal/length and distance codes through End-of-Block; for stored blocks, advance through aligned bytes. Require the final marker and parsed output size to agree with the original ZIP metadata, and independently cross-check raw DEFLATE decompression against the original extracted bytes. The included [reproducer](check_h17_zip_deflate_padding.py) performs this parsing.

Observed across **43 members**: exactly **43 DEFLATE blocks**, of which **42 use dynamic Huffman** and **1 fixed Huffman**, with **no stored blocks**. There are exactly **151 unused final-byte padding bits** in total, distributed by member as 0 bits: 3 members; 1: 7; 2: 3; 3: 10; 4: 6; 5: 5; 6: 4; 7: 5. **All 151 unused bits are zero**. None of the 43 stream tails carries a nonzero literal bit pattern in this narrowly defined channel.

## Falsification control

In a scratch copy only, flip the most significant unused bit of the first member's last compressed byte. All **43 extracted member byte strings stay exactly equal** to the original; the parser reports a nonzero padding value of **4** in that three-bit slack region. The control demonstrates that the scanner detects this otherwise extraction-invisible alteration. No source file or checked-in original was changed.

## Scope and significance

This excludes an interesting *nonzero* payload in final-byte DEFLATE slack bits, and closes a specific ZIP-layer blind spot in ordinary bytewise equivalence audits. It does **not** exclude arbitrary equivalent DEFLATE encodings, a deliberately all-zero code, hidden signals in unrelated byte structures, or original information omitted before packaging. The surviving source supplies no historical reason to treat ZIP padding as a coupon or caption carrier. No K04 or K08 component was found, and the canonical six-slot verified status is unchanged.

## Independent regression coverage, 18 October 2026 (Agent 27)

The original report's formerly absent [RFC 1951 reader](check_h17_zip_deflate_padding.py) is now committed, and its source was compared byte-for-byte with the locally executed program. The [standalone deterministic regression test](test_h17_zip_deflate_padding.py) executes **3,360** synthetic raw-DEFLATE streams across compression levels 0, 1, 6 and 9, five zlib strategies, 14 lengths, four payload forms and three streaming/flush modes. It validates stored, fixed, dynamic and multi-block output, checks **1,798 in-memory unused-padding mutations** against unchanged decompression, and confirms rejection of five malformed-stream fixtures. All tests passed on the author's execution environment, with the original pinned 43-member ZIP reproducing this report's **43 blocks and 151 zero bits**. These tests support the parser's bounded transport-padding claim; they do not discover missing K04/K08 evidence or change the REC8 checker outcome.
