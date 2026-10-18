# Agent 18 continuity: H-17 source replay and evidence-gap assessment

**Invocation:** 2026-10-18, normal research mode selected by actual secrets RNG result 7. Root COUNTER 24 -> 25, confirmed remote update. Claimed previously unused Agent 18 with run `aurora-eighteen-20261018` at **2026-10-18T00:53:54Z**, pushed lease and fetched to confirm. Original claimed_at must remain immutable. Repository README prohibits per-commit workflows.

## Local source reconstruction

Unpacked uploaded 43-member ZIP in an invocation-local `/mnt/data/h17_case`. Wrote an **independent** stdlib read-only six-source reducer at `work/recover_case.py` and a local candidate; it selects source records directly, then invokes unmodified `verify.evaluate` in memory. This independently confirms K01 `049AAB2E1CDE7A82CD7C60234303C91A`, K02 `0D7E3AB56FB75DA3EB0E2E06786D239E`, K03 `1384AF96E25D6ADA666209CB55E062FA`, K05 `FF8B78200A56E8586DCDA00EF01E4572`, K06 `5DBF40EE52FAAED9A536D3326CF0D95A`, K07 `93495F5E425AB8E592123DABAEB68545`. Untouched original `verify.py --candidate candidate.json --json` reports 6 PASS, K04 and K08 MISSING, combined INCOMPLETE, accepted false. The original checker returns exit code 1 as expected.

K04 exact incident ESC-N job PS-261003-0417 RECOVER last acknowledged attempt2 remains payload `A9A9DC5731A5E2AE879C47215C2559D5`. XOR original mask gives `2CFF149C50E54557228E7DE60B3EB7C9`, SHA256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`, which fails target `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`. K08 authenticated final margin text is not in preserved notes/mail; descriptions and drafts do not fix exact normalized words. K04 and K08 must remain null.

A user-facing reproducible bundle was generated at invocation-local `/mnt/data/h17_recovery_package.zip` (48 members, zip CRC checks pass, bundle SHA256 `59f3a436c15d4944ef9e40e99bcd5da414bc620f283aac001e6bea86b3c52310`). It contains the untouched 43 source files and verifier/commitments plus candidate, verifier JSON, independent read-only reducer and source-by-source notes. Invocation-local paths are not persistent across agent runs.

## Exploratory leads not promoted

- The spool's ordered 133 PAYLOAD fields were concatenated as hexadecimal nibbles. All 4,225 overlapping 32-nibble windows, including 16-byte windows crossing payload-field boundaries, were evaluated under the unchanged mask and SHA256 target. No K04 acceptance hit. This is a narrow source-backed inter-record splice idea, without original provenance or a general impossibility result. No noisy public result created.
- A small Python MT seed probe (100,000 seeds × first 128 32-bit outputs against first regular spool payload prefix) and a set of 46 date/named seeds × first 30,000 32-bit outputs had no hit. Stronger related RNG probes were already logged by Agents 1, 10, 12, 15, 16. This speculation was not published.
- ZIP timestamps were identical for all 43 members (2026-10-04 11:40:00); external/internal attributes and compression versions were also uniform. The preexisting broader ZIP audit already excludes common hidden metadata/slack carriers.

## Research direction and limits

Read public results README, strong source-sufficiency and bounded search reports, latest Critic gate and identities 1/2/3/4/14/15/16. Their existing work already covers extensive K04 corruption families, source-carrier scans, K08 phrase grammars, selector controls, ZIP integrity and chronology anomalies. **Do not duplicate**. New research should begin from a genuinely newly observed permitted carrier or independent source-backed transform and retain unchanged acceptance. The human maintainer's 'solvable' assertion is not evidence of any particular candidate. No complete key, no original-source authenticity witness.

No remote facility equipment or original mailbox access occurred. Shared repository resources and local ZIP left unmodified. No findings merit a results README edit yet.

## 18 October 2026, 15:56Z continuation (new invocation)

Claimed Agent 18 again with verified remote lease `h17-autonomous-18-20261018-20261018155625079` (original claimed_at 2026-10-18T15:56:25.079Z). Current user explicitly wants **only a completely validated final key**, so do not create or send any six-slot handoff artifact. Reviewed current public source-sufficiency and Critic 15:46 UTC guidance; still no accepted K04 or K08. Extracted original 43-member ZIP in invocation-local `/tmp/h17_case` and inspected printer tail, crew notes, mail chronology, original acceptance/checker. Selected 18:02Z K04 ACK has no independent media integrity; K08 margin remains unquoted. A targeted exploratory check of known printer payloads against unkeyed digest families SHA256/MD5/SHA1/SHA512/BLAKE2 and 17 source-anchored string templates (job IDs, dates, attempts, index) plus common per-job `random.Random` seeding patterns found no two-byte prefix match across 133 rows. This narrow negative is **not** source-authenticating and should not enter results/ without a reason to believe the printer device used such synthesis. A worker-agent consultation attempt failed with upstream 404; no external source was contacted. No new original candidate or valid eight-slot inventory was established.

Next useful work must offer new evidence with authentic provenance (correct K04 payload/mask or exact K08 caption), not more speculative hash or language enumeration. Original case records unchanged.
