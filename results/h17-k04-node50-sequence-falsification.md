# K04: original printer full words falsify the proposed consecutive node50 recorder stream

**Agent 38, 19 October 2026 ~09:50 UTC.** This is a source-derived computational *falsifier* of the new 72-consecutive-control-word premise in [Agent11's node50 report](h17-k04-node50-sequence-bridge.md). It does **not** disprove the original seq70 **low-31** individual cross-source fingerprint, nor recover K04/K08. The original selected row129, K04 mask, original REC8 commitments and desk nonce are never accessed.

## Independent original-source target words

Agent11's proposed model places recorder node50 control sequence `j` at common untempered MT output index `s7-463+j` where `s7` is the first output of printer row7. It assumes that all 72 CRC-valid, uniquely numbered node50 controls are *consecutive* MT outputs in sequence order.

Two smaller correspondences are already documented and retained in this test:

1. **Printer-only full 32-bit witness:** `row121.word3 = row91.word3 XOR twist(row38.word0, row38.word1)`. This direct untempered equality fixes `s91-s38=394`, `s121-s38=621` under the common MT witness model.
2. **Earlier isolated recorder anchor:** `inverse_twist(row7.word3 XOR row38.word0).low31 = node50_seq70.low31`. Under the same-stream assumption it places `s38-s7=230`. This condition uses only seq70, **no assumption that seq67/68/69 are successive**.

Thus, *inside Agent11's own phase model*, printer row91 begins at `s7+624` and row121 begins at `s7+851`. Their three original paired intact words at columns 0,1,2 provide exact 227-separated inverse twists:

`M[j] = inverse_twist(row91.word[j] XOR row121.word[j])`.

They directly reconstruct independently held-out, fully specified hidden stream words:

- `X[s7+228] = (M[0] & 0x7fffffff) | (M[1] & 0x80000000) = E18DCD4D`.
- `X[s7+229] = (M[1] & 0x7fffffff) | (M[2] & 0x80000000) = 820D840E`.

This deduction uses original intact printer rows 91 and121, plus the already established row38/row7 alignment. It makes **no use of node50 seq67, seq68 or seq69 control bytes**.

## Fresh predictions and exact contradiction

Under Agent11's extended 72-word consecutive assumption, MT recurrence instead demands

`X[s7+227+j] = X[s7+j] XOR twist(node50_seq[66+j], node50_seq[67+j])`, `j=0,1,2,3`.

Applying this to the original spool and all CRC-valid node50 controls produces:

| Unobserved MT output relative to row7 | Printer-only predecessor recovery | Consecutive node50 prediction | Different bits |
| --- | --- | --- | ---: |
| **+228** (`j=1`) | `E18DCD4D` | `7BEE882D` | **13/32** |
| **+229** (`j=2`) | `820D840E` | `F1522284` | **18/32** |
| **+230** (`j=3`) | Original row38 first word `344442FC` | `344442FC` | 0/32 |

Thus two *fully printer-determined* words disagree with the purported node50 block in **31 of their 64 bits**. The +230 equality remains true; it principally reflects the original seq70 anchor. This identifies exactly why checking that row7/38 link and metadata top2/top3 bits can look promising while wrongly extrapolating to all 72 controls.

The seq68/69-predicted +229 word `F1522284` coincidentally still tempers to CLASS upper3=2, agreeing with the row38 RECOVER label. But the full original reconstructed word is `820D840E`, also with upper3=2. **A three-bit label match did not validate the 32-bit hidden word.**

## Stronger research disposition

The [self-contained read-only reproducer](../agents/agent38/k04_node50_sequence_contradiction.py) SHA-pins both unchanged case-source members and verifies TRP2 record CRCs. It includes a separate synthetic CPython `random.Random` experiment with **72 actually contiguous MT outputs**, which passes the *same* inverse-twist reconstruction and all predictions. The original contradiction is therefore specific to the source/model combination, with correctly ordered MT arithmetic.

**Reject the full 72-word contiguous source-block assumption** in joint seed/state reconstruction or first-cycle origin floors. In particular, the conditional `s7>=463` bound and further inferred `s0>=371/377` from treating seq0..71 as a complete earlier MT stream are *unsupported by that falsified premise*. Preserve the original one-control seq70 low31 fingerprint and Agent11's computed metadata codes as observations under their narrower hypotheses; avoid asserting continuity or a 2,304-bit usable MT prefix.

This is an exact incompatibility **conditional on the earlier seq70 MT alignment and original printer witness interpretation**. It is not a claim about real facility RNG usage. The recorder timestamps independently challenge chronological physical common-stream generation. K04 target bits and K08 original wording remain unresolved; original REC8 accepted six slots and combined incomplete state are unchanged.
