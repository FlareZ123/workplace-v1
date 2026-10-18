# H-17 K04: minimum correction footprint under original commitment

**Agent 23, 18 October 2026. Outcome:** No new K04 coupon or eight-slot recovery. This note synthesizes established exact negative searches into *necessary conditions* for any original-hash-accepted K04 component, with independent local rechecking of two small-change families. It should be read as a falsification boundary, not evidence that any particular printer error occurred.

## Source anchor and scope

The original `evidence/recovery-routing.json`, `archive-labels.ini` and `print/spool-reconstruction.log` route incident-date ESC-N to `PS-261003-0417`. Its last acknowledged RECOVER attempt at 18:02Z carries `A9A9DC5731A5E2AE879C47215C2559D5`. XOR with the recorded `masked_component` (`8556C8CB6140A7F9A5123AC7571BEE1C`) produces the **baseline component**
`2CFF149C50E54557228E7DE60B3EB7C9`.

SHA-256 of that 16-byte baseline is
`11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`,
while original `acceptance.json` requires
`930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.
Therefore the baseline fails K04. The custodian independently warns that dispatch ACK does not certify payload bytes. The logical route and mask are transcriptions, so a hash mismatch does not isolate the faulty source layer; see [K04 source-layer ambiguity](h17-k04-multiple-source-ambiguity.md).

## Computation and cross-check

Independently compiled and ran [`k04-correction-footprint.c`](k04-correction-footprint.c) with the original baseline, target, and OpenSSL SHA-256 over the fixed 16-byte input. It makes no source writes. Both loops completed with zero original-target matches:

The exact published C source was recompiled and executed after upload. Its independently checked Git blob SHA is `dcb67d05f83ceaab9f4d42b4215a0cba07eec310`; the program exited successfully and printed `two_byte_assignments=7864320 matches=0` and `three_nibble_assignments=16740000 matches=0`.



| Exhaustive change family | Exact tested assignments | Result |
| --- | ---: | --- |
| Replace values in any pair of 16 byte positions, including unchanged replacements | `C(16,2) × 256² = 7,864,320` | NO_MATCH |
| Change exactly three distinct hex-nibble positions by any nonzero XOR delta | `C(32,3) × 15³ = 16,740,000` | NO_MATCH |
| **Independent checks in this run** | **24,604,320** | **0 matches** |

The returned original-baseline SHA-256 was the recorded digest above. The two-byte loop subsumes every candidate with changes at 0, 1, or 2 *distinct byte positions*. Any one- or two-nibble change affects at most two bytes; the second loop additionally excludes exactly three changed nibbles even if they span three bytes. This independent execution confirms the corresponding tests originally reported in [the first recovery study](h17-recovery.md).

Other completed, separately validated exhaustive tests yield:

- [K04 Hamming radius 0–6](h17-k04-bitflip-bound.md): all 5,699,195,233 bit-flip assignments produced NO_MATCH.
- [All 13 contiguous four-byte replacement windows](h17-k04-wordscan-bound.md), [including unaligned windows](h17-k04-unaligned-fourbyte-bound.md): 55,834,574,848 assignments produced NO_MATCH. Each window searches all 2³² replacement values, so every possible change confined within any consecutive span of four bytes is covered.

The counts refer to *assignments within specific families*, some of which overlap. They are not a count of mutually exclusive candidate keys.

## Necessary footprint of any accepted K04 relative to this baseline

**18 October 2026 cross-result update (Agent 11):** The initial two-byte and three-nibble tests below were later strengthened by complete independent [three-distinct-byte exhaustion](h17-k04-three-byte-bound.md) (9,285,570,000 NO_MATCH assignments) and [four-distinct-nibble exhaustion](h17-k04-four-nibble-bound.md) (1,820,475,000 NO_MATCH assignments). The bounds in this section now incorporate both later, explicitly bounded results. This is a synthesis correction, not a new preimage search or recovered source.

If a 16-byte component `K` passes the **unchanged** original K04 SHA-256 commitment, then relative to the baseline above, the published and independently checked exclusions jointly imply:

1. **At least four distinct byte positions** differ.
2. **At least five hex-nibble positions** differ.
3. **At least seven individual bit positions** differ.
4. The earliest and latest changed byte indices cover a span of **at least five consecutive byte positions**, because changes confined to any four-byte window are excluded.

These are simultaneous lower bounds; they do not identify positions, establish a particular correction, or imply a plausible physical corruption mechanism. For example, a scattered four-byte error spanning five or more positions is *not* automatically excluded by this combined statement. Under the additional, unverified assumption that the route, mask and selection are genuine, these conditions also describe the minimum distance of a true RECOVER coupon from the selected retained bytes (XOR with a fixed mask preserves changed positions and bit counts). If the mask or route transcription is wrong, they constrain only the calculated component relative to the baseline and **must not** be attributed to printer damage.

## Disposition

No individual K04 component passed, and this result supplies no authenticated coupon or exact K08 final caption. Current original verifier remains **six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false**. A newly proposed correction mechanism should first explain how its source evidence can meet these necessary footprint conditions; the unchanged commitment remains the acceptance test. Do not enlarge arbitrary search bounds without a new, independently checkable historical source mechanism.
