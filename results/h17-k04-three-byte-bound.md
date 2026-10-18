# K04: exact three-distinct-byte substitution bound (Agent 32, 18 October 2026)

**Result:** zero original-commitment matches among **9,285,570,000 distinct** 16-byte K04 candidates differing from the selected retained XOR result in exactly three byte positions. Together with the independently reproduced zero-, one- and two-byte exclusions in [the earlier correction-footprint report](h17-k04-minimum-correction-footprint.md), this establishes a **minimum of four different byte positions** for any accepted value relative to this baseline. No K04 value, historical coupon or K08 final wording is recovered.

## Observed primary source and model

The incident-date ESC-N route in `resources/evidence/archive-labels.ini` selects job `PS-261003-0417`. `mail/16.eml` specifies its last acknowledged RECOVER attempt. `resources/evidence/print/spool-reconstruction.log` records attempt 2 as an ACK with 16-byte payload `A9A9DC5731A5E2AE879C47215C2559D5`. The transcribed `resources/evidence/recovery-routing.json` supplies XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C`. Their computed XOR is `2CFF149C50E54557228E7DE60B3EB7C9`, whose SHA-256 is `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`. It fails the original K04 SHA-256 commitment `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

**Hypothesis tested:** the reported 16-byte output differs from the original-hash-accepted value in exactly three, potentially nonadjacent bytes, while all other output bytes are correct. This is a mathematical correction class, **not** a claimed printer defect mechanism. Its source provenance is limited: the custodian warns ACK does not authenticate retained payload bytes; route mapping and XOR mask are transcriptions. The hash mismatch does not identify which source layer is wrong.

## Exhaustive method and validation

The [C scanner](k04-three-byte-scan.c) enumerates every ordered index triple `0 <= a < b < c < 16`, exactly `C(16,3)=560` triples. At each position it enumerates all 255 byte values other than that position's baseline byte. Each assignment therefore differs at **exactly** those three positions, with no duplication across triples. Total `560 * 255^3 = 9,285,570,000` unique candidate assignments.

For each one-block 16-byte SHA-256 message, it creates the standard 64-byte padded block, initializes an OpenSSL `SHA256_CTX`, calls `SHA256_Transform` and compares all eight 32-bit state words with the unchanged target digest. Five OpenMP threads were used in the completed local full scan; output:

```
K04 scan start: combinations=0..560, thread_max=5, selftest=0
checked=9285570000 elapsed=112.7504 found=0
```

The published version prints `threads=` and uses a loop over digest words rather than writing eight explicit comparisons; the comparison semantics and exhaustive range are identical. A separate **synthetic positive control**, using a high-level OpenSSL `SHA256` digest of the deliberately changed baseline at byte positions (0,5,15), correctly found `2DFF149C50E74557228E7DE60B3EB7CD` among the 16,581,375 assignments for that single triple. High-level Python `hashlib.sha256` independently confirmed the original baseline digest, XOR result, and enumeration cardinality. The synthetic control is an algorithm test, not an original-target match.

Input source SHA-256 fingerprints (read-only local extraction): `recovery-routing.json` `f8fcbca73d23bf1066edb88c088f89cd24cf22e7c78a4a412166254a4764d8a5`; `archive-labels.ini` `146fa698f44bc9b9fa7a443d8dc71a2e23ff0f883dabd01512f8ade82d3666ad`; `spool-reconstruction.log` `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`; `acceptance.json` `681739241b757b471acca4c0fef9d9d97e9493883887736d5db3b92bfb0c137f`.

Reproduction on a machine with OpenSSL libcrypto, a C compiler and OpenMP: compile `k04-three-byte-scan.c` with OpenMP and libcrypto (e.g. `cc -O3 -fopenmp -Wno-deprecated-declarations k04-three-byte-scan.c -lcrypto -o k04-three-byte-scan`), run with argument `selftest` and expect `found=1`, then run with no arguments and expect `checked=9285570000`, `found=0`, exit status 1. An optional pair of numeric arguments restricts the tested triple-index half-open range for sharding, without changing inputs. The complete original target run may return earlier if it finds a valid hit, but will always scan the declared range in the published code.

## Interpretation and limits

The precise new bound is **at least four changed byte indices** for any 16-byte K04 value satisfying the untouched hash, relative to the retained XOR output. Earlier independent tests additionally establish at least four changed nibbles, seven flipped bits, and an index span of at least five bytes. This excludes *only* the defined source-relative candidate class, including dispersed triple-byte errors. If the original mask and job selection were trustworthy, fixed-XOR symmetry transfers this byte-difference bound to original printer payload bytes. If those transcriptions were wrong, the same bound remains algebraic on the derived component and cannot diagnose printer damage.

Neither an accepted key nor its originating historical source is available from this test. K01/K02/K03/K05/K06/K07 remain original-commitment PASS; K04/K08 remain null; combined INCOMPLETE, accepted false. Consult the [source-sufficiency matrix](h17-source-sufficiency-matrix.md) before extrapolating. Further unguided mutation expansion is not a priority absent a documented source mechanism.
