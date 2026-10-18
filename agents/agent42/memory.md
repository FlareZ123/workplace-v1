# Agent 42: H-17 recovery continuity

Claimed 2026-10-18 07:46:27Z, normal mode, RNG draw 3, no Work mode. Reviewed original 43-member ZIP, all mail, route, desk notes, spool and key source reports. Unmodified original verifier locally confirms K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false.

K04 last ACK RECOVER job PS-261003-0417 attempt 2 payload A9A9DC5731A5E2AE879C47215C2559D5, mask 8556C8CB6140A7F9A5123AC7571BEE1C yields 2CFF149C50E54557228E7DE60B3EB7C9; original acceptance rejects. Source layer remains unauthenticated. K08 final words not quoted. No new component found.

Fixed stale K04 lower-bound figures in results/h17-k04-multiple-source-ambiguity.md, commit 451ecea: four changed byte positions, five changed nibbles, seven changed bits, byte-span at least five positions. Algebraic bounds only, no printer diagnosis.

User-side reproducible handoff: /mnt/data/H17_recovery_handoff.zip with unchanged original verifier, evidence, candidate, verification.json, derivation notes. ZIP and original checker validated.

Next: Seek original source evidence or a documented local transformation proving the authentic K04 coupon/mask and K08 exact caption; follow evidence-first gate in README and relevant Critic broadcasts. Avoid unguided phrase and mutation enumeration or redundant six-slot replay.

## Enhanced archival handoff

Repacked the same user-visible `/mnt/data/H17_recovery_handoff.zip` atomically under a file lock with 51 members. The original 43 exported members are byte-identical; additionally bundled byte-for-byte `original_export.zip`, a complete per-member SHA-256 manifest, `work/verify_preservation.py` to cross-check original ZIP/member hashes and original `verify.evaluate` against recorded output, and `work/validate_missing.py` for original-target K04 coupon and K08 caption tests. SHA-256 of final handoff: `9315b6a1826c2c7f80d4399ef67e58e54539f899a4eb92c703185d18f3dbdead`. Fresh extraction passed ZIP CRC, complete 43-member preservation check, six-slot unchanged verifier reproduction, and known-negative K04/K08 examples. These are custodial support tools, not original data recovery.
