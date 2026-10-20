# H-17 K04: complete two-ended four-byte retained-fragment repair class, NO_MATCH

**Agent 8, 20 October 2026 ~00:32 UTC.** This is a fully completed **direct original K04 candidate attack** on a new, tightly scoped 32-bit media-repair class. It recovered no K04 component and does not authenticate a historical corruption mechanism. K08 remains unquoted.

## New testable source-layer mechanism

The original spool `evidence/print/spool-reconstruction.log` explicitly describes itself as a **retained-fragment buffer reconstruction** and disclaims independent payload integrity. Original `mail/16.eml` says dispatch ACK does not authenticate the media bytes, distinguishing the selected ACK from an actual verified coupon. The incident-date label and route select the 18:02Z attempt-2 ESC-N RECOVER ACK for job `PS-261003-0417`. Its exact original 16-byte payload is:

`A9A9DC5731A5E2AE879C47215C2559D5`

The repeated `A9A9` at the payload's front is an observed reason to **consider**, but it is insufficient evidence to assert, first-edge corruption. The proposed finite model is a fragment reconstruction that retains **the middle 12 bytes** while replacing two boundary bytes on each side. Treat original payload bytes at zero-based positions `0,1,14,15` as wholly unknown. The suffix pair is part of the bounded hypothesis; the supplied record gives **no independent evidence** it is damaged. The model applies equally to the reduced K04 candidate's four edge positions under XOR with the unchanged mask.

Original route mask: `8556C8CB6140A7F9A5123AC7571BEE1C`. The selected reported reduction is `2CFF149C50E54557228E7DE60B3EB7C9`, whose original SHA256 is `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b` and whose unchanged original K04 commitment is `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`. Original spool SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`; original full preservation ZIP SHA256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`.

The precisely specified original-target search is:

`K(a,b,c,d)= a || b || 14 9C 50 E5 45 57 22 8E 7D E6 0B 3E || c || d`

for all `a,b,c,d ∈ {0..255}`, applying unchanged SHA256 to each 16-byte candidate. This differs from the completed three-distinct-byte, four-nibble, contiguous-four-byte, word-lane periodic-XOR and one-unit insertion/deletion scans: all four edge bytes may change independently, with an interior intact span of **12 bytes** and changed-byte span **16**.

## Executed calculation

[Source-fixed read-only C SFT](../agents/agent8/k04_twoended_fragment_32bit.c) uses OpenSSL's existing SHA256 compression primitive on a single correctly padded 16-byte block, with a 32-bit encoded high/low pair for the four unknown edge bytes. Compiled and locally executed against the unchanged K04 target with GCC 14.2, OpenSSL 3.5.5 and OpenMP (five threads). A separate initial one-block known-answer check reproduced the Python standard-library SHA256 digest of the original reported baseline exactly. A synthetic positive injected `ABCD` as leading pair and `1267` as trailing pair; the tested high interval `[43981,43982)` found **exactly one**, with the expected complete synthetic candidate `ABCD149C50E54557228E7DE60B3E1267`.

A first monolithic scan was interrupted by the tool's runtime limit without a completed result and is **not counted**. The successful exhaustive run partitions the full 16-bit high-pair domain into sixteen disjoint half-open shards, each of width `4096`, and enumerates every `0..65535` trailing pair inside each shard. Each shard ran to its own printed `COMPLETE` counter:

| Leading two-byte high-pair domain (decimal) | SHA256 component candidates | Original K04 matches |
| --- | ---: | ---: |
| 0–4095 | 268,435,456 | 0 |
| 4096–8191 | 268,435,456 | 0 |
| 8192–12287 | 268,435,456 | 0 |
| 12288–16383 | 268,435,456 | 0 |
| 16384–20479 | 268,435,456 | 0 |
| 20480–24575 | 268,435,456 | 0 |
| 24576–28671 | 268,435,456 | 0 |
| 28672–32767 | 268,435,456 | 0 |
| 32768–36863 | 268,435,456 | 0 |
| 36864–40959 | 268,435,456 | 0 |
| 40960–45055 | 268,435,456 | 0 |
| 45056–49151 | 268,435,456 | 0 |
| 49152–53247 | 268,435,456 | 0 |
| 53248–57343 | 268,435,456 | 0 |
| 57344–61439 | 268,435,456 | 0 |
| 61440–65535 | 268,435,456 | 0 |
| **Complete union** | **4,294,967,296** | **0** |

The candidate positions, base bytes and digest constants are hardcoded from the original source in the committed SFT. The exact persisted C file was not separately compiled from a GitHub checkout; the local method-equivalent program supplied its tested outputs and positive control. Each shard's expected NO_MATCH exit code is 1, with its final counter and zero matches verified. Every subset covers `4096×65536` distinct candidate bytes; the intervals together cover the 32-bit space exactly once. The original source ZIP, route, acceptance digest and verifier were not edited.

## Inference and stop condition

**No accepted K04 coupon exists in the defined two-ended replacement class**, conditional on the reported ESC-N last-ACK and mask being the correct other input. This is a new direct missing-slot exclusion rather than a printer chronology/rank calculation. It cannot prove a fault type, certify the route/mask, recover any true original coupon bits, or exclude alternative damaged positions. There is no original evidence authorizing expansion to additional arbitrary unknown bytes, and doing so would exponentially enlarge an already explicitly speculative repair model.

The recurring genuine cracking bottleneck remains a separately authenticated original K04 payload/mask/producer witness and an exact K08 desk-caption original. K01/K02/K03/K05/K06/K07 are the accepted six; K04 and K08 remain unresolved, original combined acceptance incomplete.
