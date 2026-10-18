# Agent 50 continuity — H-17 recovery

Claimed 2026-10-18T04:36:04Z as run `records-recovery-20261018-a50` (counter incremented 45→46). This is a normal-mode invocation.

## Verified research status

The original local 43-member ZIP and repository resource set yield six accepted K slots: K01 `049AAB2E1CDE7A82CD7C60234303C91A`, K02 `0D7E3AB56FB75DA3EB0E2E06786D239E`, K03 `1384AF96E25D6ADA666209CB55E062FA`, K05 `FF8B78200A56E8586DCDA00EF01E4572`, K06 `5DBF40EE52FAAED9A536D3326CF0D95A`, K07 `93495F5E425AB8E592123DABAEB68545`. The unchanged local `verify.py` returns six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false. The repository's canonical `results/h17-candidate.json` already holds this result; avoid another duplicate replay/README edit absent changed input.

K04's source-selected spool RECOVER ACK attempt 2 XOR recorded mask produces `2CFF149C50E54557228E7DE60B3EB7C9`, whose digest `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b` fails the original K04 target. No independent payload integrity checksum. K08's original final wording is not quoted; drafts and other-envelope labels are explicitly separate, and acceptance cannot invert the caption HMAC. The custodian calls the export trimmed. No complete recovery is justified.

## Independent local experiment (exploratory, NOT recovery)

Noted a specific source relation: Emily's N10 says she revisited “the photograph after the last cup,” which plausibly points to N01 (Jason's tea/sea photograph). Tested the narrow hypothetical final-caption mechanism of exactly three contiguous 2–8-word fragments from N01 (containing sea/tea), N13 (night/mugs/window/lamp) and N20 (sea/voices/table), each exactly once in any order, separated by pairs of `[space, and, while, with]`. Source SHA-256 of notes `13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb`. Fragment counts 21,85,62; 6 permutations × 16 joiner combinations = **10,624,320 assignments**, all NO_MATCH against unchanged original K08 target. A known N02 HMAC/component value `BF889359B0303F2B2B2FD96AE841210B` was the positive computational control. Script and JSON output were computed in the local case work area (`work/k08_photo_triptych.py`). Source does **not** say Emily used a three-fragment splice, so this is a bounded encoding exploration, not a provenance finding; do not promote in canonical summary. Existing `results/k08-photo-splices.py` covered two-fragment photo/Emily note constructions and overlaps this scope partially.

## Priorities

Respect Critic's `2026-10-18T0106Z_Critic_evidence-priority-enforcement.md`: require original observed anchor, historical provenance mechanism, deterministic reduction, discriminating prediction, and untouched commitment. Seek independent source-backed exact K04 coupon bytes or K08 final wording rather than inventing repairs. Existing exhaustive K04 bitflip, retry, wordscan, byte-orientation and fragment-ordering bounds are already adequately documented. `private/` contains only `.gitkeep` according to checked shared tree. Do not use original facility systems or people; case constraints confine case-material recovery to the local export.

Local user-facing deliverable: `/mnt/data/h17_recovery_handoff.zip` has candidate.json, original verifier output and derivation notes; this is not a repository path.
