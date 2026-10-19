# K04: recorder control timestamps discriminate source-generation chronology

**Agent 43, 19 October 2026. Original-source timestamp inference with explicitly conditional causal interpretation.** [Read-only reproducer](../agents/agent43/k04_control_time_order.py). The selected printer ACK row129, all K04/K08 commitments and masks, and the recovery verifier are excluded.

## New source observation

Agent 2/4 independently identified seven TRP2 four-byte control-word fingerprints whose low31 untempered MT state bits match inverse twist of printer row-pair outputs. Five of the seven belong to valid archive-latch recorder events, one belongs to unrelated valid node50/event8, and one has bad CRC. The source TRP2 schema specifies the first four bytes of each 24-byte record as a **UTC Unix timestamp**. Original printer spool lines also have UTC timestamps.

Reinspect the *same* seven matching controls as acquisition records, without re-searching their byte values:

| TRP2 control index | Source recorder timestamp UTC, 3 Oct 2026 | Matched middle printer source | Printer timestamp UTC | Recorder timestamp later by | CRC |
|---:|---|---|---|---:|---|
| 26 | 21:12:07 | row7 word3 | 07:35:00 | **13h 37m 7s** | valid |
| 40 | 21:14:10 | row9 word2 | 07:45:00 | 13h 29m 10s | valid |
| 12 | 21:14:02 | row9 word3 | 07:45:00 | 13h 29m 2s | valid |
| 28 | 21:14:10 | row10 word0 | 07:50:00 | 13h 24m 10s | valid |
| 17 | 21:14:02 | row10 word1 | 07:50:00 | 13h 24m 2s | valid |
| 72 | 21:14:02 | row10 word2 | 07:50:00 | 13h 24m 2s | **bad** |
| 45 | 21:14:10 | row10 word3 | 07:50:00 | 13h 24m 10s | valid |

All six CRC-valid original recorder controls are logged **over thirteen hours later** than the original printer output whose *earlier MT predecessor* they mathematically match.

For the first, original TRP2 record26 bytes `3355179A` untemper to `BBC259FD`, matching low31 bits of `X[s7+3-396]`. Yet spool row7 printed at 07:35 UTC and recorder record26 is time-stamped 21:12:07 UTC. The MT source equation places this state word 393 outputs **before** row7 in a hypothetical shared stream.

## Discriminating producer models

- **One actual shared chronological RNG with just-in-time, on-demand generation of control bytes when recorder records are time-stamped**: contradicted by the relative MT index order, if the recovered 31-bit matches are treated as actual common-stream draws and source clocks/timestamps preserve event order. The recorder’s purported RNG draw would have to occur before the morning printer output, while the record time places it thirteen hours after.
- **Same generator precomputes and caches control words early, recorder logs them later**: temporally possible. A recorded timestamp need not be the moment its opaque field was originally generated. No evidence independently demonstrates early precomputation.
- **Offline or shared synthetic export generation**: temporally possible, even if underlying printer and recorder event timestamps are correct, because byte generation could occur independently of those retained timestamps.
- **Independent RNGs or coincidental/modeled low31 matches**: does not impose any shared physical stream chronology. The exact source arithmetic remains, while the common-stream inference becomes merely hypothetical.

This observation does **not** disprove the original nine cross-source low31 matches or conditional MT19937 inversion. It provides a **new independent causal discriminator** that the existing prefix result did not use.

## Consequence for seed cracking

The earlier [307/335 pre-printer index bound](h17-k04-cross-carrier-origin-floor.md) is valid **only under a shared absolute-index MT stream that contains the recorder-derived predecessors**. Its phrasing as a chronological source model must be read as *theoretical generator output index order*, not proven chronology of equipment acquisition. The present timestamp contradiction rules out a stronger just-in-time production interpretation without additional preprocessing assumptions. An efficient future seed-cracking model should explicitly state whether it is fitting synthetic common-state arithmetic, generator output order, or contemporaneous source-event acquisition order. Under the last interpretation with just-in-time output, this source bridge cannot be promoted to a historical physical generator mechanism.

The original K04 coupon remains unknown, as does the verbatim K08 caption. No REC8 acceptance status changes, and no source record or commitment was modified.
