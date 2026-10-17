# H-17 archive recovery: current evidence

**Recovery status, 17 October 2026:** The original REC8/1 acceptance inventory confirms six components: K01, K02, K03, K05, K06 and K07. The [candidate](h17-candidate.json) and [unchanged-verifier output](h17-verify.json) record **6 PASS, K04 and K08 MISSING, combined INCOMPLETE, accepted false**. No complete eight-component recovery key has been verified. Original evidence and acceptance commitments must remain untouched.

## Strongest source-grounded findings

[First reconstruction and per-slot derivations](h17-recovery.md) and an [independent evidence-provenance audit](h17-evidence-audit.md) support the six confirmed components. The [read-only standard-library replay](replay_h17.py) derives them from `resources/evidence/` with the original routing and selection rules, including the telemetry revision filter, TRP2 CRC exclusion and transfer retries.

For **K04**, the incident-date logical ESC-N route maps to job `PS-261003-0417`. Its last acknowledged RECOVER attempt is attempt 2. The source payload `A9A9DC5731A5E2AE879C47215C2559D5` XORed with the recorded mask yields `2CFF149C50E54557228E7DE60B3EB7C9`; this **fails** the original K04 SHA-256 commitment. A dispatch ACK is explicitly not an integrity certificate for the retained printer bytes.

The [exact-job retry-divergence audit](h17-k04-retry-divergence.md) and [independent Hamming-geometry check](h17-k04-retry-nonredundancy.md) find that all three retained RECOVER retries differ at each corresponding byte position, with pairwise distances 68, 62 and 62 bits. If the attempts were corrupted copies of an identical source, the exact minimum possible maximum error per attempt would be 34 bits. **The records do not establish that common-source premise**, and neither result authenticates the selected ACK.

A focused [K04 source-rule consistency certificate](h17-source-rule-consistency.md) independently checks all 133 complete spool payloads with the fixed mask (zero accepted), quantifies the anomalous `mail/16` chronology, and separates the deterministic NO_MATCH from hypothesized missing evidence. These tests still do not provide the correct K04 bytes.

For **K08**, the crew notes and email describe a final personal keeper caption but never quote its authenticated exact words. The first and second Emily drafts, as well as the distinct standby and commissioning labels, are not accepted. The [K08 textual audit](h17-k08-textual-coverage.md) finds no retained mail attachments or photographs that would supply the missing final wording. The public nonce and HMAC reduction can validate a proposed exact phrase; they cannot recover unknown original language by themselves.

Source coverage has been checked independently: the [43-member ZIP equivalence audit](h17-export-equivalence.md) finds that the supplied ZIP's extracted bytes match all corresponding repository resources by Git blob ID. The [preservation manifest](h17-source-blob-manifest.json) and [read-only checker](check_h17_source_manifest.py) establish a reproducible drift check. They do not certify whether the original export included all material.

## Bounded negative experiments

These tests constrain named hypotheses about source recovery. Counts across rows can overlap and **must not be summed as distinct recovered possibilities**.

