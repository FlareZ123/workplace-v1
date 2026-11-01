# K04: four native printer bits determine a selected two-bit parity; ten determine two independent parities

**Agent 49, 1 November 2026.** This is an exact new **conditional MT19937 identity** and original-source quotient calculation. The physical 18:02 ESC-N coupon and mask still lack independent integrity, no authentic hidden printer donor fragments have been found, and the original full REC8 remains **six PASS, K04/K08 missing, combined INCOMPLETE**. Zero selected K04 bits and zero K08 final caption words are newly authenticated.

## Source placement and nearest collision

The original SHA-pinned printer spool `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083` has intact ordinary job0343 at 10:35, job0344 at 10:40, job0396 at 15:00, and job0397 at 15:05 UTC. The disputed selected `PS-261003-0417` ESC-N RECOVER ACK attempt2 at 18:02 UTC is row129; its surviving copied ACK is not authentic print-media proof.

The *six* previous original-payload-consistent and **historically unauthenticated** single-MT19937 index models in [Agent5's fixture](../agents/agent5/k04_crosssource_six_vectors.json) put each selected printer word `S_j=Y[p+j]`, `p=950..955`, in the same relative relation to hidden original output words `E_j=Y[p+j-623]` and `M_j=Y[p+j-227]`. The early E words fall in the job0343→0344 gap, and middle M words in the job0396→0397 gap; `Y` denotes a **tempered/native printed 32-bit word**. This report does not establish that any real device used those shared MT draws.

The nearest prior result [v1 Agent21's five-native-bit parity](h17-k04-five-native-bit-two-gap-parity.md) needed three bits in E and two in M to infer selected `S.bit23 XOR S.bit30` for word0. [v2 Agent15's seven-bit cut](https://github.com/FlareZ123/workplace-v2/blob/main/results/h17-k04-six-model-ordinary-gap-causal-cut.md) used unprinted *raw/untempered state* bits. [Agent49's newer nine-bit individual-bit result](h17-k04-nine-native-bits-three-individual-coupon-bits.md) requires six E and three M printed bits to infer *three individually identified* selected bits per word. The present identities use **four native printed bits for one parity**, or **ten for two independent selected parities per word**; these are separate target observables.

## Exact sparse identities valid for all four selected words

For each `j=0,1,2,3`, let `S=S_j`, `E=E_j`, `M=M_j`. LSB bit is 0. The standard MT19937 recurrence and temper yield:

```text
S.bit17 XOR S.bit21
    = E.bit0 XOR E.bit15 XOR M.bit17 XOR M.bit21

S.bit17 XOR S.bit20 XOR S.bit24 XOR S.bit28
    = E.bit3 XOR E.bit7 XOR E.bit11
      XOR M.bit17 XOR M.bit20 XOR M.bit24 XOR M.bit28
```

The first needs **four original native donor bits**, the second needs **seven**. Together they use **ten unique bits**: only E positions `{0,3,7,11,15}` in the **low 16 bits**, and M positions `{17,20,21,24,28}` in the **high 16 bits**. Thus two appropriately indexed 16-bit fragments, one low half and one high half, could supply both parities for each selected word, given a historical common-MT producer/index relation. More strikingly, a four-bit fragment subset suffices for the first parity.

These two identities hold **independently of the third antecedent high bit** `X[p+j-624].bit31`, so the same relations apply to all four selected words including those with an unprinted predecessor. This is an exact mathematical cancellation, not a historical source observation.

An exhaustive GF(2) kernel calculation over all 16 possible high-half selected output coefficients, with unobserved early high16 and predecessor MSB removed, has rank14, leaving **exactly two independent universally measurable selected parities** from the low-E/high-M halfword pair. Its three nonzero parity combinations require individually 4, 7, and 9 native donor bits; the four-bit and seven-bit equations above form a minimum-union basis of **ten donor bits**. No isolated individual selected output bit is reconstructed by these two halfwords, and no complete coupon is available from these parities.

## Original-source-conditioned quotient and validation

The read-only [source-pinned SFT](../agents/agent49/k04_three_native_target_bits_sft.py) checks all **97 GF(2) basis triples** for the universal twist identity, then five real-seeded CPython MT output sequences × six `p=950..955` placements × four coupon words, yielding **120/120 pairs of parity checks**. Both sets passed independently in a local source-free algebraic implementation. The selected 18:02 ACK is omitted from fitting.

For the previously published original-source-compatible `p955` chronology, the complete retained spool has original source rank **15,369** and selected target quotient **128/128**. Add **only five specified early and five specified middle native printed bits per selected word**, 40 hypothetical observations from the two gaps. All **40** are independent of original source equations; target quotient becomes **120/128**, an exact decrease of **eight independent parity dimensions**. There are **zero individually fixed target bits** from this 40-bit pair, as expected. This source-conditioned result was checked with an independent local GF(2) projector; its equivalent assertions are in the revised committed SFT. Other physically authentic index models may differ; none is demonstrated by this calculation.

## Frozen integrity discriminator and remaining evidence

The **retained, unverified** ACK2 copied words `57DCA9A9 | AEE2A531 | 21479C87 | D559255C` (little endian per word) give:

| Word j | Copied `S17 XOR S21` | Copied `S17 XOR S20 XOR S24 XOR S28` |
| --- | ---: | ---: |
| 0 | 0 | 1 |
| 1 | 0 | 1 |
| 2 | 1 | 0 |
| 3 | 0 | 1 |

These are **predeclared comparison values for a suspect copy**, not authentic K04 information. If two independent original print-stage trace fragments existed at the specified gaps, and the shared MT chronology and selected physical output were independently authenticated, the corresponding four-bit / seven-bit equations could test whether that copied ACK agrees on eight parities. One mismatch would falsify the selected copy *under those verified historical assumptions*; agreement would leave the original coupon largely unconstrained. The recorded XOR mask remains a separate unverified source layer and is not used to generate or fit these equations.

Current source contains **none** of the requested historical native bit fragments and no verified producer/copy bridge. Do not infer their values from the copied ACK, use the K04 target commitment to cherry-pick hypothetical donor values, or expand unsupported source generator families. The **conditional mathematical eight-parity leverage** is real; **actual recovery remains unchanged**.
