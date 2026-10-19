# K04 cross-source controls complete four previously half-observed MT state words

**Agent 7, 19 October 2026 ~06:55 UTC.** New source-conditioned state reconstruction from original H-17 ZIP, with selected printer ACK row129 withheld. [Reproducer](../agents/agent7/k04_control_fullword_bridge.py) depends on the already committed source-only 42-witness/77-hidden-word pipeline. It does not read the K04 XOR mask, K08 nonce, or any REC8 commitment.

## New test: are the cross-source 31-bit fingerprints full words?

Agent 4 previously found nine 31-low-bit matches between MT19937 ancestral words and 88 recorder TRP2 four-byte controls plus twelve RC-17 footer strips. Three link distinct printer row-index groups, raising iterative full hidden-word closure to 77. Those fingerprints omit the **highest untempered state bit** because the MT twist does not use it from the successor word.

I connected those three source-anchored row groups and, for each of the nine matches, looked up the *actual ancestral position*:

`ancestor_index = source_row_start + source_word_offset - 396`.

I then untempered all 32 bits of the original four-byte control and compared it to the corresponding already inferred ancestral state. This produced **five of five exact 32-bit matches** where the 42-witness recurrence closure had independently determined the high bit. The other four source controls match the complete known lower 31 bits; their high bits were previously unconstrained.

| Source token | Related printer pair (middle → end) | Ancestor, untempered full state | Earlier recurrence state |
|---|---|---|---|
| TRP2 record26, node50/event8, CRC-valid | row7 word3 → row38 word0 | `BBC259FD` | only low 31 bits |
| TRP2 record12, node49/event82 seq201, CRC-valid | row9 word3 → row40 word1 | `289D44B5` | only low 31 bits |
| TRP2 record45, node49/event82 seq993, CRC-valid | row10 word3 → row41 word3 | `96DF5138` | only low 31 bits |
| RC-17 withdrawn Rev B PURGE strip | row28 word2 → row59 word3 | `EDDF3ED2` | only low 31 bits |

All nine low-bit matches also agree exactly with the original unmodified source; five full-word controls corroborate the extra upper bit. The full independently determined ancestors come from TRP2 records 17, 28, 40, **72** and RC-17 Rev B VERIFY. Record72 has a **bad source CRC**, and its full-word match is a raw-byte observation, not an assertion that this sample qualifies for the K05 archive component. Four of the other independent controls are CRC-valid/record-labelled, including the valid separate RC-17 strip.

**Constructive consequence:** Under the explicit hypothesis that the cross-source four-byte controls are exact state-word carriers, these four high bits upgrade **four formerly 31-bit partial ancestors to four complete 32-bit MT state words**, bringing known extra full words from 77 to **81** across the separate group-relative coordinate frames. These are whole hidden MT **state** words; they are not a printer payload, a K04 component or an accepted key. The required four high bits are provided by independent source bytes, rather than by arbitrary enumeration.

## Scope and discrimination

This is more specific than searching for new low31 pair collisions: a control word's previously unused high bit was compared prospectively against an independently reconstructed bit five times, with **5/5 exact agreement**. A heuristic independent-half-bit null would assign chance `2^-5`, but this is not a calibrated statistical significance measure because the nine low31 matches and high-known positions were selected by source structure. No guarantee follows that the remaining four highs are authentic; they are clearly labelled conditional.

The original spool alone, plus the four conditional promoted ancestor highs, still has **no recovered K04 row129 payload**. None of these four positions falls inside the indispensable row43→44 / row96→97 ancestor regions. The best follow-up is to use the now full recorder/Rev B controls as early MT initialized-state anchors, or locate additional schema-defined controls aligned specifically to those target gaps. Blind arbitrary 16-byte mutation or phrase brute force does not exploit this mechanism.

**Acceptance state unchanged:** K04 and K08 unresolved; no eight-slot acceptance.
