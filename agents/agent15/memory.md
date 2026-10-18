# Agent 15 continuity: H-17 byte-carrier audit and evidence-preserving submission

Invocation mode selected by an **actual** uniform cryptographic draw: 2 (normal mode). Increased top-level COUNTER from 19 to 20. Claimed previously empty agent15 identity with run ID `8579d788-5d26-47c2-884f-107b3f398c3d` at **2026-10-18T00:04:22.368441Z** by successfully pushed `agents/agent15/.lease.json`; fetched lease to verify ownership. Original claim timestamp is immutable and must be used in the >=70-minute release check.

## Reproduced baseline

Local input `/mnt/data/c-energy-group-documents2026.zip` contains 43 original members, ZIP SHA-256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`. Read `START_HERE.md`, custodian note, route sheet, acceptance, all relevant mail, spool, crew note and previous shared research. Executed the original `verify.py` evaluation directly from the archive, and separately ran the untouched script from an invocation-local package: K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false. Exit code 1 is expected for an unaccepted complete/partial candidate.

K04: incident-date ESC-N route PS-261003-0417 last ACK attempt 2 payload `A9A9DC5731A5E2AE879C47215C2559D5`, XOR original mask `8556C8CB6140A7F9A5123AC7571BEE1C` yields `2CFF149C50E54557228E7DE60B3EB7C9`, SHA-256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`, NO_MATCH original K04. K08 no authenticated final quote in notes/mail. All earlier extensive attempts documented in results README already constrain various mutation/text-grammar classes. Do not promote unproven guesses.

## Added narrow new evidence

Audited *all 42 UTF-8 members* at the byte-level for hidden Unicode/control/formatting carriers, motivated by missing K08 desk-margin wording. Only non-ASCII text char is U+2014 in START_HERE title; 11 form feeds U+000C in 12-section RC-17 scans are expected page separators. Zero other non-LF ASCII control bytes, trailing-space/tab lines, or BOMs; detection positive controls cover U+200B, tab, trailing whitespace and BOM. Published **`results/check_h17_text_controls.py`** and **`results/h17-text-control-carrier-audit.md`**. This closes only the explicitly stated raw-character carrier classes, not acrostics or missing words.

Brief exploratory check of hash outputs from canonical `PS-261003-0300` job/time/index identifiers failed to match the first filler payload; no evidence of such a payload-generating rule, no report or conclusion promoted from this probe. Existing agent1 also probed a narrow set of PRNG seeds. Do not scale unguided hash/PRNG speculation without a source-grounded predictor and positive controls.

## User-facing reproducible package

Produced invocation-local `/mnt/data/h17_recovery_submission.zip`, containing exact original archive, original `verify.py` and `acceptance.json`, six-slot `candidate.json`, `verification.json`, and `derivation.md`. Verified ZIP CRCs, original archive byte equality, and ran original script on the packaged candidate. This sandbox path is **not** persistent across invocations, so source of truth for agents remains repo results. Files were staged atomically under a lock.

## Research priorities and constraint

Original `START_HERE.md` permits only local evidence; no external person/device contact. Critic's 23:56 17-Oct evidence-first gate warns against indiscriminate hash sweeps, and repo maintainer's claim of solvability cannot alone justify inventing source bytes. Prioritize a reproducible local source-backed relation yielding a positive K04 coupon or exact K08 phrase. Preserve unchanged commitments/verifier and distinguish any hypothetical acceptance from original evidence provenance.

At every checkpoint, obtain actual UTC runtime clock and compare against immutable `claimed_at`. Under 70 min, continue productive investigation. At >=70 min, preserve all state, push, then delete lease as final pushed operation and exit.

## Subsequent source-cohort investigation and shared synthesis

The original 133-line printer reconstruction splits exactly into 128 regular 5-minute job entries (0300..0427) timestamped with `+00:00`, plus five later RECOVER tail entries timestamped `Z`. Job/attempt pair `PS-261003-0417 / 1` collides across 16:45 LABEL/ACK and 18:01 RECOVER/REQUESTED; distinct serialization cohorts and reused identifiers are *observed*, provenance/corruption mechanism remains unknown. Unique selected K04 RECOVER/ACK attempt 2 still fails. Published `results/check_h17_spool_cohorts.py`, `results/h17-spool-cohort-identity-audit.md`, and one broadcast `communications/broadcast/2026-10-18T0020Z_agent15-spool-cohorts.md`. Updated main `results/README.md` with links to both new reports.

Brief local source-structure hypothesis test: the 128 regular row labels contain 9 observed CLASS/DEST pairs; exhaustively assigned each pair a binary bit (excluding all-zero/all-one) and packed the 128 rows with four reversal options, both raw/direct and original mask-XOR variants (8,160 K04 commitment checks). Zero matches. This is a bounded exploratory test of a binary side-carrier, *not* a source-supported original coupon derivation; do not promote it as a general result or exclude other unrelated encodings.
