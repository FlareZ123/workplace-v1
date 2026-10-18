# Remaining H-17 source-selection decoy controls

**Agent 16, 18 October 2026.** Scope: read-only tests against the untouched 43-member export 06, specifically the K01, K04, K05 and K06 selection paths left out of the earlier K02/K03/K07 decoy-resilience suite.

## Method and input controls

The standalone standard-library test uses an extracted original export (or the repository `resources/`). Before testing, it verifies SHA-256 of eight input files: mail/03, mail/06, mail/14, trip-recorder.raw, RC-17-scans.txt, spool-reconstruction.log, archive-labels.ini and recovery-routing.json. All source mutations exist only as in-memory strings and byte arrays. None are saved to the preservation export.

The baseline reducers read their original field discriminators and original acceptance commitments. Each test has an exclusion control (ignored decoy) and sensitivity control (change that should affect candidate selection or its authenticated bytes). No synthetic value is treated as original recovered evidence.

## Observed execution

- K01: The explicit standby register decoy leaves signed ink A,B,C,D unchanged. Editing signed ink B changes the component and the original slot check rejects it.
- K05: An added high-sequence CRC-invalid record, high-sequence wrong node, high-sequence wrong event and high-sequence record at the exclusive UTC endpoint each leave the authentic component unchanged. An added *CRC-valid*, in-window, correctly identified higher-sequence record for latch zero changes selection and is rejected by the original slot hash.
- K06: Reversing form-feed-separated scanner page blocks leaves revision C's SERVICE_ORDER component unchanged. Altering the approved DRAIN control-strip byte changes K06 and fails the original slot check.
- K04: An added newer REQUESTED retry and an unrelated job's ACK do not displace PS-261003-0417's last acknowledged RECOVER attempt 2. An added later exact-job RECOVER ACK changes the selected candidate as required. Neither authenticates source bytes; the actual recorded ACK still fails the unchanged K04 commitment.

Local stdout: eight input file digests PASS; all four control groups PASS. No test promotes K04/K08 or changes original sources. Canonical outcome stays 6 PASS, K04/K08 missing, combined incomplete, accepted false.

The test's scope concerns *selection correctness under specifically defined synthetic perturbations*. It cannot prove original printer payload integrity, invent the unquoted keeper caption, or recover the eight-component key. Refer to `results/README.md` for the stronger multi-agent source-status synthesis.
