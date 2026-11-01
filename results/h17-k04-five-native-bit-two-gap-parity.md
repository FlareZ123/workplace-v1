# K04: five printed donor bits from two source-compatible MT gaps determine one selected-coupon parity

**Agent 21, 1 November 2026. Conditional mathematical target-leverage result, not recovered media.** Original H-17 REC8 acceptance remains six PASS; independently authenticated K04 selected 18:02 coupon bits **0/128**, Emily's exact K08 final words **0**, and combined REC8 **INCOMPLETE**. This uses neither the disputed selected payload nor the K04 acceptance digest to infer a donor relation.

## Original anchors and relation

The original SHA-256-pinned printer spool is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Intact printer row43, `PS-261003-0343` at **10:35 UTC**, has last native little-endian untempered MT word `X[p-624] = 59E4D0B9`, whose high bit is **0**. Intact row96, `PS-261003-0396` at **15:00 UTC**, precedes the second possible donor interval. The selected ESC-N / `PS-261003-0417` / RECOVER / attempt2 is the disputed **18:02 UTC** row129.

The six published, fully **payload-source-compatible** single-MT19937 index examples in `agents/agent5/k04_crosssource_six_vectors.json` have `s43=p-627, s96=p-234, s129=p` for `p=950..955`. They are **not authenticated physical printer chronologies**; other printer metadata assumptions have previously contradicted these fixed layouts.

Let `X[t]` be an untempered 32-bit MT state-output word, `Y[t]=temper(X[t])` its printed native 32-bit output, and `word.bitN` refer to bit N with LSB=0. The exact MT twist/temper algebra gives, for every valid MT state stream:

```text
Y[p].bit23 XOR Y[p].bit30
    = Y[p-623].bit16 XOR Y[p-623].bit17 XOR Y[p-623].bit24
      XOR Y[p-227].bit23 XOR Y[p-227].bit30
      XOR X[p-624].bit31
```

The final term is **0** using the actual intact row43 word. Thus one target coupon parity is determined by **five native output bits across only two latent donor words**:

- Early donor `Y[p-623]`: printed bit positions **16, 17, 24**, between `PS-0343` (10:35) and `PS-0344` (10:40).
- Middle donor `Y[p-227]`: printed bit positions **23, 30**, between `PS-0396` (15:00) and `PS-0397` (15:05).

In all six frozen placements the relative job boundaries and five bit positions are identical; only the absolute MT indices change. Both required sets lie within the **high 16 bits of their respective 32-bit printed donor words**. Two genuinely independent, historically indexed upper-16-bit output fragments would suffice for this *one parity*, provided a common MT producer and source-index mapping were authenticated. A source file that merely has two arbitrary 16-bit values is **not** an indexed witness.

The original copied K04 mask begins `8556C8CB` (little-endian first word `CBC85685`); its bits 23 and30 are both 1. Their XOR is 0, so, *if that mask is historically accurate*, the same parity would hold for the reduced K04 first word. A single parity does not recover either participating bit or the other 126 dimensions.

### Exact selected-copy falsification question

The retained **unverified** 18:02 ACK2 PAYLOAD begins `A9A9DC57`, giving native little-endian first word `57DCA9A9`. Its observed `bit23 XOR bit30 = 0`. If a future independently authenticated, precisely indexed pair of original donor upper-halfwords yields **XOR of the specified five bits = 1**, then the retained selected first-word copy is inconsistent with that authenticated producer/output chronology. Donor XOR **0** only establishes agreement on one parity; it cannot certify the other 127 coupon bits, the printed mask or the complete key. No such donor pair exists in the present export, and this conditional comparison was **not** used as an oracle to select hypothetical donor values.

## Reproducible target-information test

[Single-file read-only reproducer](../agents/agent21/k04_p955_donor17_sft.py) imports the pre-existing original-source GF(2) projector from `agents/agent33/k04_global_target_projection.py` and the original-source-compatible p955 vector from Agent5. It deletes selected row129 **before** building the basis. The untouched 132 intact payload rows give source rank **15,369** and selected target quotient **128/128**. Augmenting with five **hypothetical** donor bit values obtained from one affine state completion produces quotient **127/128** and fixes exactly `Y[p].bit23 XOR Y[p].bit30`. A hypothetical *single* donor `Y[p-227]` top-16 fragment alone gives no reduction (rank128); its top17 gives rank127 by a different two-bit parity. These are synthetic oracle evaluations, **not original observed donor values**.

The MT twist and temper are GF(2)-linear in their three predecessor words; zero input plus every one-hot bit across the three 32-bit inputs is a complete 97-vector certificate of the stated identity. **All 97/97 basis controls pass**, establishing the equality for every possible input triple. Five independent actual CPython MT19937 seeded streams at all six p indices also satisfy it, including the nonzero original-predecessor-MSB case: **30/30 synthetic controls**. The earlier v2 Agent15 [seven internal-state-bit dependency](https://github.com/FlareZ123/workplace-v2/blob/main/results/h17-k04-six-model-ordinary-gap-causal-cut.md) required unprinted untempered donor bits for four candidate parities. This result provides a different, independently testable **native-serialization five-bit / two-upper-halfword** witness condition for the first selected parity. The earlier v1 [optimistic hidden-output 16-bit oracle](h17-k04-global-optimistic-sampler-leakage-cut.md) addressed 300 *not fully source-consistent* index layouts and does not decide this frozen source-consistent p955 geometry.

### Strength of the two-gap printed-fragment oracle (p955 only)

For the same **source-compatible but historically unverified** p955 placement, reveal only the highest `k` tempered bits of each of the **two** exact gap outputs `Y332` and `Y728`. Original row129 is omitted throughout. The source-conditioned GF(2) quotient shrinks as follows; actual recorded additional donor bits remain **zero**.

| Hypothetical upper-bit fragment per word | Unknown selected first-word dimensions | Unknown entire selected 128-bit coupon dimensions |
|---:|---:|---:|
| 15 bits | 32 | 128 |
| **16 bits** | **31** | **127** |
| 17 bits | 29 | 125 |
| 24 bits | 16 | 112 |
| 31 bits | 2 | 98 |
| 32 bits | 0 | 96 |

The five-bit identity is the **one** linearly recoverable selected-word parity from the two upper-16 fragments under this geometry. Full copies of just these two outputs would fix all **32 bits of the first selected word**, while leaving the other three selected words entirely unknown. This is a target-facing quality threshold for possible *new original* printer trace fragments. It does not authenticate the hypothetical layout or imply that two old arbitrary halfword fields are equivalent to `Y332` and `Y728`.

## Admission boundary

No original record in the current export supplies these two indexed printed donor fragments, the printer's historical common-MT producer law, or an independent source confirming that the selected **physical ESC-N coupon** used this modeled stream. Ordinary CLASS/DEST categorical metadata alone does not authenticate the required full two-fragment witness, and the copied selected ACK has an independent integrity limitation. Do not relabel the hypothetical donors as original K04 bits or use the K04 commitment to select arbitrary latent traces. An independently acquired original indexed trace could test this precise parity before any complete coupon recovery; otherwise the result is a useful **conditional causal acquisition specification**, with no accepted seventh slot.
