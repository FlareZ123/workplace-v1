# K04: source-ordered three-carrier future-donor construction (19 Oct 2026)

**Agent 1. A new target-oriented cross-carrier candidate route, tested to its stated stop criterion. K04/K08 remain unresolved.** Reproducer: [`agents/agent1/k04_triangular_transfer_bridge.py`](../agents/agent1/k04_triangular_transfer_bridge.py). No original source, selector, commitment or verifier was modified.

## Four independently retained inputs and proposed producer mechanism

The 43-member case export includes (1) 84 CRC-valid TRP2 recorder 4-byte controls at byte offset 12 of 24-byte records, with explicit node/event/latch/sequence/timestamp labels; (2) twelve Rev B/C/D-draft RC-17 eight-hex-character footer strips and the separately specified service order; (3) the intact 16-byte printer records in `spool-reconstruction.log`; and (4) 16 two-byte CHUNK checkpoints per transfer in `transfer-audit.jsonl`, each indexed by sequence and attempt. These are genuine distinct original carrier types. Their exact SHA256 pins are enforced in the script.

Earlier K04 work identified full MT19937 printer recurrence witnesses and separate printer/recorder low31 or printer/AX checkpoint bridges. This **new combination tests three simultaneous source classes** as a prospective generator of previously unobserved MT future words. Conditional on a shared MT stream, take three source-ordered full recorder/procedure words as the MT middle donor `M[j]=X[k+397+j]`, four intact printer words as `F[j]=X[k+j]`, and the original source-ordered three AX checkpoint values as the high sixteen bits of later outputs `X[k+624+j]`. Before consulting target row129, predict each transfer checkpoint:

`prediction[j] = upper16(temper(M[j] XOR twist(F[j], F[j+1])))`, for `j=0,1,2`.

A three-checkpoint match would give a full-word/partial-word **source-indexed triple** and a falsifiable new stream-placement link. If such a link reached or independently fixed the target-side missing ancestor windows, it could reduce the 128-bit K04 ambiguity. Importantly, the documents authenticate the individual bytes and selected orderings, **not** common MT production of recorder, procedure and transfer fields. A positive would still require held-out producer/chronology validation. The original recorder timestamps can postdate printer records, so logged time must not be mistaken for draw time.

## Tested finite class and observed result

Recorder candidate ordering families: raw file order, UTC acquisition-time order, ascending sequence within node/event, and ascending sequence within node/event/latch. Procedure orderings: original scanner order and document-defined service order within each revision; withdrawn Rev B and draft D remain auxiliary source witnesses, never accepted K06 evidence. The selected K04 spool row129 is excluded outright, as are K04 mask, K08 nonce, all acceptance digests and verifier.

- **205 distinct** three-word recorder/procedure donor windows.
- **56** transfer three-checkpoint windows across four transfers, keeping original indexed `(seq, attempt)` order and little-endian checkpoint interpretation previously supported by the AX bridge.
- **132** intact nonselected printer four-word blocks.
- **27,060** derived three-high16 transfer predictions and **zero three-word matches**.
- **Zero matches even at the first two consecutive predicted high16 checkpoints** within the same source-labelled windows, a stricter early exit.
- Three independently seeded actual CPython MT output-stream positive controls satisfy the prediction identity exactly.

An independent additional pair-only route compared **4,560** unordered combinations of 84 valid recorder controls plus 12 RC-17 strips against 396 intact printer within-payload twist values, to identify full `X[k+397]` / `X[k+624]` donors. **Zero full 32-bit matches**; this was independently exercised with true MT source-word positive controls. The combinatorial donor pairs have *no* independently authenticated stream-index or temporal adjacency, so their negative result is a narrow candidate-class exclusion.

## Stop criterion and research impact

This proposal is now **closed for the exact source-ordered three-carrier hypothesis**, rather than prompting expansions of word permutations, nonce/seed guesses or conditional gap tests. Its evidence-derived predictions produced no new full original future word, no K04 selected coupon bits, and no new K08 normalized words. The source still lacks authentic target-ancestor **index placement** and original final-caption inscription. A genuinely new source could reopen the approach only if it established common producer/cache epoch and the missing source-index relation, after a held-out intact-word prediction. The original verifier remains at six PASS and K04/K08 MISSING.

This is a tested **conditional producer/candidate pathway**, not a proof that cross-source MT sharing never occurred or a recovery success.
