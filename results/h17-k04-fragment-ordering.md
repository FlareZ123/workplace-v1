# H-17 K04: bounded variable-fragment ordering audit (Agent 9)

**Date:** 17 October 2026. **Result:** **5,421,480 candidate assignments** from a defined two- to five-fragment ordering/orientation hypothesis all fail the original K04 commitment. K04 and K08 remain unverified.

## Source and hypothesis

The incident-date `ESC-N` route in `resources/evidence/archive-labels.ini` resolves to `PS-261003-0417`. The last ACK `CLASS=RECOVER` attempt 2 in `resources/evidence/print/spool-reconstruction.log` holds `A9A9DC5731A5E2AE879C47215C2559D5`. The untouched `resources/evidence/recovery-routing.json` mask `8556C8CB6140A7F9A5123AC7571BEE1C` produces baseline XOR component `2CFF149C50E54557228E7DE60B3EB7C9`, which fails the original `resources/acceptance.json` SHA-256 value for K04.

The print record is a **retained-fragment reconstruction** whose payload bytes lack an independent integrity checksum. An ordering error during concatenation of variable-length contiguous fragments is a plausible *hypothesis* worth an exact finite test; no source independently establishes that this error actually occurred.

For each fragment count `s` from 2 to 5, enumerate every selection of `s-1` cut boundaries among the 15 inter-byte positions. For every partition into `s` contiguous nonempty byte fragments, enumerate every permutation of those fragments and every subset of fragments to reverse bytewise. Concatenate the resulting fragments, XOR the resulting 16 bytes with the original mask, hash the candidate component with SHA-256, and compare to the unmodified K04 acceptance digest. No extra padding, guessing bytes, rerouting of job IDs, or changes to evidence are permitted.

## Exact tested classes

| Number of fragments | Assignment count `C(15,s-1) × s! × 2^s` | Unchanged commitment |
| --- | ---: | --- |
| 2 | 120 | NO_MATCH |
| 3 | 5,040 | NO_MATCH |
| 4 | 174,720 | NO_MATCH |
| 5 | 5,241,600 | NO_MATCH |
| **Total** | **5,421,480** | **NO_MATCH** |

Counts refer to assignments; multiple permutations and cuts can yield identical 16-byte payloads. No claim about a unique-candidate count is made.

## Reproducibility and controls

Read-only standard-library [`check_h17_fragment_permutations.py`](check_h17_fragment_permutations.py) uses source selection from [`check_h17_bit_slips.py`](check_h17_bit_slips.py). From repository root, run `python results/check_h17_fragment_permutations.py resources 2 4` and separately `python results/check_h17_fragment_permutations.py resources 5 5` for bounded execution. Positive control constructs a known three-part reordered and reversed candidate using cuts after bytes 5 and 11, independently hashes its masked output, and confirms the enumeration finds a match to that synthetic digest. Counts are asserted analytically for each fragment size.

Local tested source SHA-256: `1a70a62c5a05ac3095bcc0e6eac99b065cb8adfb1d7d56290887fe04d634368e`. This report treats the untouched original `acceptance.json` as authoritative for the actual result.

## Interpretation

The result rejects **only** permutations of two through five intact variable-length fragments with optional byte reversal within each fragment. It does not recover an authenticated spool payload and does not exclude six or more fragments, altered fragment bytes, missing media, corruption unrelated to ordering, or a different original coupon. Agent 3's previous permutations of fixed four-byte words overlap a subset of the enumerated cases. The acceptance mismatch and lack of independent payload-integrity evidence remain.

Do not promote the invalid XOR baseline to K04. Without independent integrity-checked coupon/media and an authenticated exact K08 final keeper caption, the combined eight-part REC8 recovery remains incomplete.
