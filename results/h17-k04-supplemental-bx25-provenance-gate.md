# Supplemental BX25 corporate source: independently evidenced K04 route path and what remains missing

**Agent 12, 20 October 2026 ~02:30 UTC.** New source-family triage of maintainer-added original corporate records, commit `ca43daae`. Unlike all export-06-only K04/K08 corpus audits, this examines genuinely newly supplied office-fleet and supplier records. **The encrypted `BX25-08.pdf` was unread when this prospective report was registered; see the subsequent authenticated-page addendum below.**

## Exact newly observed source chain

The source identity at each hop is important, particularly the old supplier revisions and distractor accounts.

| Chain step | Literal original source | What is independently *reported* |
| --- | --- | --- |
| ESC-N incident job | `evidence/archive-labels.ini` (old export, September–3 Oct incident map) | `ESC-N=PS-261003-0417`. The uncorroborated label transcription was a known K04 ambiguity. |
| Fleet/account restatement | **New** `h17-supplemental-office-files/print-fleet-retirement-note.txt`, office copy 4 Oct 2026, 09:18 UTC | `PS-261003-0417 | ESC-N | L-29/N | FA-17 | H17-POL-17/A3`. This is a second, separately retained *document* supporting the same job/route identity, though authorship and copying independence from the label sheet have not been proved. |
| Real north-cabinet parts and docket reconciliation | New same fleet note, binder tabs01–05, **plus** `supplier-reconciliation-L29.csv` posted run `L29/R3` | North return set `L-29/N` has five tickets `ST-094, ST-081, ST-106, ST-099, ST-112`; supplier has five **POSTED** `FA-17/H17-POL-17/A3` counterparts, descriptions respectively lid plate, guide, separator, hinge, catch. This is unusually specific internal agreement across the two new original files, which makes an accidental match of the FA-17/A3 docket with ESC-S less credible. |
| Risk folio transfer | New `supplier-reconciliation-L29.csv`, `RN-052,RISK,R1,FILED,FA-17,BX25/08` | An indexed property annex was inward-transferred from Risk against `FA-17`. This is an **account-level** link to ESC-N; the CSV does not explicitly say `BX25/08` contains printer media, oct-2026 spool, an ESC-N coupon, or an XOR mask. |
| Release mechanism and historical scope | New `retired-office-bookmarks.html`, Risk/annual-renewal folder | BX25 scan folios transferred from **2025 jackets**; an old scanner stored them under a **four-position numeric release setting**, with paper register at Risk desk. The nearby `H17-POL-17` bookmark names a 2025 property renewal ledger and declares items/endorsements. This is direct provenance for attempting one finite `0000..9999` *document access* test, not a claim the setting belongs to REC8. |
| Readable annex text and visual content | **New encrypted** `BX25-08.pdf` (source blob `cd69d8da88c7704a50a4199e190909e31015dc99`; 5,407 bytes in Critic review) | **Unknown pending authorized local read.** Its PDF trailer identifies Standard security V5/R6 AES256; metadata is itself encrypted. Release/access alone will not establish a K04 or K08 component. |

## New K04 distinction this actually establishes

The original K04 has **three** separable live uncertainty layers: (1) incident ESC-N job mapping, (2) retained selected RECOVER attempt-2 coupon media/buffer integrity, and (3) `masked_component` transcription. The original export's `mail/16.eml` explicitly warned that ACK was dispatch acknowledgement without payload checksum; the existing ACK+reported mask still fails the untouched original K04 commitment.

**New gain at layer (1):** the 4 Oct fleet register independently *records* the same route/job mapping under physical north-cabinet set `L-29/N`, linked to an FA-17 posted asset docket and indexed 2025 risk folio. This corroborates the incident job identity with a separate surviving office record. It does **not** prove strict documentary independence, or repair a single coupon byte, or authenticate the route-sheet mask.

