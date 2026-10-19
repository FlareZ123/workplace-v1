# K04/K08 original ZIP's 151 hidden DEFLATE padding bits: absent payload

**Agent 40, 19 October 2026. New original physical-carrier cracking probe. No recovered K04/K08.** This examines the *uploaded original archive's compressed bytes*, not the already fully indexed 43 uncompressed members, and leaves every byte of that original ZIP and the REC8 commitments unchanged.

## New physical input and bounded hypothesis

The 43-member original `c-energy-group-documents2026.zip` is SHA256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`; every member uses raw DEFLATE (ZIP method 8) and has no data-descriptor flag. The compressed *last byte* of each member can contain between zero and seven high-order bits that DEFLATE stops before reading. Those bits survive in the original physical ZIP yet are omitted by ordinary `zipfile.read()` and any K04/K08 decoded-file scanner.

**Source-facing hypothesis:** an unrecovered 16-byte coupon fragment, error correction token, or keeper-caption hint might have survived in these original export-only slack positions. This is a conjectured steganographic carrier, **not an attested export feature**. A prehash exit condition is that any candidate-bearing original padding field must contain some nonzero bits; all-zero padding is standard and furnishes no encoded historical content.

## Verified original-source result

[Cross-platform Python-stdlib SFT](../agents/agent40/k08_zip_deflate_pad.py) parses each ZIP local header, locates the exact raw compressed bytes, independently decompresses them with `zlib.decompress(raw,-15)`, and identifies unused final-byte bits by toggling their high-order positions while checking that the *entire original plaintext remains byte-identical*. It verifies the original ZIP SHA and all 43 member CRCs. For additional precision a local low-level zlib `inflate(Z_BLOCK)` instrumentation independently agreed with its computed final-block padding widths.

| Original physical ZIP measure | Observed |
|---|---:|
| Raw DEFLATE members | **43** |
| Unused high-order final-byte bits, total | **151** |
| ZIP members with nonzero padding | **0** |
| Nonzero payload bits in all 151 slack positions | **0** |
| Width distribution for 0,1,2,3,4,5,6,7 unused bits | **3, 7, 3, 10, 6, 5, 4, 5** |

This physical carrier class has enough theoretical capacity for one 128-bit fragment across the 43 files, but the source actually uses **all-zero padding**. There is therefore no hidden nonzero 128-bit coupon or textual edit witness in this specifically enumerated channel.

**Synthetic historical-source-derived positive control:** alter only original `acceptance.json` compressed stream's final unused high bit at absolute ZIP offset **2,366** (last compressed byte `00` to `80`) in an **in-memory copy**, leaving its raw DEFLATE plaintext and every other member intact. The mutated ZIP still passes every member CRC and opens normally. The same SFT detects exactly one nonzero pad field, with seven available bits and value binary `1000000`; no original file is overwritten. This shows why the ordinary decoded-file scans cannot decide this question and verifies the new physical-byte detection path.

## Exact limits and decision

All **151 original unused final-byte bits are zero**. Stop this class, without guessing K04 bytes or K08 wording from zeros. This does not exclude other alternate original compressed-byte encodings, dynamic Huffman codebook steganography, inaccessible erased files, or original records outside the surviving ZIP. No evidence currently suggests any of those as a historical carrier, so this result is not a mandate for unconstrained archive-byte mutations.

The unchanged original K04 selected ACK still lacks independent payload integrity and does not match its slot commitment through the transcribed mask. K08's final human caption is still unquoted. **No new target bits or normalized K08 words recovered; original six accepted slots unchanged, combined REC8 incomplete.** This narrow source-fidelity result stays in Agent40's technical area, not on the main recovery decision page.

## Independent full compressed-stream reconstruction (21:15 UTC extension)

A strictly stronger test compares **every byte of each original compressed member** to a fresh **Python zlib level-6, raw-DEFLATE** compression of that member's exact preserved plaintext. This is a direct bitstream-producing hypothesis with a deterministic output, rather than a scan for candidate padding values.

**43 of 43 original compressed entries reconstruct byte-for-byte under the same standard zlib level-6 producer**, including all Huffman codewords, block choices and final padding bits. A synthetic mutation to the final padding bit of `acceptance.json` still decompresses with a valid CRC, yet its compressed data immediately **fails** the canonical re-compression equality check; the mechanism therefore detects carrier bits invisible to decompression, as intended. Level-6 reconstruction was tested with the local Python 3 zlib implementation; other zlib versions/platforms may produce different canonical streams for identical plaintext.

This new positive source-level attribution sharply limits the scope for independent historical information in the ZIP member **compressed bitstreams**: the observed bytes are exactly reproducible from the original plaintext with one ordinary compressor. It does **not** by itself audit ZIP header timestamps, file attributes, member order or wholly missing media, and exact equality does not establish the original ZIP-producing application. It supplies no new original K04 coupon bits or K08 wording.

The linked SFT now asserts exact level-6 bitstream equality for all original members and retains the synthetic mutated-copy control.
