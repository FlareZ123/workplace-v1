# H-17 chronology comparison: accepted K07 and unresolved K04

**Agent 10, 18 October 2026.** The timestamp anomalies already reported in the source-rule consistency certificate can be interpreted using K07 as a control.

Gabriel's mail/13 header is dated 2026-10-02 09:56 UTC and describes AX-7782 as the final handoff. The transfer-audit COMMIT for AX-7782 is stamped 2026-10-03 20:55:10 UTC, a difference of 1 day, 10 hours, 59 minutes and 10 seconds. The source-selected K07 checkpoint chain nevertheless passes its original 16-byte slot commitment.

Simon's mail/16 header is dated 2026-10-03 07:49 UTC and describes a later printer request. The related spool records are stamped 18:02 UTC (RECOVER ACK) and 18:03 UTC (RECOVER REQUESTED), 10 hours 13 and 14 minutes after that header. The selected K04 ACK reconstruction fails its original commitment.

A retrospective-sounding early mail date therefore occurs with both an accepted technical reduction (K07) and a rejected one (K04). Chronology anomalies alone neither justify choosing a different K04 printer route nor authenticate a particular repair. The K07 hash acceptance confirms the derived bytes under the recorded rule, without proving the historical timing of the mail. Both observations warrant source provenance caution.

Sources: resources/evidence/mail/13.eml, mail/16.eml, transfers/transfer-audit.jsonl, print/spool-reconstruction.log, recovery-routing.json and acceptance.json. Existing original-case source replay: results/replay_h17.py. Status unchanged: six PASS; K04 and K08 unresolved.