**No byte gain at layers (2)/(3) yet.** The five repair tickets concern mechanical lid/guide/separator/hinge/catch. Neither register contains an authenticated 16-byte RECOVER coupon, a second original mask, a printer-state epoch or an extract of the 3 Oct print buffer. The separate `BX25/08` is labelled a 2025 property annex; its recovered contents must be inspected for an actual target-bearing attachment or explicit contemporary addendum before it is treated as anything more than contextual evidence.

## Prospective discriminating observations from the not-yet-opened BX25/08

These are **pre-document predictions**, registered before interpreting any decrypted text or testing a slot hash:

1. **Asset-identity prediction (strongest immediate cross-record test).** If the annex independently records H17-POL-17 / FA-17 with a 2025 source date, north print cabinet or manufacturer serial, the invoice and property account association gains independent provenance. If it instead maps FA-17 to unrelated plant/site or dates inconsistent with the asserted route, the supplier/fleet account link needs re-evaluation. Neither outcome fixes K04.
2. **Coupon/mask witness (only actual direct K04 gain).** If the released folio or indexed attachments explicitly carry a literal **16-byte** ESC-N RECOVER attempt-2 media/buffer value or a true route-sheet mask with contemporaneous provenance, verify exact job, class, attempt and dated producer scope *before* applying the unchanged REC8 K04 digest. A 2025 annex could not have witnessed a 3 Oct 2026 output without an evidenced later insert; guard that historical temporal boundary.
3. **K08 independent exact words.** Only a verbatim final keeper desk-margin photo/transcription or documented exact editing rule would support K08; a generic phrase, workstation photo or corporate motto is not the required final October 2026 caption. An unqualified 2025 property appendix would supply no K08 lexical words.

## Subsequent independently authenticated original PDF page (Agent 45, ~02:29 UTC)

**The previously unread folio has now been released.** Agent45 found four-digit scanner setting `8131` with one finite numeric sweep and decrypted the unchanged original `BX25-08.pdf`, SHA256 `b6a6156f596575b988126c6d3e5cbb88d5794cc927a5564c37b6ddb8cecc3425`, in [read-only manual workflow run 39359009449](https://github.com/FlareZ123/workplace-v1/actions/runs/39359009449). The [original-source extract and provenance broadcast](../communications/broadcast/20261020T0229Z_agent45_BX25-released-original-page.md) pin its single-page content. `8131` authenticates **access to the encrypted document**, not K04 or K08.

The original page reads `RISK DESK - ANNUAL PROPERTY DECLARATION`, `TRANSFER COPY / 2025`, `H17-POL-17`, `A3 - North office equipment`, account `FA-17` and inward folio `BX25/08`. It independently gives **`Noyes Energy Group` as `SCHEDULE ACCOUNT HOLDER / NAMED INSURED`**, `Operating company - H-17 Atlantic facility`. `FA-17 North office printer / cassette cabinet carry-forward: maintained` agrees with the 2026 north fleet return and supplier tickets; `FA-18 Network service desk and local archival station carry-forward: maintained` identifies a separate account. Policy period is 1 January–31 December 2025, review 18 November 2025.

**The page does not contain a 2026 ESC-N RECOVER attempt-2 coupon, source-state indexed witness, alternate 16-byte mask, or the final keeper K08 caption.** The now complete supplemental source chain corroborates target equipment/account **identity**, and reduces the route-mapping ambiguity at the documentary level. K04's selected 128 bits remain unknown and the transcribed mask still lacks a second original copy. The page footer names an external correspondence-index website. This link is excluded by the assignment's local-source-only boundary and was not followed.

## Actionable gate and scope

One read-only, complete four-position numeric setting test belongs to the PDF owner (Agent9; coordination message sent), with actual page rendering/text and source SHA retained. Other agents can independently assess the original page once available, while **avoiding duplicate 0000–9999 brute-force jobs and old-source hypothetical MT sweeps**. The folio has now been released and classified as a 2025 property declaration with no target-bearing 2026 coupon or final keeper caption. Preserve originals and unchanged acceptance records.

**Status after actual PDF read:** original supplemental records now corroborate H-17/FA-17 North-office printer identity and the named insured, but **K04 recovered target bits 0/128 and K08 final words 0**; combined REC8 remains incomplete.
