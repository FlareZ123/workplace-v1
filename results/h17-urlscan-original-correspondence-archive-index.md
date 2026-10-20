# H-17 source-linked external correspondence: independent public scan archive index

**Agent 47; 20 October 2026, 05:04 UTC.** This is a source-acquisition discriminator, not a recovered K04/K08 component. Original evidence files, nonce, coupon mask and acceptance commitments were neither altered nor passed into the web probe.

## Exact original lead and distinct question

The originally supplied 2025 property-annex scan BX25/08 (released and classified by Agents 45/12) names the electronic correspondence index at `https://noyes-energy-group.pages.dev/`. Agent 5 checked the currently linked public site and the Internet Archive availability/CDX indexes; Agent 4 checked public image-alt/media references. None yielded October 2026 ESC-N attempt-2 coupon or Emily's final desk caption. Those were previous checks, not re-executed here.

New question: does an **independent historical public website-scan archive**, urlscan.io, already hold a publicly recorded snapshot of the exact originally cited domain, possibly preserving original indexed correspondence? This would be a *historically separate observation*, unlike reading the same live marketing pages again. The target signal was a scan of a dated original H-17/coupon/keeper-caption URL followed by independent provenance checking. Nothing behind current company authentication was requested or touched.

## Executed test and outcome

- Read-only, anonymous public `GET` for urlscan.io published scan index query `page.domain:noyes-energy-group.pages.dev`.
- Separate read-only, anonymous public `GET` for urlscan.io broader indexed-domain query `domain:noyes-energy-group.pages.dev`.
- Both calls returned **HTTP 200** on 20 October 2026 at 05:04:31–32 UTC and `PUBLISHED_MATCHES 0`, `IN_SCOPE_PUBLIC_RESULTS 0`.
- Synthetic parser control PASS; the program only reports already-published public scan metadata and explicitly filters the site's `/admin` and `/api` paths. It submits no new scan, logs in nowhere and makes no corporate API request.

**Reproducer:** [Agent 47 original script](../agents/agent47/h17_urlscan_archived_source_sft.py) and [manual-only workflow](../.github/workflows/h17-agent47-urlscan-archive.yml). **Executed source output:** [GitHub Actions run 39372924886](https://github.com/FlareZ123/workplace-v1/actions/runs/39372924886/job/118464589136). No per-commit trigger exists. Successful job exit indicates the probe ran, not that target evidence was found.

## Scope, inference and stop

This excludes only publicly searchable scans in the two **specific urlscan.io queries at observation time**. It does not establish that no scans exist under private/unlisted visibility, another archive, a physical copy, a historical R: mapped-drive index, or an authenticated corporate records location. Their absence from this public index gives **zero observed K04 coupon bits** and **zero exact normalized final K08 words**.

The historical source-to-recovered-target path failed at the very first independent archive-index witness. Do not broaden into speculative corporate path guessing, credential testing, repeated marketing-page scraping or unsupported K08 phrase checks. Future progress requires an authenticated original target-bearing source or a source-supported producer/edit rule with a withheld real-source prediction. Original all-eight REC8 acceptance remains incomplete.
