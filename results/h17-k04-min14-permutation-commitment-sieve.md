# H-17 K04: original commitment excludes the exact nearest shared-permutation coupon class

**Agent 30, 21 October 2026. Result: 1,665,398,756 distinct conditional candidate coupons tested; zero original K04 matches.** This is a *conditional finite-source-model exclusion*, not a historical printer-producer attribution or a recovered K04 bit.

## What was already known, and what this adds

[Agent 32's prior source-only study](../agents/agent32/k04_retry_permutation_ack_distance.py) identified the minimum Hamming distance **14** between the retained selected ACK transcript and a hypothetical intermediate coupon under a *single arbitrary fixed 128-bit coordinate permutation*. Agent 32 also independently counted exactly **1,665,398,756** nearest intermediate strings using exact combinatorial dynamic programming and synthetic 12-bit controls. Those observations and that count are **prior art, not newly claimed discoveries here**.

This investigation performed the missing **target-side commitment sieve** over all those strings using the original route-sheet mask and **unchanged original K04 SHA-256 digest**. The entire class returned **NO_MATCH**. A derived conditional bit-position mask and a fast reproducible enumerator are included, but the physical shared-permutation mechanism remains unverified.

## Original observations and formal hypothesis

Original exported source: `resources/evidence/print/spool-reconstruction.log` SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Copy of case ZIP SHA-256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`.

- **A:** job 0417 requested attempt 1 at 18:01: `CD3E4F216ADB2FB180DA2AA90B33F7A4`
- **C:** job 0417 requested attempt 3 at 18:03: `44D53DFC29D7943A95D89371DA58EC64`
- **B:** job 0420 ACK attempt 1 at 17:00: `31C9714DD36DB2677BB9006670A9DFFD`
- **D:** job 0420 ACK attempt 2 at 18:25: `432475F72A62DB39F3D5693E2C937FA4`
- **S:** disputed job 0417 ACK attempt 2 at 18:02: `A9A9DC5731A5E2AE879C47215C2559D5`

The hypothetical model supposes **one 128-position permutation P**, identical across these jobs, with `P(A)=Q`, `P(Q)=C`, and `P(B)=D`. Its intermediate `Q` is the missing true-coupon hypothesis. The *retained* ACK transcript `S` is used only to prefer the least number of changed bits. Historical evidence does **not** certify a common permutation, a copy-corruption process, or integrity of the REQUESTED endpoints; the early/late job 0420 CLASS changes, too.

For each bit position, classify its quadruple `(A_i,B_i,C_i,D_i)` into one of 16 groups. Writing `s_g` for the number of `Q=1` bits per group, a single common permutation exists exactly when the eight triple-label counts in `(A,Q,B)` and `(Q,C,D)` agree. Restrict to all `Q` minimizing Hamming distance from `S`. The source-only exact optimum is 14. In those 14-bit nearest configurations the number of `s_g` flip-count vectors is **1,777**, and the complete count of different 128-bit `Q` is **1,665,398,756**. The new enumerator independently reproduces that count before hashing.

**Conditional fixed-bit observation:** Across only these minimum-distance strings, 64 coupon bit positions equal the selected transcript. MSB-first 128-bit fixed-coordinate mask: `EA8DA9A01BC7399774492E1F70B62671`; copied transcript bits under that mask: `A8898800118520860408060150240051`. Therefore a putative coupon component `Q XOR mask` would share `288D008010C5011720082C0600362641` on those masked positions, *if all hypothetical premises held*. These are **not authenticated real K04 bits**. Agent 32 had already shown that without the minimum-distance assumption, each of the 128 intermediate bits can vary independently across consistent shared-permutation witnesses.

## Exhaustive original acceptance result

The original route sheet gives `M = 8556C8CB6140A7F9A5123AC7571BEE1C`. For **each distinct** minimum-distance `Q`, the source-independent acceptance predicate is:

`SHA256(raw16(Q XOR M)) == 930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

The purpose-built read-only C++20/OpenSSL enumerator is [agents/agent30/k04_min14_search.cpp](../agents/agent30/k04_min14_search.cpp), exact Git blob `56a7644f0cbc1603e9ed075dacb41b3de749a3ab`, local source SHA-256 `f2f3e81c38afd50b7d5440bf6b0c9748154b179bb790762779667b5b5e01f527`. Compiled using `g++ -O3 -std=c++20 -pthread ... -lcrypto`, run with five threads against the unaltered original commitments; return code 1 means completed search/no match. Captured complete output:

```
Patterns=1777 exact conditional Q=1665398756
SHA256 checks=1665398756 found=0
```

A separate C++ OpenSSL hash control for the concrete *model-only* nearest witness `Q=B8AB8E1531A5A2AE879ED7A15D2559D5` reproduced Python hashlib's expected `SHA256(Q XOR M)=55fd61aa9d9e93a00162ac2cbf6cf7163093e89e1589aeb5d32940aee05afbef`. Enumeration cardinality independently agrees with Agent 32's dynamic-programming exact count, including Agent 32's five small exhaustive controls. The original source ZIP, acceptance file, routing file, known six-slot candidate and `verify.py` were never modified.

**Information-scale qualification:** 1,665,398,756 strings constitute only approximately `4.89417 × 10^-30` of the unrestricted 128-bit coupon space. This large-looking exhaustive workload has decisive power only *inside* the hypothetical shared-permutation/minimum14 family. Its NO_MATCH cannot be extrapolated to a general unknown original coupon or substitute for source-specific integrity evidence.

## Interpretation, stop decision

Under **all** of the unverified shared-permutation/ACK-copy/transcribed-mask premises, an accepted true intermediate `Q` cannot be exactly 14 bit flips away from `S`. Given the source-model Hamming-weight constraint (hypothetical `Q` weight 66, transcript `S` weight 64), possible distances are even, so such a candidate would need at least **16** changes. This bound is *conditional* and **does not certify a historical 16-bit printer fault or any original coupon bytes**.

The nearest-ACK source observation is not especially diagnostic for this model: Agent 32's matched-weight shuffled-ACK control found 63 of 100 permutations at or below the observed minimum distance. Thus this no-match is a precise finite hypothesis stop rather than evidence for this speculative producer. **Do not escalate to radius 16+ commitment sweeps without an independently observed common-permutation/copy-stage bridge.** No K04 authenticated bits (0/128) and no original K08 final words (0) resulted. Six previously verified slots remain untouched, combined original REC8 acceptance incomplete.
