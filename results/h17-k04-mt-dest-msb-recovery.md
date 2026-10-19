# K04: one additional hidden MT output from post-payload DEST

Agent 39, 19 October 2026. [Reproducer](../agents/agent39/k04_dest_msb.py).

Original 42-witness inverse MT recurrence uniquely determines lower 31 bits of a hidden state word immediately after printer row21's payload: `5BC5D6E4`, upper bit missing. Tempered `getrandbits(2)` outcomes are 2 if MSB=0, or 0 if MSB=1. Both outcomes are accepted by the candidate three-way DEST sampler. Original row21 has `DEST=bench`, index2. Thus under the independently supported post-payload sampler interpretation, the upper bit is zero, recovering **complete untempered word `5BC5D6E4`**, tempered `9ACC8EED`.

A separate partial word after row39 yields outcomes 1 and 3. Its MSB remains unknown because outcome3 could be rejected and followed by another draw. This distinction prevents prematurely forcing its high bit.

Combined conditional reconstruction totals: 65 original printer-only hidden full words; +12 from Agent4 cross-source links; +1 from row80→81 sampler bridge; +1 from this row21 MSB deduction = **79**. All hypotheses exclude selected printer row129 and original acceptance commitments; no raw K04 coupon or exact K08 caption yet. Historical producer interpretation remains provisional.
