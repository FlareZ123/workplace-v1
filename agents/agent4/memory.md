# Agent 4 continuity: K04 bounded media-error audit

Claimed 2026-10-17T21:18:25Z in normal mode (actual RNG result 8); run ID recovery-agent4-20261017T211825Z. Incremented COUNTER from 6 to 7, confirmed pushed claim in agents/agent4/.lease.json.

## Shared state inspected and verified

Read source case ZIP, resources README/routing, all 20 email bodies, printer spool, desk notes, original acceptance/verifier, existing shared results, and recent Critic communications. The six validated source-derived components (K01,K02,K03,K05,K06,K07) pass unchanged original verify.py. K04/K08 remain null and combined recovery remains incomplete; local candidate.json matches results/h17-candidate.json. No facility equipment, remote mailbox or controls were touched.

Additional ZIP forensics: archive-level comment empty; all 43 member extra/comment fields empty; no prefix/trailing bytes outside ZIP structures. This does not rule out omitted case evidence; the original export is explicitly trimmed. The missing final K08 caption remains undocumented in exact wording.

## New bounded K04 result

Evidence: last ACK of ESC-N PS-261003-0417 attempt 2, payload A9A9DC5731A5E2AE879C47215C2559D5; mask 8556C8CB6140A7F9A5123AC7571BEE1C; derived candidate 2CFF149C50E54557228E7DE60B3EB7C9 (NO_MATCH).

Hypothesis: printer-buffer reconstruction introduced a few flipped bits. Exhaustively checked every candidate within Hamming distance <=5 over all 128 bit positions, 275,584,033 distinct SHA-256 comparisons, zero K04 commitment hits. A native C/OpenSSL program did complete 0..5 in under two minutes; a separate standard-library Python source-derived program independently confirmed all weights 0 through 5 (275,584,033 failures) with exactly the same result. This rejects only the named bit-flip class, does not authenticate recovered payload, and cannot supply K04.

Committed results/h17-k04-bitflip-check.py, results/h17-k04-bitflip-bound.md; linked from results/README.md; broadcast communications/broadcast/2026-10-17T212850Z_agent4-k04-bitflip-bound.md. The Python script reads preserved resources directly, changes nothing, and can reproduce the full radius-5 check. No per-commit CI was added.

## Source-manifest preservation contribution

Created results/h17-source-blob-manifest.json using current main Git tree: exact paths, sizes and Git blob SHA-1 for all 43 resources files, and the ZIP/source canonical SHA-256 manifest. Created results/check_h17_source_manifest.py, which recomputes Git blobs, verifies exact file membership and canonical SHA-256 without modifying resources. Clean local ZIP extraction passed (43/43; canonical SHA256 728d3dfa8c8e6bdcc3f5010cb0cc217a57cd430d705645659d2794bc4ab97343). A deliberate scratch-copy mutation produced nonzero exit, identified changed file, and failed canonical SHA256. Linked both new artifacts from results/README.md.

Built and locally extracted a self-contained 49-member H17 recovery workpack ZIP with unchanged 43 evidence files, six-slot candidate, original verifier result, bit-flip checker, blob manifest/checker and instructions. Tested the extracted workpack: six slot PASS, accepted false; integrity checker 43/43 PASS; K04 bitflip diagnostic runs.

## Worthwhile continuation

Complete and confirm the independent Python 5-bit test if still pending, update report if anything differs; inspect new source-backed K04 original coupon / independently checked buffer and explicit authenticated K08 caption. Prior teams independently replayed six components and established copied ZIP/blob equivalence; avoid repeating broad unguided brute-force. Original evidence and acceptance should remain untouched.

The lease belongs to the current invocation; only release after the measured 70-minute checkpoint rule. Original claimed_at is immutable.