| Evidence hypothesis | Exact bounded test | Result and reproducer |
| --- | --- | --- |
| Small corruption of K04 last-ACK output | All bit-flip combinations of Hamming distance 0–6, 5,699,195,233 candidates | [NO_MATCH](h17-k04-bitflip-bound.md); [five-bit script](h17-k04-bitflip-check.py) and [six-bit source](h17-k04-hamming6-sharded.c) |
| One aligned printer word damaged | All replacement values for each of four aligned 32-bit locations, 17,179,869,184 candidates | [NO_MATCH](h17-k04-wordscan-bound.md); [scanner source](k04-wordscan-fast.c) |
| Mixing retained retries for exact K04 job | Three RECOVER attempts, independent per-position byte selection, 3^16 assignments | [NO_MATCH](h17-evidence-audit.md); [source](k04-byte-mosaic.c) |
| Whole-bitstream shifted at the boundary | Every 1–23-bit left/right shift with all replacement edge bits, 33,554,428 assignments | [NO_MATCH](h17-k04-bit-boundary-slip.md); [source](check_h17_bit_slips.py) |
| One internal deleted-and-reinserted fragment unit | Bit, nibble and byte units at every removal/insertion position, 114,688 assignments; 83,945 unique candidate payloads | [NO_MATCH](h17-k04-internal-splices.md); [source](check_h17_internal_splices.py) |
| Variable fragment concatenation error | Every two- to five-block contiguous partition, permutation and per-block byte reversal, 5,421,480 assignments | [NO_MATCH](h17-k04-fragment-ordering.md); [source](check_h17_fragment_permutations.py) |
| Final K08 wording composed of retained drafts and notes | Exact-note, span, subsequence and constrained cross-note phrasing tests | [NO_MATCH within stated grammars](h17-evidence-audit.md); [textual limits](h17-k08-textual-coverage.md) |
| Verbatim carriers anywhere in the 43 original file members | 108,021 raw 16-byte and 432 hex-text windows for K04 coupon/K04+K08 direct components; 618,316 contiguous 1–40-word K08 spans | [NO_MATCH in explicitly defined original-data extraction classes](h17-all-file-carrier-bound.md); [read-only scanner](check_h17_all_carriers.py) |

Additional targeted K04 byte-substitution and boundary-slip scopes appear in the [original reconstruction](h17-recovery.md) and [provenance report](h17-evidence-audit.md). Negative mutation tests do not establish which original source bytes were lost or whether a particular corruption mechanism occurred.

For a compact side-by-side assessment of what the preserved sources actually establish for each unresolved slot, see the [K04/K08 source-sufficiency matrix](h17-source-sufficiency-matrix.md). It separates observed data, authenticating evidence, contradictory chronology, tested carrier classes and conditions for promotion.

## What can complete recovery

An independently integrity-checked incident-date ESC-N original coupon, printer-media capture or exact ACK buffer with provenance could supply **K04**. An original signed desk margin, envelope image or trustworthy verbatim contemporary quotation of Emily's final caption could supply **K08**. The [missing-evidence intake plan](h17-missing-evidence-intake.md) states needed identifiers and custody documentation. Use [K04 coupon validation](check_h17_coupon.py) and [K08 caption validation](check_h17_caption.py) against the untouched individual commitments. Only after both components pass should the original offline verifier be rerun for the combined commitment.

The earlier [Critic evidence-provenance review](../communications/broadcast/2026-10-17T204358Z_Critic_evidence-provenance.md) recommends prioritizing independently authenticated missing sources over unguided preimage searches. Existing evidence supports six verified components, and the two remaining original-source claims are unresolved.

**Source-sufficiency boundary (updated 18 October):** A normal-mode researcher has now inspected the additional permitted repository area: current `private/` contains only `.gitkeep`, with no source material; the local upload contains `prompt.md` and the same 43-member ZIP ([Agent 10 scope audit](../communications/broadcast/2026-10-17T224430Z_agent10-private-scope.md)). [Source-rule consistency](h17-source-rule-consistency.md) separately reconciles the incident-date ESC-N mapping and records the uncorrected time discrepancy: `mail/16.eml` at 07:49 UTC anticipates the 18:03 UTC requested spool attempt. Another mismatch is `mail/13.eml` dated 2 October describing the AX-7782 final handoff, while its COMMIT record is 3 October at 20:55 UTC. These anomalies affect evidence provenance; they do not supply accepted K04 or K08 bytes. The supplied materials and checked permitted locations have yielded no independent coupon or verbatim final caption. This is **not** proof that no inferential recovery method exists. The [Critic's evidence-first decision gate](../communications/broadcast/2026-10-17T224013Z_Critic_sufficiency-falsification.md) remains appropriate. Current outcome remains **6 PASS, 2 MISSING**, and the original case forbids external contact.
