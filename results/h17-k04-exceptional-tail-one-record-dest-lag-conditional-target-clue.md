# K04 exceptional RECOVER tail: one-record DEST lag matches four controls and nominates one disputed payload bit

**20:42 UTC falsification addendum: competing predictor.** The four unaffected comparisons do **not** uniquely select the final word's highest two bits. Enumerating all 124 adjacent two-bit positions across all four previous 32-bit payload words yields **two** complete 4/4 predictors: (word1, bits20..21) and (word3, bits30..31). The selected copied row129 has word1 bits20..21 equal to code **2**, agreeing with row130 DEST=bench, while its word3 bits30..31 equal code **3**, disagreeing. Thus the same retained source supports both an **intact selected copy** under the alternative lag feature and a **corrupted bit** under the preferred destination-sampler feature. The preferred word3 feature has an independent ordinary-producer precedent, but *no original producer witness states it applies to the exceptional Z tail*. The alleged bit6 copy damage is **not established**, and no verified selected coupon bit follows. Treat the one-bit and 256-candidate failed hashes below as narrowly bounded conditional diagnostics only.

**Agent 1, 1 November 2026, ~20:32 UTC. Status: new target-directed, source-conditioned hypothesis; original K04 remains unaccepted.** Standalone read-only reproducer: [agents/agent1/k04_tail_lag_sft.py](../agents/agent1/k04_tail_lag_sft.py). This report identifies a narrow prospective copy-stage clue. It does not authenticate the historical producer or add a recovered K04 component.

## Original observation and why this is a distinct mechanism

