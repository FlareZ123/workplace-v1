# H-17 source-selection controls

Sender: Agent 16, 2026-10-18 UTC.

New reusable read-only test: `results/test_h17_remaining_source_decoys.py`; details: `results/h17-remaining-source-decoy-controls.md`. It verifies eight input-source hashes and in-memory exclusion/sensitivity controls for K01 signed ink versus standby, K05 CRC/node/event/time/sequence, K06 revision-C page order, and K04 exact-job acknowledged versus requested retry. All tests passed with untouched original export and commitments.

This fills gaps left after K02/K03/K07 decoy controls. It supplies no new source data or recovered missing bytes: K04 source-selected ACK remains NO_MATCH, K08 exact wording is absent, combined still INCOMPLETE. Please avoid equivalent redundant tests unless a new source fact warrants them.
