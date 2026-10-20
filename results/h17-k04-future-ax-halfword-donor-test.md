# K04 forward-state donor attack: original AX checkpoint halfwords versus TRP2/RC17 words

**Agent 8, 20 October 2026 (UTC 19 October ~00:10 Dublin).** A **new target-directed, bounded negative** involving original cross-source bytes. The selected printer row129, masked coupon, original REC8 commitments, verifier and all K08 candidate material are **excluded**. No recovered coupon bit is claimed.

## Original source anchor and testable producer mechanism

The source original `evidence/transfers/transfer-audit.jsonl` has 64 two-byte AX checkpoints. Agent36's earlier [AX-7778 printer bridge](h17-k04-transfer-checkpoint-16bit-bridge.md) found one exact ordered four-word and one independent three-word match between the **little-endian** checkpoint numbers and upper-16 tempered MT19937 output bits reconstructed from intact printer words. This motivates the *specific* test that a future indexed AX checkpoint could be a partial original MT output, potentially informing the K04 target. Include both byte orders as an explicit sensitivity check. The original 88 TRP2 four-byte controls and 12 RC17 footer strips are a separate, previously documented fullword MT-carrier class.

Agent29's newly obtained [original-printer-conditioned forward-state equations](h17-k04-forward-donor-leverage-and-source-xor.md), in the source-consistent but historically **unverified** index955 chronology, yield four XOR constraints between future MT words:

| Conditional future word pair | Known untempered XOR bits | Source-predicted masked XOR |
| --- | --- | --- |
| 1412 / 1866 | FFFFFFFF | BD2761F8 |
| 1185 / 1412 | BFFFFFFF | 359EC0C7 |
| 1185 / 1866 | BFFFFFFF | 88B9A13F |
| 1411 / 1865 | 9FFFFFFF | 0CDE27B9 |

A full 32-bit carrier at either future position and a 16-bit upper-tempered AX checkpoint at the other must obey the projected XOR. Account exactly for the unknown bits in the masks by enumerating both (or four) completions through the **linear MT tempering** transformation. This is an original-source-driven necessary condition for a *future donor pair*, independent of the contested target payload or the acceptance SHA. It is stronger than assuming a future index from file order or testing the K04 hash on fabricated coupon bytes.

## Source-bounded calculation

Original SHA256 source pins: transfer JSONL `32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf`; TRP2 raw `5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba`; RC17 scans `a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d`. Read all 64 AX chunks and all 100 original external fullword fields, retaining recorder CRC state for provenance. Test 200 little-/big-endian fullword interpretations against 128 AX halfword orientations. Separately test 64 AX fields against one another in **globally consistent** little and big-endian interpretations.

| Future pair | Fullword external ↔ AX halfword matches | AX ↔ AX pairs, little | AX ↔ AX pairs, big |
| --- | ---: | ---: | ---: |
| 1412 / 1866 | 0 | 0 | 0 |
| 1185 / 1412 | 1 | 0 | 0 |
| 1185 / 1866 | 0 | 0 | 0 |
| 1411 / 1865 | 2 | 0 | 0 |

The three halfword coincidences are:
1. For 1185/1412: **TRP2 record17** (CRC-good, little-endian four-byte control) with **AX-7778 seq4 attempt1** (little-endian checkpoint `7CA7`, numeric `A77C`).
2. For 1411/1865: TRP2 record8 (CRC-good, big-endian control) with AX-7783 seq3 attempt1 (little-endian).
3. For 1411/1865: TRP2 record24 (CRC-good, little-endian control) with AX-7783 seq1 attempt2 (big-endian).

**No hit has the independently established correct future stream index difference.** For the only collision involving the historically cross-anchored AX-7778 cohort, the already published row34-relative coordinates put TRP2 record17 at `s41-622 = -565` (because `s41-s34=57`) and AX seq4/attempt1 at `-407+8 = -399`, a difference of **166** state outputs. The candidate future pair 1185/1412 requires a difference of **227**. This false positive fails a discriminating independent index test; it must not be promoted to a 16-bit K04 discovery. AX-7783 has no corresponding authenticated MT phase mapping here; its two apparent hits are also unindexed, and one requires mutually inconsistent field byte-order choices for a common-stream producer.

The unindexed null model expects approximately **3.515625** fullword–AX coincidences across the four predicates and both byte orientations; three observed matches carry no convincing independent support. AX-only comparisons have expected ~0.55 random coincidences across both global endian cases; observing zero is unsurprising. Counts describe attempted labelled pairings rather than independently sampled random draws.

## Interpretation and cracking decision

- **New discriminating fact:** No original AX-pair in either global orientation satisfies the four future-state XOR tests. The apparent cross-carrier fullword/AX matches fail to supply indexed target observations, particularly the independently contradicted AX-7778 candidate above.
- **Target-bit gain: zero.** The known six REC8 slots are unchanged; K04/K08 remain missing. This closes this *bounded high16 future-donor pairing class*, conditional on Agent29's index955 chronology and the source-derived AX high16 producer model; it is not a global prohibition on future donors.
- **Next positive path:** locate a genuinely historically indexed state1412/1866 source or a producer/seed/order specification predicting a withheld intact printer output, then project it to the K04 last word via the already published full32 XOR equations. A larger free-choice permutation of AX fields would repeat the very unindexed false-positive problem identified here.

[Read-only single-file reproducer](../agents/agent8/k04_ax_future_halfword_sft.py): `python agents/agent8/k04_ax_future_halfword_sft.py original-case.zip`. The exact committed file was not executed inside a Git checkout; a method-equivalent independent local scan against the untouched user ZIP produced the stated counts and original literals. The SFT pins original source SHA digests and includes positive checks of the MT mask/tempering projection. Neither original sources nor acceptance commitments were modified.
