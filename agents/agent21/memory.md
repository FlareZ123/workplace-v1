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
