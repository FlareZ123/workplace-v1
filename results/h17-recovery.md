# H-17 incident archive: reproducible recovery status

**Case:** IR-261003-H17, export 06 (4 October 2026). **Researcher:** Agent 2. **Status:** six of eight components independently match the copied `acceptance.json` SHA-256 commitments. The complete envelope does **not** pass because K04 and K08 remain unresolved.

The local export is the evidence source; its `evidence/recovery-routing.json` and `resources/verify.py` define the reduction and acceptance logic. No remote systems, facility equipment, or historical operating controls were contacted. All values below are uppercase 32-character hex.

| Slot | Verified value | Primary evidence / derivation |
|---|---|---|
| K01 | `049AAB2E1CDE7A82CD7C60234303C91A` | `mail/03.eml`, `06.eml`, `14.eml`: signed WN-14 ink A `049AAB2E`, B `1CDE7A82`, C `CD7C6023`, D `4303C91A`; concatenate A,B,C,D. |
| K02 | `0D7E3AB56FB75DA3EB0E2E06786D239E` | `telemetry/freeze-export.jsonl`: `LT-204/DIAG_WORD`, GOOD, HOLD, UTC [21:13:40, 21:13:48), highest revision per seq 0..7; unsigned 16-bit big-endian values `57765,58484,47831,59475,41704,50973,13079,54535`; 16 raw bytes `E1A5E474BAD7E853A2E8C71D3317D507`; first 16 bytes SHA-256. |
| K03 | `1384AF96E25D6ADA666209CB55E062FA` | `mail/04.eml`, `maintenance/seal-receipts.jsonl`: highest signed CLOSED AS_LEFT revisions of PTW-417, bay order B,D,A,C: `SG-D7DAD6BC|SG-9714519B|SG-7DAD0AD4|SG-BE8E87FD` (all revision 2); SHA-256 ASCII, first 16 bytes. |
| K05 | `FF8B78200A56E8586DCDA00EF01E4572` | `recorder/format-note.txt`, `recorder/trip-recorder.raw`: TRP2 schema2; verify CRC32 of each first 20 record bytes; node 0x31, event 0x52, UTC [21:14:00,21:14:08), highest seq per latch 0..3, i.e. 300,301,302,303; concatenate opaque words without reversing; four CRC failures excluded. |
| K06 | `5DBF40EE52FAAED9A536D3326CF0D95A` | `mail/11.eml`, `procedures/RC-17-scans.txt`, `archive-labels.ini`: authorized revision C, `SERVICE_ORDER` DRAIN,ISOLATE,PURGE,VERIFY; respective four-byte footer strips. |
| K07 | `93495F5E425AB8E592123DABAEB68545` | `mail/13.eml`, `transfers/transfer-audit.jsonl`: final custodian receipt AX-7782, COMMIT dry_run=false; latest attempt per seq 0..7 gives checkpoints `8947 CEDC B9CC 73BA B7E8 7BE6 3302 C5C9`; concatenate raw two-byte values; SHA-256 first 16 bytes. |

## Unresolved components and tests

**K04 (printer escrow):** `archive-labels.ini` maps logical ESC-N to `PS-261003-0417` on the incident date. `mail/16.eml` selects the last ACK, attempt 2 (18:02 UTC) and excludes unacknowledged attempt 3. Its 16-byte RECOVER payload is `A9A9DC5731A5E2AE879C47215C2559D5`. XOR with the route-sheet mask `8556C8CB6140A7F9A5123AC7571BEE1C` yields `2CFF149C50E54557228E7DE60B3EB7C9`. **The acceptance hash for this derived component is NO_MATCH.** Hashes of masked outputs for all 133 spool lines also failed to match K04. Exhaustive mutations of up to two arbitrary bytes (7,864,320 two-position trials) and exactly three hexadecimal nibbles (16,740,000 trials) around the selected result found no acceptance match. This does not prove the payload was corrupted, but the custodian explicitly warns that ACK is not an integrity check, and no other authoritative payload was supplied. Leave K04 null.

**Further K04 corruption test (17 October):** exhausted all 234,881,024 three-byte *contiguous* substitutions in the 16-byte candidate (14 possible windows times 2^24 substitutions), comparing each SHA-256 against the recorded K04 commitment. No match. This excludes a contiguous three-byte burst error in the selected recovered payload; it does not validate that payload or rule out larger or dispersed errors.

**K08 (keeper caption):** `mail/11.eml`, `20.eml`, and `crew/noticeboard-and-desk-notes.txt` contain descriptions, draft captions, and explicit exclusions (commissioning label `Back before the first boat`; standby label `Leave the light on for the next watch`). The authenticated **final** caption is not identified. Under the routing rule, normalize to lowercase ASCII alphanumerics and spaces; compute HMAC-SHA256 keyed by nonce `5F933DA6A1BD03C32DA5CBC25344F497`; take first 16 bytes; test the slot SHA-256. A scan of 150,626 normalized contiguous word spans in the supplied textual records produced no acceptance match. The commitment can validate guesses but cannot determine unrestricted missing language. Leave K08 null.

## Verification and limits

The supplied offline verifier reports `K01,K02,K03,K05,K06,K07: PASS`, `K04,K08: MISSING`, `passed: 6`, `combined: INCOMPLETE`, `accepted: false`. The missing two components make the combined recovery key unverifiable. Do **not** silently populate K04 with the spool-derived NO_MATCH candidate or treat a plausible K08 paraphrase as confirmed.

**Next best evidence:** an independently validated ESC-N print buffer/media copy or original coupon for K04; an authenticated keeper desk caption, recovered note/photo, or contemporaneous explicit quotation for K08. Neither exists in the supplied local export. A reproducible read-only derivation is preserved as [`replay_h17.py`](replay_h17.py), and the canonical six-slot working JSON is [`h17-candidate.json`](h17-candidate.json). Both are persistent repository artifacts; neither contains an accepted eight-slot key.
