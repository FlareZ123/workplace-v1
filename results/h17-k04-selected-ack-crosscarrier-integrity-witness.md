# K04: source-corrobated selected ACK words via independent original MT precursors

**Agent 8, 19 October 2026 ~19:01 UTC.** Direct, selected-coupon-facing source test of a *new* independent-witness class. It yields no original K04 bits or accepted key; the recorded ACK remains unauthenticated. [Source-pinned SFT](../agents/agent8/k04_selected_ack_crosscarrier.py) with original ZIP as input.

## Original evidence and pre-hash prediction

- Candidate output: incident ESC-N spool job PS-261003-0417 last ACK attempt 2, original PAYLOAD `A9A9DC5731A5E2AE879C47215C2559D5` at zero-based spool row129. The export explicitly says its media bytes are unverified. The four little-endian untempered 32-bit words are `10D4A0CA F8BD9DBA 7F223290 D54FBDFD`.
- Independent controls: 88 original TRP2 recorder four-byte control fields, in both serializations, and 12 source RC-17 footer strips in both serializations (**200 32-bit source control orientations**). The 132 intact unselected printer rows provide **138,336** earlier/later ordered crossrow word pairs; no disputed row129 byte enters that independent pair index.
- Mechanism: under a shared historical MT19937 output producer and suitable stream spacing, any intact selected word used as predecessor successor `X[k+1]` must have its untempered low31 bits equal to one of the source-only inverse-twist pair fingerprints. Conversely, treating selected word as `X[k+624]` (end) or `X[k+397]` (middle), the inverse twist of it with an intact printer word must match the low31 bits of an independent TRP2 or RC-17 control. These are three separate source-corrobation roles. They potentially constrain or falsify complete selected **words**, with the original acceptance SHA completely withheld.
- Prediction/exit specified before reading acceptance: one exact 31-bit cross-witness is worth independent producer/index scrutiny; zero means stop this direct-copy recurrence family. This test is more generous than source chronology because it allows every earlier/later intact printer pair, both orientations of auxiliary four-byte controls, and their unvalidated producer clocks.

## Results

| Selected-ACK role | Original source geometry | Exact matches |
|---|---|---:|
| `X[k+1].low31` donor for two intact printer words | 4 selected untempered words × all 138,336 printer pair fingerprints | **0** |
| `X[k+624]` end with older intact printer middle | 4 selected end words × 129 earlier printer rows × 200 independently carried controls | **0** |
| `X[k+397]` middle with later intact printer end | 4 selected middle words × printer rows130..132 × 200 independently carried controls | **0** |

The original CRC-valid **TRP2 record28** still matches exactly the corresponding held-out *intact* row10 word0 → row41 word0 inverse-twist fingerprint, verifying the source-control orientation, untempering and inverse transform on a real original positive example. The method-equivalent program executed against the untouched original 43-member ZIP yielded exactly these empty original target matches and the positive control. A new historical interpretation that transforms words or supplies extra indexed donors would be outside the tested class.

## Boundary

This tests the actual **recorded ACK**, which may be corrupted; a failure to match does **not** disprove a shared printer MT producer or exclude the unknown genuine selected coupon from another source. It also does not authenticate the selected bytes, provide a repair recipe, or directly limit all output generator/position possibilities. Crucially, no independent target-side ancestor window is newly indexed. The original K04 mask, K04 commitment, K08 nonce, and original verifier are unused. **K04 newly recovered bits 0; K08 exact words 0; six other slots unchanged; complete REC8 not accepted.**

Do not repeat this fingerprint search without independently source-backed output reordering, serial transformation, generator epoch, or a new original witness. For reconstructing the authentic selected bytes, the higher-leverage [paired hidden-window algebra](h17-k04-target-leverage-constellations.md) still demands genuinely indexed observations on *both* missing MT ancestor runs; an original ESC-N coupon or exact uncorrupted mask witness would bypass the model.
