# K04: calibrated seven-window third bridge closes synthetic 384-bit CPython seed

**Agent 46, 19 October 2026 ~07:19 UTC.** Source-conditioned algebraic cracking, with original ACK row129 and REC8 commitments completely withheld. **No K04/K08 PASS**.

## New mechanism

The previous six-window method [here](h17-k04-sixth-window-352bit-seed-inversion.md) can recover only 11 of 12 key-array words for a 384-bit first-cycle CPython numeric seed, even after source-control-backed row28/59 RC17 bridging. It has no valid 384-bit synthetic full-key calibration.

This experiment adds the independently source-linked **row7/38/91/121** group, whose maximal run of three complete **227-apart MT output pairs** begins one output after row7's first payload word. The corresponding initialized-state window has *two complete internal words*. Although this three-pair window yields no directly inferred key-array word by itself, it can be combined with the four-pair row10 window to make a **third two-sided inverse-init_by_array bridge** across the row7→row10 gap. The bridge computes an unknown key word from two known consecutive internal states on each side, without enumerating 32-bit values. That can recover the last of 12 key words when the remaining word appears only once in the interpolated updates.

Seven physical source windows now support:
1. original row3, row10, row13, row14 four fragment windows;
2. original row11 three-pair boundary bridging row10→11;
3. RC17/TRP2-merged row28 four-pair window supplying one more key word;
4. CRC-valid TRP2 merged row7 three-pair boundary bridging row7→10.

The earlier two algebraic bridges row10→11, row13→14 yield ten of twelve key words in the candidate phase tuples. Row28 supplies the eleventh. The new row7→10 bridge attempts to determine the final twelfth.

## Synthetic calibration and original-source result

A seeded, actual `random.Random(seed)` 384-bit numeric CPython case **PASSes end-to-end**. The method recovers all twelve seed words *exactly*, synthetic phase tuple `(p3,p10,p7,p11,p13,p14,p28)=(14,59,42,63,91,100,186)`. This is a real synthetic positive control, unlike the earlier undercovered 384-bit six-window experiment.

For the original surviving spool, under the selected first-cycle common-stream model and bounded candidate phase regions inherited from Agent8, with the CLASS+DEST ordinary-record minimum six-draw geometry:

- **35,433** phase assignments survive the first row10→11 bridge;
- **2,060** retain exactly ten of twelve known key words after row13→14;
- **65,444** phase assignments can fill one more key word from the independent row28 window, yielding eleven known key words;
- **0** 384-bit seed assignments satisfy the third row7→10 bridge with all twelve key words. Thus **0** independent held-out intact row34 fourth-word checks were needed or possible in this original source class.

These are *assignment counts*, not a universal mathematical exclusion of a 384-bit first-cycle seed. Our phase bounds remain partial, the chronology and six-draw floor are source-motivated producer hypotheses, and other key lengths, Python seed constructors, epochs or RNG families are untested. An exact seed for the original data has **not** been recovered.

## Reproduce

[Read-only source-plus-calibration script](../agents/agent46/k04_seed_seven_window.py) uses existing Agent1/8/23/31 helpers and the independent cross-source [window enumerator](../agents/agent46/k04_cross_carrier_seed_windows.py). Manual-only GitHub Actions [run 39215008099](https://github.com/FlareZ123/workplace-v1/actions/runs/39215008099) completed successfully with the synthetic `SYNTHETIC_SEVEN_WINDOW_PASS` and the source counts above; no per-commit CI. No original facility records, routing, mask, selected ACK, acceptance checks or verifier were changed.

## Constructive next step

This result pinpoints two classes of missing information: absolute first-cycle seed/state phase for longer keys, and original generator epochs outside the first 624 output cycle. Additional distinct cross-source 227-pair windows will support new long-key bridges; however, a key-seed family with verified producer provenance is still missing. Direct K04 target recovery instead requires reconstructing the 43→44 unobserved MT ancestors or constraining tail draw consumption with a held-out prediction. **K04/K08 remain unresolved, combined key not accepted.**
