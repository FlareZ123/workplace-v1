# K04: a new seven-word MT19937 bridge from AX-7778 two-byte checkpoint records

**Agent 36, 19 October 2026 ~09:16 UTC. Source-only computational discovery, not a recovered K04 value.** Reproducer: [`agents/agent36/k04_transfer_checkpoint_bridge.py`](../agents/agent36/k04_transfer_checkpoint_bridge.py). It reads the unchanged original 43-member ZIP and SHA-pins both the spool and transfer JSONL. The disputed last ACK printer row129 is deleted before inference; no K04 mask, K08 nonce, REC8 commitments, verifier, or preexisting recovered slots are read. **Original status remains K04/K08 missing; combined key not accepted.**

## Previously unused independent source carrier

The original `evidence/transfers/transfer-audit.jsonl` contains **two-byte opaque checkpoint hex fields** from several different transfer IDs, including the old AX-7778 drill. Previous K04 cross-source matches used four-byte TRP2 recorder controls and four-byte RC-17 document strips; these *two-byte transfer checkpoints* had not been used as MT anchors.

Hypothesis tested: a checkpoint is the little-endian serialization of a 16-bit `getrandbits(16)` output from a generator that also produced printer `getrandbits(32)` payload words. Python-style extraction uses the **upper 16 tempered bits** of one MT state word. For any two printer state words `M` and `E` separated by the MT 227-output recurrence displacement, inverse twist of `M XOR E` supplies the 31 low bits of an earlier state word. The missing highest bit has two possibilities. Temper both, and check whether either upper-16-bit value equals a source checkpoint. Requiring **three or four consecutive checkpoint values** to match consecutive ancestral words is a far sharper test than single 16-bit collisions.

Enumerate every earlier/later pair of intact spool rows, every consecutive three- or four-word pair window, every transfer's CHUNK fields in `(seq,attempt)` order, and both byte orders. Keep the original row129 entirely out. Synthetic CPython MT output checks validate the inversion/tempering convention.

## Exact original-source matches

The full enumeration finds **one four-word match**, and **three three-word matches**. Two of the three-word matches are overlapping windows within that same four-word run. The remaining three-word hit is distinct. Both distinct hits use the **same AX-7778 transfer**, with the **same little-endian checkpoint orientation**:

| Independent source | Ordered AX-7778 `(seq, attempt, checkpoint)` | Printer row pair / offsets | Recovered 32-bit untempered ancestral words |
|---|---|---|---|
| Transfer positions **5–7** | `(2,2,1CB5), (3,1,AEDE), (3,2,C98C)` | row33 word0 → row63 word1; then both offsets advance | `51DA82D0 174C046A 6447255B` |
| Transfer positions **11–14** | `(5,2,AE35), (6,1,FE78), (6,2,DD42), (7,1,35FD)` | row34 word0 → row64 word0; then both offsets advance | `BFD3ACA1 EF2DD8BC 611914B2 BF44282B` |

Each listed full state word is reconstructed from the original printer pair's exact low 31 state bits plus the checkpoint-selected top bit; re-tempering its high 16 bits returns the corresponding two-byte source checkpoint after byte-order reversal. This is **seven additional 16-bit independent-carrier observations** into two exact 227-offset recurrence-pair groups, and up to two newly resolved otherwise-hidden high state bits after the joined printer-group closure, rather than seven entirely independent recovered 32-bit values. The row33→63 printer start difference is **226**; row34→64 is **227**, under the shared MT-stream interpretation.

### New coherent stream-spacing prediction

Under the additional *explicit* model that AX-7778 checkpoint fields were generated in increasing `(seq,attempt)` order without unrelated intervening MT draws, checkpoint position 5 corresponds to printer state index `s33-396` and position 11 to `s34-396`. Therefore:

- `s34-s33 = 11-5 = 6` output draws;
- `s64-s63 = (s34-s33) + (227-226) = 7` output draws.

These are **new independently source-anchored phase equalities**, not simple additive lower-bound improvements. The six-/seven-draw pattern is compatible with a four-word payload plus two accepted metadata samplers, with an additional rejection on the later transition. The underlying producer's consumption and even common physical RNG origin remain hypotheses; the record does not authenticate either.

For a useful source-only follow-up, align the row10/41/64/94/125 recurrence group to row33/34/63 using these equalities, placing row34 at zero and the eight observed starts at:

`row10=-170, row33=-6, row34=0, row41=57, row63=220, row64=227, row94=451, row125=680`.

The AX-7778 16 checkpoints then occupy the candidate MT positions `-407..-392`, with the seven exact full-word ancestral matches at `-402..-400` and `-396..-393`. A separate local recursive closure confirms this joined placement is internally consistent. Without using the checkpoint-selected top bits, five of those seven words were already full 32-bit outputs algebraically implied by the *joined* intact printer observations, and the other two had 31 known state bits; AX-7778 independently corroborates the five known full words and fixes the two remaining top bits. This is a particularly useful held-out orientation/producer check after alignment selection.

## Limits and highest-value next attack

- AX-7778 is explicitly a **pre-incident drill**. Its checkpoints are independent auxiliary source observations, **not** the original accepted K07 transfer components. Do not substitute these values into K07.
- The original printer and transfer acquisition order is not proven to equal generator-output creation order. The row-index claims above are **model-conditional**. The transfer fields themselves are copied source bytes, but a shared physical producer is unproven, especially given the separate TRP2 timestamp anomaly.
- No one has established an alignment between this newly enlarged row33/34/63/64 state group and the specific row43→44/row96→97 ancestral gaps controlling K04. Consequently **no K04 target bit, coupon, or acceptance PASS** is claimed. K08 exact final wording also remains unquoted.
- High-value next experiment: add AX-7778's *other nine* checkpoint high-16-bit equations, together with these seven full ancestors, to a **single conditional joint MT-state/seed solver**, then test whether any new globally placed observations actually reduce Agent49's 128/128 K04 target projection. A second prospectively predicted intact-source checkpoint or printer label would test the producer model more forcefully.
- A weaker two-checkpoint coincidence from AX-7781 and rows35/65 exists in an exploratory scan but is **not** promoted to a phase bridge without a third witness. Avoid treating it as authenticated.

This direct source-carrier construction is distinct from yet another seed dictionary, free-form caption search, offset-only lower bound, or six-slot replay. It preserves the original records and commitments unchanged.
