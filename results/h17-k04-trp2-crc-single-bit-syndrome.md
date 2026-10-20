# TRP2's four damaged-tail CRC records share a single-bit syndrome; K04 cross-carrier repair does not accept

**Agent 43, 20 October 2026 ~01:12 UTC.** Read-only original-export experiment. [Reproducer](../agents/agent43/k04_crc_tail_layer_probe.py), run as `python agents/agent43/k04_crc_tail_layer_probe.py original-case.zip`. Source artifact: supplied 43-member H-17 export. Selected printer row129 excluded from MT cross-carrier discovery, and original K04 acceptance used only for the final finite explicit repair check. Source records, verifier, commitments and six established components remain unchanged.

## New exact source observation

The TRP2 recorder's 88 24-byte records each store an IEEE/zlib CRC32 of their first 20 bytes. Four records have bad CRCs: indices **14, 41, 72, 77**, all node 49/event 82, time **21:14:02 UTC**, latch 0/1/3/2 respectively and sequences **900/901/903/902**. For each one, the calculated CRC XOR the stored CRC is **exactly `00000100`**. Thus all four have the **same one-bit checksum syndrome**, not four unrelated random CRC defects.

Under the explicit alternative hypothesis that the *stored CRC and the other 16 non-control data bytes are intact* and only the four control bytes at offsets 12..15 were damaged, CRC32's invertible four-byte map determines a unique replacement control. All four demand the **same original-versus-restored control XOR, `3F9B320D`**.

| Original record | Seq | Retained control | Conditional control-only repair | CRC XOR syndrome |
| --- | ---: | --- | --- | --- |
| 14 | 900 | `C2DE39CC` | `FD450BC1` | `00000100` |
| 41 | 901 | `BA194782` | `8582758F` | `00000100` |
| 72 | 903 | `F2595C84` | `CDC26E89` | `00000100` |
| 77 | 902 | `2A4EE66D` | `15D5D460` | `00000100` |

The **competing simpler source model** is that the four original control fields are already intact and the stored CRC bit 8 alone was flipped in each damaged record. That requires one bit of change per record, while the control-only model requires a 4-byte XOR. The surviving format note warns of failed CRCs and does **not** identify which field suffered damage. Hence the four alternate controls are **conditional reconstructions**, not authenticated donor words or K05 replacements. The common syndrome does not authenticate historical coupling between recorder and printer.

## New K04 cracking tests from this specific source damage motif

The original printer spool also warns its retained media payloads lack integrity checks. A **cross-carrier shared-XOR hypothesis** is now finite rather than a generic bitflip radius: if the same four-byte control corruption vector `3F9B320D` affected one or more of the four aligned 32-bit lanes in the incident-date ESC-N selected ACK attempt-2 printer coupon, undo it before applying the unchanged K04 XOR mask. We explicitly tried **all 15 nonempty lane subsets** in both byte orientations (`3F9B320D` and `0D329B3F`): **30 source-motif candidates, zero original K04 commitment matches**. This is a narrow rejection of this cross-source correction mechanism, not a statement about arbitrary 16-byte corruption.

As a separate *target-withheld* producer test, each of the four conditional restored control bytes was untempered as a prospective little-endian MT19937 32-bit observation. Check its characteristic 31-bit inverse-twist fingerprint against **all pairs of the 528 intact original printer payload words** excluding disputed row129. **4 × C(528,2) = 556,512 ordered-by-source pair comparisons, zero exact 31-bit matches.** This excludes the narrow direct printer-pair bridge class for these four hypothetical repairs; it does not exclude other generator epochs, source transformations, hidden state positions or merely checksum-only damage.

### Independent original-state discriminator favors CRC-only damage at record 72

The *uncorrected* control bytes from original CRC-invalid record **72** (`F2595C84`, seq903, latch3) untemper to exactly `353CCDFC`. This is **identical in all 32 bits** to the source printer's inverse-twist expression `inverse_twist(X[row10,word2] XOR X[row41,word2]) = 353CCDFC`. The match is a previously documented original recorder/printer bridge (Agent43/Agent7), now used as an **independent discriminant between the two CRC damage layers**, not claimed as a new recorder bridge. Under control-field-only CRC repair, its alternative `CDC26E89` untempers to `7D2306F6` and loses the original bridge. The three other original raw CRC-bad controls yield no exact full32 inverse-twist printer-pair bridge among the tested 139,128 pairs each. Thus **record72 has affirmative cross-carrier support for leaving its raw control bytes intact and correcting only the CRC checksum**, consistent with the striking common 0x100 syndrome across all four damaged rows.

This provides meaningful *source-layer* evidence, but it does not prove the three other raw controls are authentic (or the source was one actual chronological MT producer), because their own preserved original 32-bit independent state witnesses are absent. The 0x100 checksum-bit model remains the simpler cross-record explanation. It still contributes **zero direct K04 selected coupon bits**.

Pinned source SHA-256: recorder `5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba`; spool `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The SFT includes synthetic positive controls for both (a) control-word XOR damage with intact CRC and (b) a flipped stored CRC bit; it asserts the exact observed four-record syndrome and tests the 30 original-target derived candidates.

## Recovery implication and limits

This is a **new original-source error signature** capable of distinguishing useful defect models when independent evidence for the damaged layer becomes available. Its most economical local explanation is four common CRC-bit flips. It has not yielded a new authenticated MT observation, coupon byte or exact K08 word. **Actual new K04 selected bits: 0/128. K08 final exact words: 0. K04 and K08 remain MISSING; no complete REC8 acceptance.** Do not use the alternate controls as valid K05 writes or promote the failed cross-carrier pattern to a replacement K04 coupon.

Future target-bearing work should look for genuinely independent printer coupon integrity evidence, historically indexed later recorder words, or an original caption quotation. This experiment should not be repeated as an expanded arbitrary XOR radius absent a new source coupling mechanism.
