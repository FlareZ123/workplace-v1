# K08: held-out caption *recoverability* protocol (Agent 50, 19 October 2026)

**Status: challenge defined; no K08 recovery claimed.** This implements the [Critic 19 October blind-recovery request](../communications/broadcast/2026-10-19T0155Z_Critic_blind-recovery-calibration-gate.md) as one short source-model calibration, without revisiting the established six-slot replay or ranking more uncalibrated final-caption guesses.

## Original, source-grounded challenge

The preserved crew extracts include three known complete captions whose *contextual cues* also survive elsewhere: (A) the empty-bench photograph and Emily's subsequent reference to a photograph after the last cup (N01/N10), (B) Emily's first crew-board draft and the description of late-watch mutual care (N02/mail11/mail20), and (C) Emily's second desk draft, referenced conceptually by her later mugs/window/lamp prose (N06/N13). The true target of each challenge is its **exact normalized caption sentence** after the descriptor's colon, withheld from the prediction input. These are pseudo-missing captions, not the authentic missing final K08 line. N01 is Jason-authored and thus tests topical transfer rather than Emily's exact personal style; prioritize the two Emily controls.

## Mechanical input and no-look protocol

From the original preserved `evidence/crew/noticeboard-and-desk-notes.txt`, replace **only** the text after each of these complete descriptor lines with `[WITHHELD CAPTION]`:

- `For the photograph of the empty bench:` (N01)
- `First draft for the crew board:` (N02)
- `Second desk draft:` (N06)

Keep the remaining original notes in order and allow `mail/11.eml`, `mail/20.eml`, `galley-and-stores.log`, and `mail/12.eml` as non-target context. Do not read the unredacted target note lines, their previous repository transcriptions, known K08 decoy components, or original K08 verifier hash during candidate formulation. All those materials are technically accessible: **human blindness is not enforceable**. If any prediction author has previously seen the target text, identify the test as a *retrospective machine ablation*, not a blind human experiment. Mechanical generation and timestamped frozen inputs mitigate accidental target leakage but do not erase past exposure.

## Freeze-before-reveal outcome

1. Predeclare the method, allowable vocabulary, search/beam settings, random seed if any, and fixed **500-candidate maximum per hidden sentence**, without reading the targets. Emit ordered, normalized ASCII-space-only unique captions as three separate lists and commit a SHA-256 of those lists **before** scoring.
2. An independent investigator then scores exact normalized equality to each original source line (not K08's commitment), recording first-hit rank for A/B/C, top-500 exact recall (particularly B/C), and optionally word overlap. Compare with a simple copy-only baseline from nonhidden retained sentences. No hashing of the original K08 commitment is part of calibration.
3. **Go:** at least one Emily-authored control recovered *exactly* and the procedure was genuinely frozen before scoring. **Stop:** no exact Emily recovery; retire this generation rule, rather than expanding the K08 search by more fluent variants. Disclose input leakage, fidelity mismatch and small sample size either way.

**Fidelity limit:** The export has no independent detailed semantic paraphrases of N02/N06 at the same fidelity as Emily's N20 description of the actual final caption. This is an imperfect control. A miss cannot prove inference impossible in general, and a hit alone cannot supply K08's true unquoted caption. It calibrates whether one defined candidate method reconstructs any held-out exact words from this source type.

Original preserved files and the original acceptance commitments remain unchanged. Any future genuine K08 candidate still needs the untouched K08 slot hash and full REC8 acceptance if K04 is also recovered.
