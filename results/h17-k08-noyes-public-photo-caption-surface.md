# K08: newly inspected source-linked public image captions and assets

**Agent 4, 20 October 2026, 03:27 UTC.** Read-only source-acquisition experiment following the human's removal of the earlier local-only access restriction. This tests a newly identified *publicly linked media source class*, not another free-form K08 HMAC candidate list. **Exact final keeper-caption words recovered: zero.**

## Original anchor and previously uninspected surface

The genuinely released 2025 BX25/08 risk/property folio gives the precise `https://noyes-energy-group.pages.dev/` correspondence hostname; see [folio evidence](h17-bx25-released-original-page-and-k04-source-gate.md). [Agent 5's earlier public-site census](h17-noyes-public-correspondence-source-triage.md) read the 11 linked HTML pages and site.js, but its parser collected `<a href>` paths and visible ordinary text. It **did not collect and retrieve the image URLs in `<img src>`/`srcset`, OG/Twitter image metadata, or URLs exposed by CSS**. This was an original possible K08 photograph-caption/asset witness surface because the 2026 original N10/N13/N20/N23 notes describe Emily revisiting a photograph and inscribing an unquoted final desk margin.

Target-facing falsifier specified ahead of retrieval: a public image alt/label, SVG caption, or metadata-associated quote specifically attributable to the late H-17 watch/Emily/final recovery envelope would be new exact-word evidence requiring independent date and provenance validation; a generic marketing/renewables image caption would not constrain K08.

## Executed read-only acquisition

[Original reproducible SFT](../agents/agent4/k08_public_media_asset_census.py) discovers media URLs from the 11 anonymously reachable linked corporate HTML pages, their `img`/`source`/`video` attributes, `srcset`, `og:image`/`twitter:image`, linked CSS `url(...)` and direct on-site media hyperlinks. It downloads discovered media with a 2 MB response cap and SHA256 logs, bounded to same-origin HTTPS paths, excluding `/admin` and `/api/`. No guessing hidden paths, credentials, form submissions, JS execution, or service mutations. It extracts published HTML alt/meta descriptions and textual media markers; it does **not** perform OCR on picture pixels or recover unpublished portal records.

A [manual-only GitHub Actions run **39364376040**](https://github.com/FlareZ123/workplace-v1/actions/runs/39364376040) completed **successfully** on exact code revision `3b35457c2c5dcf475bdf832939f3b0373d9bcc74`, no per-commit trigger. Actual executed output:

- **11** same-origin public HTML pages, the same count as the earlier ordinary-text crawl.
- **39** original public image-alt and HTML meta-description entries, with full individual quoted strings in the linked CI logs. Image alt text describes wind turbines, solar panels and transmission infrastructure. None names H-17, Emily, night-watch crew, final desk phrase, late-watch photography or REC8.
- **1** linked stylesheet `/assets/site.css`, 25,949 bytes, SHA256 `949c49b6552fa781afb915719ce5c470707ae992dda17e42fb1068d71b07e8bd`.
- **4** distinct discoverable media assets: `/assets/grid.jpg` (134,558 bytes; SHA256 `97e6fec819d1d9ce76566da2b0342bf168e054f5ba43ef9b3f027fefaeb2d04f`); `/assets/mark.svg` (182 bytes; `8af5c1d558215edd72963a05f1d23e33f3346090de435d1c6318141018844e9f`); `/assets/solar.jpg` (253,384 bytes; `99fbea5b509e5bf91e84872bca1c56c965ab66967471295bd62b2d817ba807eb`); `/assets/wind.jpg` (523,228 bytes; `80026f3f1c5d959159a68a0af0d2fffd7578c9af2b9f2a4012064f399`). No keyword-bearing printable image metadata or textual SVG content surfaced in the bounded probe.
- Homepage SHA256 `5d4aa1dd3f82e3ed63095a24b6ad76a08ac0e1536c0fd7ec7ea96be91431b653` confirms the same original public homepage as Agent 5's previous observation.

The first CI attempt **39364306527** encountered a Python CSS regexp syntax error before network retrieval; it contributes no source observation. The fixed parser's succeeding exact-head run is the sole evidence source for the results above.

## Decision and limits

This closes the **linked-public-photo-caption/alt/stylesheet surface** missing from the preceding public-site census. No 3 October 2026 original desk margin or final K08 caption is quoted. Thus actual new K08 normalised literal words **0** and actual K04 selected coupon bits **0/128**. The generic public photo descriptions are not evidence that Emily used any of their words, so no unanchored HMAC guesses are warranted.

This does not inspect visual pixels, unlinked assets, accounts, private endpoints or historical archive disks. It cannot establish the absence of such a record elsewhere. The original route, nonce, commitments and verifier are unchanged. **REC8 remains K04/K08 unresolved.**
