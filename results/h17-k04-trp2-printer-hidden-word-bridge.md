# K04: six cross-source TRP2-to-printer MT19937 hidden-word matches

**Agent 2, 19 October 2026 ~06:19 UTC. Constructive source relationship; K04/K08 remain unresolved.** Reproducer: [agents/agent2/k04_trp_printer_bridge.py](../agents/agent2/k04_trp_printer_bridge.py). Uses solely original ZIP `evidence/recorder/trip-recorder.raw` (SHA256 `5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba`) and `evidence/print/spool-reconstruction.log` (SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`); excludes printer selected ACK row129 and never reads the acceptance inventory or the K04 mask.

## New search class and observations

The original [TRP2 format note](../resources/evidence/recorder/format-note.txt) identifies four opaque control bytes at offset12 of 24-byte records; the [route sheet](../resources/evidence/recovery-routing.json) identifies the relevant archive latch as node0x31, event0x52. Decode its 16 candidate records as little-endian MT19937 outputs and untemper. Independently, untemper every 32-bit little-endian printer output except the selected row129. For each ordered pair of printer output words belonging to different intact rows, compute the exact inverse twist of the words' XOR:

`z=untemper(printer_later) XOR untemper(printer_earlier)`

`mixed=inverse_twist(z)`

Its low31 bits must be the low31 bits of a hidden MT stream output `X[k+1]` **if** those two printer words occupy index positions `k+397` and `k+624` in one PRNG stream. Compare that 31-bit fingerprint with the 16 untempered archive-latch control words. This search is source-only, and its probabilistic interpretation is conditional on a common-stream model.

| Recorder index | Sequence | Latch | Printer middle | Printer end | Control word (untempered) | CRC |
|---:|---:|---:|---|---|---|---|
| 40 | 990 | 0 | row9 word2 | row40 word0 | 7168DD87 | valid |
| 12 | 201 | 1 | row9 word3 | row40 word1 | 289D44B5 | valid |
| 28 | 992 | 2 | row10 word0 | row41 word0 | 348ADB23 | valid |
| 17 | 203 | 3 | row10 word1 | row41 word1 | 324EF3E1 | valid |
| 72 | 903 | 3 | row10 word2 | row41 word2 | 353CCDFC | **bad CRC** |
| 45 | 993 | 3 | row10 word3 | row41 word3 | 96DF5138 | valid |

**All six match the inferred low31 bits exactly. Five have valid original per-record CRC32; row72 is a damaged retry and must remain excluded from accepted K05 reconstruction.** Four of the six also match the derived mixed word in all 32 bits. The unconstrained highest bit of the other two is not an integrity failure: MT inverse twist does not constrain the top bit of `X[k+1]`. Importantly, the experiment searches the 16 original node0x31/event0x52 records, not all 88 arbitrary recorder words.

Across 528 surviving non-selected printer words, 138,336 earlier/later inter-record word pairs are eligible. A *naive independent-uniform 31-bit null* would expect 16 × 138,336 / 2^31 ≈ **0.00103 matches**, compared with six observed. This is an exploratory magnitude comparison, **not a calibrated probability of a shared physical RNG**: both sources may have common synthetic generation provenance, and the recurrence-based search was proposed after the MT lead was known. The striking two-pair/four-pair structure is an observed constraint.

## Relation to existing printer inversion

The four row10→row41 matches correspond, under the already independently discovered 42 printer MT recurrence witnesses, to **four consecutive missing state positions** -623, -622, -621, -620 in the group whose row41 start is position0. Earlier source-only printer reconstruction fully determined the first three as `348ADB23`, `324EF3E1`, `353CCDFC`; original TRP2 controls at indices28,17,72 exactly agree, including the corrupted CRC row72. The fourth position was previously known only in its low31 bits, `16DF5138`, matching recorder index45's `96DF5138` in those bits. The CRC-valid recorder bytes could supply a proposed extra high bit at the fourth position under an explicit same-stream interpretation; this interpretation requires its own independent prediction before promotion.

The two row9→row40 matches impose the **new conditional alignment `s40-s9=229`** if these pairs arise from actual MT recurrence positions. Two consecutive printers match this identical alignment, whereas rows9 and40 were disconnected in the earlier printer-only 42-witness graph. Adding the equality merges those two groups and produces one additional reconstructed complete hidden word. Under the existing two-selector ordinary transition floors, the equality is feasible, but the selected row129 first-output window remains `s129-s0=945..955`; the bridge does not itself recover any indispensable K04 row43→44 gap word.

## Limits and targeted next attack

The original TRP2 format defines opaque control bytes, and it does **not** say they were produced by the printer's MT generator. The recurrence identities therefore establish unusual cross-source mathematical correspondence, not a proven shared historical RNG. Exact 32-bit matching is stronger than 31-bit fingerprinting where separately reconstructed printer state already exists, but the partial-word matches and one bad-CRC record must be treated carefully.

Next investigation: search a coherent source-index alignment for **other CRC-valid archive-latch controls**, with each hypothesized control index independently constrained by printer recurrence and sample metadata. Seek reconstruction of at least one missing source word in the **row43→44 hidden interval** or a predictive intact-tail output. Arbitrarily imposing a common stream on all 16 controls is unsupported by the present evidence. Any candidate K04 must pass the original untouched commitment; K08 is still missing, and no combined key is accepted.

No original case file, acceptance commitment or verifier has been modified.
