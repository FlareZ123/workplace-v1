# K04 exact-job retry divergence and evidence value (Agent 13)

**Date:** 18 October 2026. **Result:** the three retained RECOVER attempts for incident-date ESC-N job `PS-261003-0417` disagree at **every one of the 16 corresponding byte positions**. The ACK-selected payload still fails the unchanged K04 commitment. This is a provenance diagnostic, not a recovered component.

## Source boundary

The local `resources/evidence/print/spool-reconstruction.log`, SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`, is a retained-fragment export and explicitly warns that payload integrity is unverified. `resources/evidence/archive-labels.ini` maps incident-date ESC-N to `PS-261003-0417`. `resources/evidence/mail/16.eml` directs selection of its last ACK for the exact job. The table below excludes the same job's earlier LABEL-class ACK because the recovery coupon is RECOVER-class.

| Attempt | State | Retained 16-byte RECOVER payload |
| --- | --- | --- |
| 1 | REQUESTED | `CD3E4F216ADB2FB180DA2AA90B33F7A4` |
| **2** | **ACK** | **`A9A9DC5731A5E2AE879C47215C2559D5`** |
| 3 | REQUESTED | `44D53DFC29D7943A95D89371DA58EC64` |

## Reproducible byte comparison

Compare corresponding bytes from each pair of source records without applying the XOR mask:

| Attempts | Different of 16 bytes | Different of 128 bits |
| --- | ---: | ---: |
| 1 vs 2 | 16 | 68 |
| 1 vs 3 | 16 | 62 |
| 2 vs 3 | 16 | 62 |

There are **zero byte positions with unanimous three-attempt agreement**. The exact retained retries therefore supply no position-wise consensus or majority byte that independently checks attempt 2. The three values could represent separately regenerated coupons, damaged acquisitions or other unrecorded behavior. Their disagreement does **not** demonstrate a particular corruption mechanism or authorize replacing the ACK rule.

With the original XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C`, the selected output remains `2CFF149C50E54557228E7DE60B3EB7C9`, SHA-256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`; original K04 commitment `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0` is **NO_MATCH**.

The method and outputs are reproducible with [the read-only script](check_h17_retry_divergence.py), which pins the original spool SHA-256 and obtains the mask/target from untouched resource files.

## Tight lower bound for a hypothetical shared original

Bitwise comparison gives 32 of 128 positions where all three payloads agree (despite zero *whole-byte* agreement). Pairwise Hamming distances are 68, 62 and 62 bits. For any hypothetical single original 128-bit payload `X`, the triangle inequality requires

`max(d(X,attempt1), d(X,attempt2), d(X,attempt3)) >= ceil(d(attempt1,attempt2)/2) = 34`.

This lower bound is **tight**: per-bit majority voting constructs `CDBD5D7529D7A6BA85D803215A31FDE4`, at Hamming distances **34, 34 and 28** from attempts 1, 2 and 3 respectively. Thus the exact minimum possible maximum deviation from one common 128-bit original is **34 bit positions**. If all three are corrupted recordings of a single unchanged coupon, at least one would need 34 or more bit errors; a model of at most 33 errors per recording is impossible.

The bitwise-majority payload XOR the unchanged mask is `48EB95BE4897014320CA39E60D2A13F8`, which **fails** the original K04 SHA-256 acceptance commitment. This test uses a source-motivated single candidate and is distinct from the accepted attempt-2 rule. Nothing in the record establishes that the attempts were meant to print identical coupon content, so the minimax radius is a **conditional** consistency bound, not an assertion that actual corruption occurred.

## Implications and limitations

This result closes a tempting but unsound assumption: retry records do **not** furnish redundant copies of stable coupon bytes in the retained export. It adds to prior exhaustive retry-mosaic and word-reassembly NO_MATCH results ([evidence audit](h17-evidence-audit.md), [word-reassembly bound](h17-k04-word-reassembly-bound.md)). It cannot rule out a correct original coupon encoded elsewhere or derive its bytes. The explicit ACK rule and integrity caveat remain distinct from the hashed acceptance criterion.

**Disposition:** no change to canonical candidate: K04 and K08 remain null, six slots PASS, and combined acceptance is INCOMPLETE. The current case excludes external contact; a new local independently authenticated source or evidence-backed derivation is needed before claiming a full recovery.
