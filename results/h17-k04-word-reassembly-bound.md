# K04 ESC-N source-word reassembly diagnostic (Agent 10)

**Date:** 17 October 2026. **Conclusion:** the recorded K04 commitment does not match any of **331,776** tested assignments in a defined 32-bit word-reassembly hypothesis. The envelope remains incomplete; this is a bounded negative test, not evidence that the original source can be reconstructed from the truncated export.

## Source and hypothesis

The original `resources/evidence/print/spool-reconstruction.log` (SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`) preserves three 16-byte `CLASS=RECOVER` payloads for the exact incident-date ESC-N job `PS-261003-0417`: attempts 1/REQUESTED, 2/ACK, and 3/REQUESTED. The separate `CLASS=LABEL` entry is excluded. Under the route sheet's XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C`, the last-ACK candidate is `2CFF149C50E54557228E7DE60B3EB7C9`; its SHA-256 differs from the K04 acceptance digest `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.

A possible, explicitly **unproven**, buffer-extraction error is **32-bit fragment reordering or byte-endian reversal**. The test divides each of those three source payloads into four aligned four-byte pieces, yielding twelve source pieces. Each source piece is also available byte-reversed, giving 24 distinct choices. For each of the four output positions, choose any one of these 24 pieces. Reuse is allowed, so the search contains all `24^4 = 331,776` assignments, including reordered original/ACK/requested fragments and independent endian reversals. XOR every reconstructed payload with the unchanged mask and SHA-256 check the resulting 16-byte component against the unchanged K04 slot commitment.

This is distinct from the earlier 43,046,721 **same-position byte mosaics**, which could not take a chunk from a different offset. It is also distinct from the exhaustive **single** aligned-word substitution: the present test can move/replace all four words simultaneously, subject to selecting them from the observed source words.

## Verification

The local exhaustive loop tested **331,776 assignments**, with **zero commitment matches**. Source: [`check_h17_k04_word_reassembly.py`](check_h17_k04_word_reassembly.py), using only the Python standard library, with the spool's fixed SHA-256, original acceptance inventory, and route sheet. The source includes a positive-control target synthesized from allowed input chunks; its full enumeration must encounter the control. It does not modify evidence.

This excludes precisely the defined source-word recombination class. It does **not** establish any particular printer failure mechanism, authenticate unacknowledged attempts, test arbitrary corrupted bytes, or recover the missing coupon. Continue to require independently verified original coupon/media for K04. Keep K04 and K08 null and the combined recovery result **INCOMPLETE** until each authentic slot passes its original commitment.
