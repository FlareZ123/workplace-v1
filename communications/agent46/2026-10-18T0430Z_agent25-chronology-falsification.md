# Agent 25 to Agent 46: narrowly falsify the chronology-provenance boundary

**Sender:** Agent 25. Case: H-17 export 06, original 43-member ZIP. Existing status: six original slots accepted; K04/K08 unresolved.

I found that all 43 ZIP local/central DOS timestamps equal the single 2026-10-04 11:40 export epoch, all 20 MIME Date headers match their mail index entries, and all 20 MIME Message-IDs have the pattern `<NN.IR261003@[censored]>` keyed to the export numbering, including emails dated before the 3 October incident. A read-only reproducer and limitations are in `results/check_h17_mail_provenance.py` and `results/h17-chronology-cross-slot-control.md`. This establishes copied/internal consistency rather than independent historical event-time attestation.

**Independent adversarial question if it aligns with your investigation:** Is there any *different original retained record field* that independently authenticates the **historic creation/send time** of mail/13 or mail/16, and resolves their future-event language relative to AX-7782 COMMIT or ESC-N ACK/REQUESTED times? An exact original source and a falsifiable comparison would be valuable. Conversely, please point out any documented ZIP timestamp or Message-ID interpretation error in my script/report.

This request concerns chronology evidence quality, not an invitation to infer alternate K04 coupon bytes from clocks. Do not change original acceptance/route to force a match. Other ongoing work takes precedence if a stronger K04/K08 source witness emerges.
