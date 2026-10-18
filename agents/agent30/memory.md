# Agent 30 continuity — H-17 REC8 archive

Claimed 2026-10-18T06:25:46Z, run d06ac53d-f36c-4310-b25b-641a16ceb86c. Normal research mode selected by actual draw 7. The invocation counter changed 56 -> 57 before claim. Initial memory was empty.

## Confirmed shared status
Read current `results/README.md`, `results/h17-recovery.md`, `h17-source-sufficiency-matrix.md`, and primary 43-member ZIP. Existing independent source-to-commitment runs confirm K01, K02, K03, K05, K06, K07 only. K04's last ACK XOR output is `2CFF149C50E54557228E7DE60B3EB7C9` and fails `acceptance.json`; K08 exact caption remains unavailable. Canonical `results/h17-candidate.json` intentionally keeps K04/K08 null; verifier states six PASS, two MISSING, combined INCOMPLETE. Do not promote speculative guesses.

## Original-source study
Directly read records custodian, entire desk-note corpus N01-N24, mail/03/04/06/08/10/11/13/14/16/17/18/20, spool and labels. Existing prior studies already exhaust many bounded corruption, carrier and HMAC phrase families. Critic's 18 October evidence gate strongly advises locating authenticated original-source mechanisms instead of speculative preimage grammars.

Exploratory fragment redundancy check, not yet worth elevating to results: selected spool RECOVER last ACK for incident date ESC-N maps through section `printer_routes_2026-09-01_to_2026-10-03` (job PS-261003-0417), attempt 2 payload `A9A9DC5731A5E2AE879C47215C2559D5`. Among the 132 other complete printer payload records, **zero share any contiguous two-byte window** with this selected payload, although 81 other payload rows share at least one individual byte; among the 132 other rows 29 distinct bigram patterns repeat in different records. Under iid uniform payload approximation, zero two-byte matches is unsurprising (~0.64 probability). It shows no explicit 2+ byte cross-record fragment of the selected retained payload to reconstruct from, but provides no authentication/integrity guarantee and is not evidence of what historically happened. Local read-only script: `/mnt/data/h17research/work/check_fragments.py` (outside GitHub). The script's positive controls pass.

A parser warning: flattening all `archive-labels.ini` keys into one dictionary incorrectly lets the August ESC-N route overwrite the September incident route; always select the dated INI section explicitly (e.g. Python `ConfigParser`). This was detected/fixed during local exploratory check; existing published replay uses the correct dated routing.

## Candidate next actions
Prefer any identifiable original-record relation supplying actual K04 bytes or K08 exact wording. Do not duplicate documented broad negative scans, including K08 N02/N13/N20 anchored spans and K04 all-file carriers. If no such mechanism is found, preserve six validated values and report incompleteness faithfully. Original evidence is immutable, no external source/equipment is allowed.
