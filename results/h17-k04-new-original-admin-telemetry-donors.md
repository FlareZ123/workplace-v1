> **PRIOR-ART CORRECTION (19 Oct ~19:04 UTC): This entire experiment reproduces earlier research, and must not be cited as new K04 cracking.** Agent 3 had already tested WN-14 groups and 44 seal serials as fullword inverse-MT donors ([prior SFT](../agents/agent3/k04_wn14_seal_source_donor_sft.py)). Agent 44 had already tested the LT-204 DIAG_WORD high16 three-word streams under a wider 16-ordering family and obtained the same zero matches with an AX-7778 control ([prior report](h17-k04-telemetry-high16-bridge-gate.md)). The five-view K02 test here is a subset of Agent 44's 16-order test. Retain this file solely as an independent replication artifact; do not infer a novel source class, target gain, or exclusion. Agent 8 discovered these overlaps after its first publication.

# K04 new original administrative and telemetry donor classes: no target bridge

**Agent 8, 19 October 2026 ~18:42 UTC, amended after Agent 3 overlap discovered.** This is a *new K02 telemetry source-family cracking test*, restricted to prospective original-source donors for the two hidden K04 MT ancestor intervals. It recovers **zero selected K04 bits** and does not propose a K08 phrase. The existing target-indexed donor cut and original verification state remain unchanged.

## Prior gap and new original inputs

Earlier cross-source K04 inversion searched four-byte TRP2 **control** words, RC-17 footer strips and AX-7778 **two-byte transfer** checkpoints. **Important priority correction:** Agent 3 had already tested the WN-14 signed groups and 44 seal serials with the same inverse-MT bridge method at ~16:48 UTC (see [Agent 3 SFT](../agents/agent3/k04_wn14_seal_source_donor_sft.py) and [message to Agent 8](../communications/agent8/2026-10-19T1648Z_agent3-signed-ink-seal-bridge-null.md)). Those two repeated checks below are replication controls only. The distinct previously untested source hypothesis in this result concerns **LT-204 diagnostic-word ordered three-/four-run precursors**.

1. Four signed WN-14 **ink** control groups, verbatim in original `evidence/mail/03.eml` and `06.eml`: `049AAB2E`, `1CDE7A82`, `CD7C6023`, `4303C91A`. These jointly supply accepted K01 but are tested here only as possible shared-generator MT carriers.
2. Forty-four original `SG-XXXXXXXX` serial fields in `evidence/maintenance/seal-receipts.jsonl`. These include unrelated permits, revisions and unsigned records deliberately kept as *auxiliary observations*, without changing the signed K03 selection.
3. Thirty-two in-range `LT-204/DIAG_WORD` revision records (`seq=0..7`, `revision=1..4`) in `evidence/telemetry/freeze-export.jsonl`, plus the original K02-selected eight values. Original diagnostic values are 16-bit integers. Source orders tested: `(seq,revision)`, `(revision,seq)`, retention-file order, timestamp/UTC order, and the original GOOD/HOLD greatest-revision eight-value selection.

**Historical producer premise:** A common MT stream might have produced some administrative hex identifiers or diagnostic words, even if those fields are not valid K04 inputs. This is an explicitly *conditional* synthetic-generation hypothesis; no custodian evidence says the signed watch register, seal serials or telemetry shared a printer PRNG. A positive result would still require source order and epoch evidence, plus a withheld intact-source prediction before assuming any K04 target placement.

## Target-facing predictions set before testing

The original 132 nonselected complete printer payloads (selected row129 excluded) yield **138,336** ordered interrow pairs of full 32-bit MT state words. For each earlier middle `M` and later end `E`, the exact MT inverse twist `inverse_twist(M XOR E)` exposes a low31-bit hidden predecessor fingerprint. If a new 8-nibble field is a serialized 32-bit output at one such indexed predecessor, little- or big-endian `untemper(field) & 0x7fffffff` must equal this fingerprint. **Stop** if neither orientation matches.

For 16-bit diagnostic fields, ask a *stronger* source-order question: can **three or four consecutive diagnostic values** match three/four consecutive ancestor states inferred from a pair of intact printer payloads? The unknown predecessor top bit gives two possible tempered upper16 values per inferred word. Test both orientations of each *complete* original ordered diagnostic run (numeric display or byte-swapped). A surviving three-run would merit provenance checking; absent one, stop this exact donor-copy branch.

## Original results

| New source family | Original source scope | Result |
|---|---|---|
| K01 WN-14 signed ink groups | 4 distinct 4-byte words × 2 orientations | **0** inverse-MT precursor matches |
| K03 raw seal serials | 44 4-byte fields × 2 orientations | **0** inverse-MT precursor matches |
| K02 LT-204 diagnostic stream | 32 revision values across 4 natural source orders, plus selected 8; all consecutive 3/4-runs, both orientations | **0** three- or four-value ancestor matches |

The original **AX-7778** checkpoint run at source positions 11..14 matches four original inferred ancestor outputs for printer rows34 and64 under checkpoint byte reversal, as previously found by Agent36. This is an independent positive control of the newly implemented 16-bit orientation and inverse-twist method. A separate source-only 32-bit positive check retrieves original CRC-valid TRP2 record28 as the predecessor of printer row10 word0 / row41 word0. The known RC-17 REV B two-footers also reappear when all standalone eight-hex tokens are probed, showing the broader extraction can find genuine existing related words. No positive instance involves the new WN-14, seal or telemetry categories.

**Exact source SHA256**: spool `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`; seal receipts `c00944558636fbcc7e91b81e8e838ffd13fcd5a30d121b41951888766a8a0e32`; LT-204 telemetry `3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f`; transfer records `32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf`.

Locally executed read-only original-ZIP reproducer `agents/agent8/k04_new_donor_carriers_sft.py` provides the explicit candidate tests, original-field assertions and AX-7778 control. The candidate script was tested in the invocation's local standalone runtime; a checked-out remote run is not claimed.

## Cracking implication

Agent 3 already excluded **directly serialized WN-14/serial low31 precursors** in the tested printer inverse pairs. This run independently replicates that bound and newly excludes **three-/four-word sequential LT-204 diagnostic upper16 precursors** in the tested source orders. It does **not** rule out transformed sources, isolated two-halfword matches, other producer epochs, shared MT states without a tested recurrence fingerprint, or newly acquired source records. Crucially, no new independent donor reaches the row43→44 and row96→97 hidden windows. Don't expand these exact negative searches absent a new source/producer mechanism.

Keep the target-facing work concentrated on an independently indexed full-/low31-word donor *inside both* ancestral windows or on independently recovered original ESC-N coupon/mask evidence. The original final K08 caption still has no exact-text witness; this experiment deliberately performs no new free-form caption guessing. **K04 0/128 newly recovered bits; K08 zero new final words.** Six other components remain accepted in the canonical shared state; combined REC8 is still incomplete.
