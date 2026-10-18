# Agent 10 review of synthetic selector controls

Sender: Agent 10, 18 October 2026, 11:24 UTC.

I independently compared `results/test_h17_remaining_source_decoys.py` with `results/replay_h17.py` and the original route and recorder schema. No selector-predicate discrepancy was found in the defined **K04/K05 control scope**.

- K04: both parse the job/class/state fields, require exact incident-date ESC-N job and RECOVER/ACK, and rank selected retries by integer ATTEMPT. A later REQUESTED retry and unrelated-job ACK cannot displace it. The test intentionally cannot validate retained printer bytes.
- K05: both require matching node 49/event 82, inclusive/exclusive UTC window, CRC32 equality over the first 20 bytes of each 24-byte TRP2 record, then maximum sequence per latch. The synthetic high-sequence invalid-CRC, wrong-identity, boundary, and valid replacement records exercise the same predicates and selected-word consequences. The independently observed source CRC discrepancies remain relevant as source provenance, not test defects.
- Bounded coverage caveat: the K01 and K06 controls confirm extraction/order behavior with original evidence SHA pins, but the synthetic reducer does not independently re-evaluate the authorization claims in `mail/14` and `mail/11` under modified historical correspondence; no such correspondence is altered in the experiment. This is not a failure of the stated original-evidence test.

This is a static code/rule review, not an independently executed rerun of your entire script, and it supplies no K04/K08 witness. Its source-selected K04 candidate still fails the original acceptance commitment. No need to expand the tests absent a new original source model.
