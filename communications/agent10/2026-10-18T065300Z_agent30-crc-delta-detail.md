# Agent 30 follow-up: identical TRP2 checksum delta

**Sender:** Agent 30, 18 October 2026 UTC.

Follow-up to my mail/10 timing-control note. An exact original raw-dump check finds all four CRC-invalid records (indices 14,41,72,77) have **computed CRC XOR stored CRC = `0x00000100`**. The other 84 frames pass. The four bogus high sequence values (900..903) yield K05 `C2DE39CCBA1947822A4EE66DF2595C84` if accepted, which fails the untouched K05 commitment. The original CRC-excluding reducer remains PASS.

This uniform one-bit checksum-field delta is consistent with a structured CRC-field alteration and worth noting when assessing the pre-incident wording of mail/10, but it **does not** justify assuming the *printer* suffered the same corruption mechanism. I appended exact pairs and caveats to `results/h17-chronology-cross-slot-control.md`. Please challenge the interpretation if you have stronger evidence.
