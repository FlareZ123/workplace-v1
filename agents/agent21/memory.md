# Agent 21 — H-17 recovery continuity

Claimed 2026-10-18T01:55:46.570Z. Mode draw 2 (normal).

## Canonical established baseline
- Read `README.md`, `resources/START_HERE.md`, original routing, custodian note, emails, crew notes, spool and selected results/critic broadcasts. Respect case scope: local export only, no outside original source contact.
- `results/h17-candidate.json`: K01/K02/K03/K05/K06/K07 PASS; K04/K08 null. `results/h17-verify.json`: six PASS, combined INCOMPLETE, accepted=false. Source-grounded reproducible `results/replay_h17.py` and independent audits already exist. Do not duplicate them.
- K04 original rule selects 18:02 UTC ACK/RECOVER attempt 2 for incident ESC-N job PS-261003-0417; retained payload XOR mask yields `2CFF149C50E54557228E7DE60B3EB7C9`, unmodified K04 target NO_MATCH. Earlier agents have exhausted numerous error geometries; source warns ACK is not a retained-byte checksum. Exact-job retry payloads are near-independent, not error-correctable close copies.
- K08 source text deliberately identifies drafts N02/N06 and separate standby/commissioning labels while not quoting authenticated final keeper caption. The HMAC/checker is a candidate validator, not a derivation of words.
- Read most recent Critic interventions from 2026-10-18 01:06 and 01:29 UTC: prioritize observed historical anchors and provenance model, stop replay/packaging repetition and unsupported mutation classes.

## This incarnation's exploratory checks
- Confirmed ZIP's 43 original members locally; ZIP central directory member timestamps all identical 2026-10-04 11:40:00 and external attrs all identical, so no timestamp-based distinguishers in that elementary metadata class. No claim of exhaustive steganography exclusion. Agent 8 already audited ordinary ZIP metadata/compression extensively.
- Tested the first regular printer payload against Python `random.Random(seed)` streams for numeric seeds 0 through 199999 and six date-like seeds using `randbytes(16)` and `getrandbits(128).to_bytes(16,'big')`; none matched. **Do not promote this weak speculative negative:** there is no evidence of Python PRNG origin or a known seed; it does not constrain K04.
- Independently ran **unmodified original** `verify.py` on the six accepted values in supplied ZIP extraction; exactly same 6 PASS result. Produced local user handoff with candidate, verifier JSON, source-cited notes as `/mnt/data/h17_recovery_handoff.zip` (a user deliverable, not proposed shared recovery progress).
- No accepted new K04 or K08 witness yet.

## Worthwhile new investigation criteria
Propose only research with (1) exact original record/field, (2) mechanism carrying an authentic missing coupon or final caption, (3) deterministic reduction, (4) discriminating falsification, (5) unchanged commitment verification. The local export is expressly trimmed and unverified for printer bytes. Avoid repeating completed negative scans solely for larger candidate counts.

## Next
Review latest mail/broadcast only if new. If a fresh source-grounded mechanism emerges, falsify it locally first; otherwise preserve six verified and explicitly unresolved two. Personal memory checkpoints should note no new accepted component rather than inflate activity.

## Verified bounded continuation (18 October 02:23 UTC)

Completed Agent 3's previously pending nine unaligned four-byte replacement offsets of K04 source-selected component, using all `2^32` alternatives at offsets 1,2,3,5,6,7,9,10,11. **38,654,705,664 assignments, zero original-target matches.** The local OpenSSL one-block C implementation validated exact SHA-256 matching at all 13 offsets using known original candidate synthetic-hash controls, and each search process had a complete NO_MATCH result. SHA of local C source: `f3694a26b026706d5f616aa03e5c847d3ad784c3fc103639f09d633660ef3395`; local summary SHA: `e632d1ce8b91a37f53cace7279cc21c826d0d8a3df43d32e7abccf97528cc492`. Machine-readable outputs retained in current invocation `/mnt/data/h17_k04_burst4/`.

Committed [new detailed completion report](../../results/h17-k04-unaligned-fourbyte-bound.md) and updated [prior aligned report](../../results/h17-k04-wordscan-bound.md) to close its unfinished continuation. All 13 possible contiguous four-byte replacement windows now excluded in the stated model: 55,834,574,848 assignments including Agent 3's prior aligned four offsets. **Do not promote as physical corruption evidence**: source never says a four-byte window was damaged, and there is no recovered K04. No change to six-slot candidate or K08.

Also ran a narrow one-token insert/delete/replace K08 draft/Emily-note source-vocabulary probe (76,727 assignments), zero hits; it lacks authoritative final-wording mechanism and is intentionally not published. Tested straightforward unkeyed hashes of spool job IDs/formats and all-source-row aggregations for K04; no match, no evidence of those source mechanisms, not published.

Next priority should again be genuine original-source provenance or an identifiable historical transformation, not another arbitrary exhaustive mutation family.
