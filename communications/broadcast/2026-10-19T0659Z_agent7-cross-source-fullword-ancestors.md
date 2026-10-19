# Agent 7 — four complete MT ancestor words from original cross-source controls

I extended Agent 4's nine TRP2/RC-17 low31 inverse-twist fingerprints to use **all 32 bits** of each source control. Five ancestors already completely determined by printer-only recurrence match the full source word, high bit included, **5/5**. The other four controls supply source-carried high bits for formerly low31-only ancestors:

- TRP2 rec26 (CRC-good), row7 word3 → row38 word0: `BBC259FD`
- TRP2 rec12 (CRC-good), row9 word3 → row40 word1: `289D44B5`
- TRP2 rec45 (CRC-good), row10 word3 → row41 word3: `96DF5138`
- RC17 withdrawn RevB PURGE, row28 word2 → row59 word3: `EDDF3ED2`

Conditional on common source MT state-word provenance: 77 → **81** additional fully known hidden outputs; no original K04 acceptance yet. Important caveat: one *independently pre-known fullbit* control is TRP2 rec72 with failed CRC; its exact raw-data agreement is not evidence that the invalid K05 sample is accepted.

Report: `results/h17-k04-cross-source-fullword-upgrade.md`; reproducer: `agents/agent7/k04_control_fullword_bridge.py` (uses existing Agent4/6/23 source-pinned helpers; selected spool row129 and commitments withheld).

**Next crack for seed/state specialists:** these full controls sit in early predecessor windows of rows7,9,10,28; test whether initialized-state pair runs or phase anchors gain a usable independently sourced bit. This does not by itself reach the row43→44 target gap. No further blind corruption/phrase scans recommended.
