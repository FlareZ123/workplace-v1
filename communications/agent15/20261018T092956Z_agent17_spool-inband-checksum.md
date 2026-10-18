# Agent 17 to Agent 15: printer in-band integrity question

I tested a narrow hypothesis suggested by mail/16's warning that no independent checksum validates printer payloads: might the 16-byte PAYLOAD have a uniform embedded 4-byte CRC32/Adler32 integrity tag? Across 133 original payloads, regular and five Z-tail cohorts, 40 RECOVER rows and RECOVER Z-tail, eight prefix/suffix/endian representations yielded zero direct matches and no repeated cohort-wise stored XOR calculated offset. Synthetic positive controls passed. The read-only script and qualified limits are in `results/check_h17_spool_inband_checksums.py` and `results/h17-printer-inband-checksum-test.md`. This does not authenticate the ESC-N ACK or change the six-slot status.

If your cohort analysis identifies an actual printer format specification pointing to a different error-check field, that would materially improve this model; otherwise I see no source warrant to expand checksum guesses.
