# H-17 public correspondence source: human privacy correction and original page delta

**Agent 9, 20 October 2026 ~03:45 UTC.** This is a new public-source delta check prompted by the human maintainer's 03:31 UTC addition, not a recovery result. The original K04 and K08 target values remain unknown.

## Exact new upstream anchor

A new human-maintainer file `communications/broadcast/2026-1792466991500`, commit `ae5bd56a3` at ~03:31 UTC, says: "The Noyes Energy Group page's privacy policy has been updated by corporate, the password database log was the result of a dev server going live by accident." This materially changes one obstacle cited by Agent 5's earlier public-site assessment: the old publicly posted password-logging statement is obsolete. It does **not** provide a portal login, authorize authentication attempts, or identify a REC8 target.

## Fresh source observation, after the human change

A one-time strictly read-only workflow `.github/workflows/h17-public-policy-delta.yml` invokes `agents/agent9/k08_postpolicy_public_delta.py` on manual dispatch only. [Successful run 39365890985](https://github.com/FlareZ123/workplace-v1/actions/runs/39365890985) completed ~03:44 UTC, following the maintainer notice. Script GETs only the original PDF-linked same-origin **public** `https://noyes-energy-group.pages.dev/privacy/` URL, checks the final origin, parses visible text and published links, and prints the full observed policy. No form, sign-in, `/admin`, `/api`, or user-supplied credentials are used.

- HTTP 200, 3,713 source bytes, SHA-256 `f73c9b0bf4f52443d533b477f479d486b51b4388e895f000a203e6832775428c`.
- The changed public text is limited to essential-session-cookie disclosures and an enquiries note: *"After a successful sign-in, an essential session cookie keeps the browser signed in for up to four hours. Signing out invalidates that session. The website does not use advertising cookies or third-party analytics."* It then says *"For questions about this website, sign in to the client portal."*
- The visible link inventory contains `/admin` plus already inventoried public company, expertise, projects, insights, contact, privacy and accessibility routes. The updated policy provides **no additional public records/correspondence URL, published caption, print media, coupon, mask, source seed, or authorized account detail**.

This is an *incremental* source change relative to the previously completed 11-page census and original 2025 property PDF. It is not another web-crawl or repeated original-case verification. As usual, the bounded negative observation does not exclude genuinely new future public content.

## Consequence for new K04/K08 cracking

The obsolete privacy-logging claim should no longer be used as a reason that **a properly authorized** person could not use the portal. However, updated cookie rules and deletion of the logging disclosure **do not grant** portal access or supply any account credential. The site routes visitors to a credentialed portal for enquiries, and no authenticated user context is present in the case. Any new original October 2026 ESC-N attempt-2 coupon, historical printer buffer, mask, producer-state witness or keeper final-margin quotation would require its own verifiable source provenance. A bare login could not itself prove those contents.

No new source-supported K04 bits (still 0/128), exact K08 normalized words (still 0), or original REC8 passes resulted. The six previously accepted slots are unchanged. Do not spend further CI on public privacy or original BX25 material absent another independently new source change.

## Distinctness / reproduction

Earlier Agent 5: `results/h17-noyes-public-correspondence-source-triage.md` and public-site crawl run 39361916034. Agent 4: `results/h17-k08-noyes-public-photo-caption-surface.md` and run 39364376040. Agent 11: source-index run 39364349829 found `robots.txt` public but `/sitemap.xml` HTTP 404. These predate the new maintainer privacy correction and none collected its revised page at 03:44 UTC. Our new observation intentionally stays limited to this modified page and does not duplicate public linked-media/sitemap reviews.

**Source boundary:** historical records recovery only. No password testing, login API probing, user-data harvesting, or live facility interactions.
