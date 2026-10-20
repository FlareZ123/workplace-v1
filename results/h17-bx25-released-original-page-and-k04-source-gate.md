# BX25/08 original PDF unlocked: 2025 printer-property identity, no direct K04 or K08 coupon

**Agent 45, 20 October 2026, 02:27 UTC.** A genuinely new original corporate supplement, committed by the human maintainer at `ca43daaec` on 20 October 02:08 UTC, was read successfully. **The PDF release password is `8131`; this is not K04, K08 or any REC8 component.** The original K04/K08 components remain missing.

## New original source and release mechanism

- Source: `resources/evidence/h17-supplemental-office-files/BX25-08.pdf`, exactly 5,407 bytes, blob SHA `cd69d8da88c7704a50a4199e190909e31015dc99`, original SHA256 `b6a6156f596575b988126c6d3e5cbb88d5794cc927a5564c37b6ddb8cecc3425`. This PDF was **not** present in the older 43-member H-17 ZIP.
- Local original `retired-office-bookmarks.html` says the old BX25 scanner used a **four-position numeric release setting** and its Risk-desk paper register was not exported. This prescribes the finite local release-code class `0000` through `9999`.
- The PDF's original Standard Security Handler R6 `/U` validation field has 48 bytes: first 32 verification bytes and next 8 validation salt. Enumerated all 10,000 zero-padded numeric settings using `pypdf._encryption.AlgV5.calculate_hash(6, pin_bytes, U[32:40], b'')` and compared against original `U[:32]`. **Exactly one match: `8131`** (after 8,132 attempted numbers). No REC8 target or archive key digest was read to derive this result.
- Independent PDF reader opening via the public `PdfReader.decrypt('8131')` method succeeded. A read-only manual workflow `.github/workflows/h17-bx25-released-review.yml` generated `[Actions run 39359009449](https://github.com/FlareZ123/workplace-v1/actions/runs/39359009449)` job `118420494830` with a **successful SHA256 check and one fully extracted original page**. Full read-only, SHA-pinned release reproducibility: `agents/agent45/bx25_release_sft.py`. No source PDF, hash commitments or verifier was altered.

## Exact original page anchors, and their evidentiary force

Source **page 1 of 1** is headed `RISK DESK - ANNUAL PROPERTY DECLARATION`, `TRANSFER COPY / 2025`. It contains these verbatim fields:

- `Register: H17-POL-17`; `Property annex: A3 - North office equipment`; `Account reference: FA-17`; `Inward scan folio: BX25/08`.
- `SCHEDULE ACCOUNT HOLDER / NAMED INSURED`: **`Noyes Energy Group`**; `Operating company - H-17 Atlantic facility`.
- `FA-17 North office printer / cassette cabinet carry-forward: maintained`.
- `FA-18 Network service desk and local archival station carry-forward: maintained`.
- `Policy year: 01 Jan 2025 - 31 Dec 2025`; `Renewal review: recorded 18 Nov 2025 / Property team copy`.
- PDF footer `Electronic correspondence index: https://noyes-energy-group.pages.dev/`. This is an external historical locator. It was **not accessed**, because the local case instructions expressly exclude outside source solicitation and systems.

The newly readable original PDF corroborates the `FA-17` and `H17-POL-17/A3` **equipment property identity** already indexed in the supplemental fleet return note and supplier reconciliation. The new unreduced named-insured value `Noyes Energy Group` was absent from the redacted case ZIP. The page does **not** provide a 2026 RECOVER attempt-2 payload, separate print checksum, route XOR mask, printer model/serial, deterministic producer recipe, random-state observation, or Emily's final keeper caption. It is a **2025 Risk-office declaration**, so any link from it to 3 October 2026 printer *payload bytes* needs an independent historical bridging source. Do not imply that a property-ledger association authenticates selected row129 bytes.

## Pre-hash producer hypothesis using the newly unredacted name

A narrow possible new input is the previously redacted company identity acting as a deterministic CPython MT19937 seed. This is **only a hypothesis**: the PDF never states the printer uses it as a seed.

An original-source-only held-out negative control tested **18 spelled source-derived representations**, including `Noyes Energy Group`, case/slug/name-only spellings, domain URL, H-17 name combinations, and the recovered four-digit PDF release setting. Each supplied five explicit CPython seed recipes: UTF-8 text, UTF-8 bytes, integer from full UTF-8 bytes, CRC32 integer, and top SHA256 word integer (**90 proposed seeds total**). Tested 65,536 consecutive 32-bit MT outputs per seed, against all **792** original adjacent two-fullword signatures from the 132 intact printer rows with both endian serializations; disputed row129, route mask and all REC8 commitments were withheld. **Zero two-word source matches**. A real CPython synthetic positive test using the same `Noyes Energy Group` seed at output index195 passed. The result excludes the exact 90 seed recipes and first-65,536-offset two-word coincidence model, not every company-named producer or the actual historical generator. It recovers zero coupon bits. Local scratch reproducer: `/mnt/data/h17_noyes_seed_holdout.py`; promote to a repository SFT only if a stronger original-seed rule emerges.

## Cracking decision and limitations

A concrete original source was recovered from an encrypted state, supplying a real property-account and named-insured identity. **Actual selected K04 coupon information remains 0/128 bits and K08 exact final-caption information remains zero words.** The PDF release code `8131` passes a separate PDF-authentication predicate, never the original REC8 predicate.

The source directly closes the question of whether BX25/08's page itself contains a 2026 printer coupon, alternate mask or final-caption quotation: **it does not**. Avoid another generic old-spool MT closure, original-43 archive sweep or prompted natural-caption dictionary. The next real REC8 gain requires a genuinely independent historically indexed coupon/mask or producer witness, or the final desk-margin exact phrase from an authorized local source. The untouched acceptance inventory remains six accepted original components and K04/K08 unresolved.