The original retained printer reconstruction in the supplied 43-member ZIP has SHA-256 \`7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083\`. It contains 128 ordinary five-minute rows followed by five exceptional RECOVER tail rows, zero-based indices 128..132. The selected ESC-N/PS-261003-0417 18:02 UTC ACK attempt 2 is row129. The copied row129 PAYLOAD is integrity-unverified.

An earlier, intact-source MT19937 result established \`s131=s130+4\` under the source-matched shared-generator index hypothesis: **no spare RNG draw** can fall between row130's four payload words and row131's first payload. [Agent44's tail DEST report](../agents/agent44/k04_tail_dest_no_draw.md) therefore excluded naively reusing the ordinary cohort's *separate post-payload destination-sampler draw* at every RECOVER tail row. The original ordinary cohort has independently fitted a top-two-bit destination coding, \`0=store, 1=desk, 2=bench, 3=rejected\` ([dual sampler](h17-k04-dual-metadata-sampler.md)).

A new, narrower possibility is **one-record-lagged metadata assignment in the retained exceptional tail**: \`DEST[r+1] = top2(le32(PAYLOAD[r][12:16]))\`. It uses the original four payload words and zero additional MT outputs. It is a *hypothesis about the export/producer's association of destination to words*, not source-attested code. It differs from earlier source-only class/DEST parity gates for ordinary print rows, and from repeat-job additive or byte-permutation repairs. The selected row129 PAYLOAD is withheld until after checking the unaffected controls.

## Four original associations around the disputed selected row

The exact raw-to-number conversion is unsigned little-endian 32-bit at bytes 12..15, matching the original printer MT output interpretation. The next row's **printed DEST** is compared with that word's top two bits, retaining the previously source-calibrated destination mapping.

| Previous row / source time | Prior last payload word (little-endian) | Top two | Following row and printed DEST | Match |
|---|---|---:|---|---|
| 127, 17:35 ordinary ACK | \`80841794\` | 2, bench | 128, 18:01 RECOVER REQUESTED, bench | Yes |
| 128, 18:01 RECOVER REQUESTED | \`A4F7330B\` | 2, bench | 129, 18:02 RECOVER ACK2, bench | Yes, metadata only |
| 130, 18:03 RECOVER REQUESTED | \`64EC58DA\` | 1, desk | 131, 18:24 RECOVER ACK, desk | Yes |
| 131, 18:24 RECOVER ACK | \`9E1036E3\` | 2, bench | 132, 18:25 RECOVER ACK, bench | Yes |

All **four** available comparisons pass. None reads selected row129's copied PAYLOAD. As a calibration of scope, the *identical lag rule* fits only **36 of 127** ordinary-to-ordinary row transitions, supporting the need for an exceptional-cohort-specific rule if the tail association is real. The ordinary producer already has a different independently described sampler path. The tail model was recognized **after** inspecting same-row matching and is not preregistered; four of four is a source observation rather than a calibrated significance estimate or proof of a physical mechanism.

The fifth relevant tail transition **129→130** is deliberately excluded from fitting because its preceding PAYLOAD is the disputed selected coupon copy. Under the one-record-lag hypothesis, row130's \`DEST=bench\` predicts the **top two bits of the actual original row129 last little-endian printed word were binary \`10\`**. These are only *model-conditional* bit values.

## Specific discrepancy in the retained ACK2 copy, then one finite verifier check

After freezing the four controls and the rule, inspect the copied selected row129. Its last 32-bit little-endian word is \`D559255C\`, whose top bits are binary \`11\`, rather than the predicted binary \`10\`. The discrepancy is **bit 6 of the last physical payload byte**, \`D5\` versus the nearest suggested \`95\`.

One complete, source-nominated single-bit correction is therefore:

- Corrected hypothetical raw payload: \`A9A9DC5731A5E2AE879C47215C255995\`.
- XOR with the unchanged official K04 route mask: \`2CFF149C50E54557228E7DE60B3EB789\`.
- SHA-256 of this 16-byte K04 candidate: \`1c72d9c52757fd8916072efa2cb753a422ea98fb3cc70dbfcfad594028b42f8b\`.
- Original unchanged K04 commitment: \`930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0\`.
- **NO_MATCH.** This is one hypothesis-derived test, not a wider edit-radius scan; earlier unrestricted one-bit repair searches also failed.

The retained 18:02 ACK2 copy already failed the original K04 digest before this test. The new hypothesis cannot explain the complete missing component through this one bit alone. Other copied bytes, the mask transcription or the lag assumption itself may be wrong.

## Evidence limits and target cut

The four destination labels and the four payloads all come from **the same reconstructed spool source**. No original print-media integrity record separately authenticates either the printed DEST metadata or the asserted one-row delay. The source does not state that the export delayed DEST by one record. Its 21-minute jump and job change between rows130 and131 make any claimed physical producer mechanism especially speculative; a format or recovery-export association would be a separate hypothetical explanation. The four comparisons were noticed retrospectively among possible lag positions.

Accordingly, the inference **does not establish any independently authentic selected K04 bit**. It offers a precise **two-bit conditional constraint** and singles out one source-copy conflict, with one direct commitment NO_MATCH. It neither certifies the historical coupon nor helps K08's exact final caption. The p955 unrestricted-state 128-bit source ambiguity remains until an actual target-integrity or source-defined target operation is established.

**Falsifiable next evidence requirement:** an independently retained exceptional-tail printer/export serializer describing destination-to-payload indexing, or an original printer/device output / separately checksummed selected attempt2 coupon. If such evidence confirms this association, use the two constrained bits in a genuinely target-directed recovery. Until then, retain original candidate status: K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, REC8 incomplete and not accepted.

The source ZIP, original verifier, routing and commitments were read only. The selected payload was excluded from the model-fitting controls and read only for the one post-fit diagnostic and hash check.


## One source-cued composite corruption pilot, 256 assignments (20:36 UTC)

The selected copied payload begins \`A9A9\`. A second, strictly defined copy-fault hypothesis is that original first byte \`A9\` was duplicated into the copied **second** byte, overwriting one unknown original byte, while the independent lag-derived constraint requires last payload byte \`D5→95\`. This offers **one 256-candidate family**; no other positions, shift amounts, extra bits or replacement words are searched:

\`original_possible = A9 || unknown_byte_00_to_FF || DC5731A5E2AE879C47215C255995\`.

This is a hypothesis about two faults in one reconstructed copy; the source does not establish that either happened. It is motivated by two specific observations, rather than an unbounded edit-distance expansion. Every one of the **256** complete 16-byte candidates was XORed with the unchanged incident-date mask and SHA-256 compared with the original K04 commitment. **Zero matches.** A synthetic positive control with replacement second byte \`42\` produced a unique match to its own manufactured digest, proving the scanner does not omit that exact case.

The original four-tail-control test was not refitted after this negative. The added 256-candidate loop is now included in the same [source-pinned SFT](../agents/agent1/k04_tail_lag_sft.py).

**Important existing overlap:** a *different* hypothesis, duplication/byte insertion that shifts all following bytes by one and loses the final true byte, was already subsumed by Agent9's complete one-unit deletion/insertion audit, including all 256 inserted-byte values and positions ([prior results](h17-k04-internal-splices.md)). Do not rescan that one-byte-shift family or present its lag-restricted 64-candidate subfamily as novel. The actual new finite pilot here is a *dispersed* second-byte overwrite plus fixed last-byte bit flip, rather than a shifted byte stream. It also falls outside the earlier distance≤6 pure-bit-flip bound for replacement bytes differing in many bits, but does not establish a source-grounded upper bound on other errors.

**Disposition:** both the single-bit suggestion and this two-fault composite are rejected by the original slot hash. The delayed-DEST pattern remains an unverified copy/producer association and K04 remains wholly unresolved as an authenticated 16-byte component.


## Distinguishing the tail-format cohort from ordinary RECOVER-class rows (20:38 UTC)

A further exact original-source control separates two potential explanations for the four-of-four association. In the **127 ordinary-to-ordinary transitions**, stratify the same previous-last-word top-two-bit lag comparison by the *following* row's CLASS: **LABEL 15/51**, **STORES 11/41**, and **RECOVER 10/35**. Thus the proposed lag pattern does not extend to the 35 ordinary five-minute RECOVER-class entries. Its small successful cohort is the exceptional final five-row section, not the word RECOVER alone.

The text export also changes UTC serialization at the precise ordinary→exceptional boundary: rows0..127 use \`+00:00\`, while rows128..132 use \`Z\`. This is a real retained formatting difference and offers a **specific place to look in an original spool exporter/merge schema** for a changed field association. It does **not** prove that a parser shifted DEST, that any bytes were corrupted, or that timestamp punctuation caused a physical change. In particular, the four tail comparisons are all from the same reconstructed artifact, and the model remains chosen retrospectively. Both the historical source/copy mechanism and the actual selected coupon remain missing.
