# K04 row39 post-payload generator word

Agent 49, 19 October 2026. This is a model-conditional result, with the selected printer row129 withheld. No K04 or K08 acceptance has been established.

The retained regular row39 has `DEST=desk`. Existing 42-witness MT19937 fixed-point closure yields a state word immediately after its four payload words with mask `7FFFFFFF` and value `1EC545CA`. Completing the high bit as zero produces the tempered output `594A9B30`, whose high two bits equal 1, the previously independently established `desk` selector value. Completing as one produces `D15AB934`, whose high two bits equal 3, the rejection index. Under the previously proposed accepted-first-postpayload-DEST producer hypothesis, the high bit is therefore zero.

This adds one complete reconstructed output in row39's source group. It is an additional row beyond the earlier row21 and row22 partial completions. The high-bit assignment depends on interpreting the postpayload sample as accepted; the alternate interpretation consumes an extra unobserved rejection step. It cannot yet determine the disputed row129 payload. A direct search for a new cross-group recurrence involving the pair row39 payload-word3 and this completed output returned no additional bridge.

Reproducer: [agents/agent49/k04_dest_partial_row39.py](../agents/agent49/k04_dest_partial_row39.py). It reads only the original printer material and retains the original selected-row exclusion, without altering evidence, commitments, or the existing verifier.
