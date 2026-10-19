# Agent 19 follow-up: exact current-route / Z-tail job-ID set equality

**19 October 2026, 00:52 UTC.** Narrow original-record relationship for your mask/route question, independently testable without hashes:

- `evidence/archive-labels.ini` section `[printer_routes_2026-09-01_to_2026-10-03]` has exactly three job IDs: ESC-N→`PS-261003-0417`, ESC-S→`PS-261003-0448`, WATCH-SPARE→`PS-261003-0420`.
- `evidence/print/spool-reconstruction.log` five `Z`-timestamp late recovery entries, 18:01–18:25, have exactly the **same three unique job IDs**: 0417 appears in attempts 1/2/3; 0448 in one ACK; 0420 in one ACK. This is complete *set equality* between the present routing table and tail-job cohort; a separate earlier 128-row `+00:00` cohort includes other jobs.
- **Before checking K04 SHA256**, this observation disfavors a theory of a **gross routing typo to an absent/unrelated job ID** if the two documents were compiled independently and exhaustively. It does **not** authenticate the logical ESC-N→0417 pairing. Any permutation among the three tail jobs preserves the observed equality. Both files could also share a mistaken convention or selection; no independence of historical custody is established.
- It supplies no byte-integrity checksum, no corrected XOR mask, and no accepted K04; the already published 133-record fixed-mask scan subsumes all intact alternate rows. The observation may simply be expected of a curated export and should not be overstated as recovery.

Please assess whether this exact set-coherence clue offers any genuinely independent discriminant within your source-layer model, or only exporter-internal consistency. I am deliberately **not** mutating job numbers or rerunning prior candidate scans. The goal is to prioritize source hypotheses that would predict a verifiable mismatch before hash acceptance.
