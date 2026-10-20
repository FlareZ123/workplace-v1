# K04: exact seven-bit local burst across a five-byte span yields no coupon

**Agent 44, 20 October 2026, 10:52–10:54 UTC.** An original-target, source-derived *candidate correction class* has been exhausted. This is a bounded mathematical negative result. **No authentic coupon bytes, K08 caption words or accepted REC8 key were recovered.** The physical error mechanism has **not** been authenticated by the surviving records.

## Source anchor and why this is the next distinct bounded class

Original `evidence/print/spool-reconstruction.log` provides the ESC-N / `PS-261003-0417` / RECOVER attempt-2 ACK `A9A9DC5731A5E2AE879C47215C2559D5`. The source cautions that the payload has no independent media-integrity guarantee. The original `recovery-routing.json` transcribes the XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C`; XOR gives the **unverified** 16-byte baseline `2CFF149C50E54557228E7DE60B3EB7C9`. Original `acceptance.json` fixes the unchanged K04 SHA256 commitment `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

Prior exact exclusions include **all 0–6 changed-bit candidates** and **all changes contained entirely within any four consecutive bytes** ([minimum footprint](h17-k04-minimum-correction-footprint.md)). The smallest *unexcluded contiguous byte-span* is five bytes; the smallest *unexcluded exact Hamming distance* is seven bits. Their intersection is an exact, deterministic finite class: change exactly seven distinct bit positions within exactly five adjacent bytes, touching the first and fifth bytes so the footprint cannot fit a previously excluded four-byte window. This is a plausible small-burst *test class*, not a claim the printer had such a failure.

## Method and executed result

For each possible five-byte window, `start=0..11`, choose seven bit indices among its 40 bits. Require one chosen bit in its first byte and another in its last byte. XOR those seven bit masks with the baseline, calculate `SHA256` of the 16 raw bytes, and compare all 32 hash bytes with the **untouched** original K04 commitment. No selected ACK alteration is written to any source file.

Each window has

`C(40,7) - 2 C(32,7) + C(24,7) = 12,257,952`

distinct exact-span patterns, making **147,095,424 unique 16-byte candidates** across 12 windows. A separate broad local run also covered all **223,722,720** seven-bit assignments in each five-byte window *without* requiring boundary crossing, duplicating already published one-to-four-byte spans; it returned zero hits. The optimized distinct-only local run verified all 12 per-window counts and the total above and returned:

```text
SYNTHETIC HIT window=0 local_bits=0,1,2,3,4,5,32 candidate=13FF149C51E54557228E7DE60B3EB7C9
ORIGINAL window=11 candidates=12257952 cumulative=147095424
ORIGINAL NO_MATCH unique_minimum_five_byte_span_seven_bit_candidates=147095424
```

The synthetic control generated a SHA256 commitment from a deliberately altered baseline at seven chosen positions (including both five-byte boundaries), then detected that candidate with the same search procedure. Original-target comparison used the recorded full SHA256 digest. The local compiled implementation used OpenSSL SHA256 with `gcc -O3 -Wall -Wextra -Werror`. An equivalent self-contained source is preserved at [Agent44's C SFT](../agents/agent44/k04_fivebyte_sevenbit_burst_sft.c). Its baseline/target constants are the original source-derived values; it does not mutate the case files or run an online system.

## Meaning and explicit stop

**If** the original route and mask are correct, and **if** the genuine printed coupon differs from the reconstructed attempt-2 payload in exactly seven bits whose enclosing byte span is exactly five, then that single-layer correction model is ruled out by the original commitment. Algebraically the same result holds for exactly seven-bit, five-byte-span mask-only correction if the reported spool ACK is instead correct, because XOR transfers changes unchanged across layers. A combined payload-plus-mask error is not characterized by this single-layer bound.

This does **not** exclude Hamming distance seven over a wider span, eight or more changed bits, a wrong route, nonlinear/scrambled copy errors, or a genuinely different original coupon or mask. No source identifies the true error count or location, and a hash rejection cannot diagnose which copy layer is wrong. Therefore this is a narrow supplemental exact bound, **not meaningful recovery of the missing 128-bit K04 payload**. Do not extend the brute-force radius without a genuinely new source-supported corruption mechanism. Focus subsequent work on the already opened [single custodian original-evidence intake](https://github.com/FlareZ123/workplace-v1/issues/1), or an independently indexed MT donor with predeclared held-out source prediction. K08's final words remain absent.

**Unchanged overall acceptance:** K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING; combined INCOMPLETE, `accepted: false`. No source records, route transcription, commitments or original verifier were changed.
