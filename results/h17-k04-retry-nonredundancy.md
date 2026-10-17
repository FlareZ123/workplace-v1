# H-17 K04 retry-payload nonredundancy certificate

**Agent 12, 18 October 2026.** This is a source-grounded diagnostic of whether the three same-job `CLASS=RECOVER` attempts provide multiple near-identical copies suitable for simple error correction. It does not search the K04 acceptance hash, change original evidence, or establish which unpreserved bytes are correct.

## Exact observed fields

The 3 October logical printer route `ESC-N` is `PS-261003-0417` per `resources/evidence/archive-labels.ini`. The exact-job RECOVER rows in `resources/evidence/print/spool-reconstruction.log` are:

| Attempt | State | 16-byte retained payload |
| --- | --- | --- |
| 1 | REQUESTED | `CD3E4F216ADB2FB180DA2AA90B33F7A4` |
| 2 | ACK | `A9A9DC5731A5E2AE879C47215C2559D5` |
| 3 | REQUESTED | `44D53DFC29D7943A95D89371DA58EC64` |

Pairwise 128-bit Hamming distances are **68 bits** (1 to 2), **62 bits** (1 to 3), and **62 bits** (2 to 3). There are **zero identical same-position bytes** for each pair. For context, independent uniformly random 128-bit values have an expected pairwise Hamming distance of 64 bits. The observed distances are compatible with unrelated random-looking payloads, though randomness or independence cannot be proved by three samples.

## Conditional mathematical bound

Under the additional **hypothesis** that all three retained records were corrupted versions of a **single identical original 128-bit coupon**, any putative common source must incur at least **96 total bit edits** across the three recorded words. At each bit position, the minimum number of edits is achieved by their majority bit; the observed sum of three pairwise distances equals 192, hence the minimum total is 192/2 = 96.

An explicit majority-bit consensus word is `CDBD5D7529D7A6BA85D803215A31FDE4`; its distances to attempts 1, 2 and 3 are **34, 34, 28** respectively, totaling 96. The 68-bit separation between attempts 1 and 2 proves, by the triangle inequality, that *every* common center is at least 34 bits away from at least one attempt. The displayed consensus attains this limit. Thus the exact **minimum covering radius is 34 bit flips**. All-three-copy repair assuming at most 33 bit errors per attempt is mathematically excluded.

The original records do **not** state that the attempts printed identical source payloads, and attempts 1/3 were unacknowledged. This conditional bound cannot be used to estimate how many erroneous bits, if any, occur in ACK attempt 2. It neither proves corruption nor recovers K04. The written K04 routing rule still chooses **attempt 2** and its mask-XOR output `2CFF149C50E54557228E7DE60B3EB7C9` fails the original commitment.

## Research implication

Previous cross-attempt byte-mosaic searches are computationally valid bounded tests, but the available payloads themselves furnish **no observed low-error redundancy** justifying majority voting or near-copy repair. Prioritize independent original coupon/buffer evidence or a source-backed mechanism identifying how these separate values relate. Do not interpret retry number as an error-correcting replica guarantee.

Reproduce exact selected rows and counts with [the read-only standard-library checker](check_h17_retry_geometry.py): run it from a repository checkout with unaltered `resources/`. Current REC8 status remains **six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false**.
