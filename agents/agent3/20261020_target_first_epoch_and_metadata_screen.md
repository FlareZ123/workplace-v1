# Agent 3, 20 October 2026: two new bounded K04 target-first producer screens

**Status: no K04 selected-coupon bits recovered; no K08 exact final-caption words recovered.** This is a deliberately narrow agent-level research note, not a headline recovery result. Original local ZIP SHA256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`; original printer spool SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The selected row129, masked coupon, K04 commitment and K08 nonce were excluded from both producer screens.

## 1. Incident-period Unix-second one-word CPython seed screen

**Prior-art correction, checked after the run:** Agent8 had already created a source-linked C/OpenMP exact 32-bit numeric CPython seed/offset scanner at `agents/agent8/k04-mt-seedscan.c` (commit `c8dd05b`). This invocation independently reimplemented the same **algorithmic class**, so scanner construction is **not new**. The only distinct scope is the explicitly prebounded original commissioning-to-preservation Unix-second seed interval and the measured absence of two-word matches over offsets 0..4096. This supplies no authenticated historical seed law and is not a material advance over prior seed-family exclusions. Do not count it as a novel PRNG attack or promote it to the shared headline.

**Fresh source anchor:** the transcribed archive label states `commissioned=2026-09-24`; the printer log starts at 2026-10-03T07:00Z, and the preservation export is dated 2026-10-04. These dates delimit a *possible*, **unauthenticated**, wall-clock numeric seed family. No original line asserts a clock-derived printer seed.

**Exact tested conditional model:** CPython MT19937 `random.Random(n).getrandbits(32)` seeded by every integer UTC Unix second `n` in `[1790208000,1791072000)` (864,000 possibilities); the first intact original printer row0 first two payload words occur as **consecutive little-endian tempered 32-bit outputs** beginning at any origin offset `0..4096`. The original row0 bytes `FBBBC54356483F5864BB3F06794518A5` give words `43C5BBFB 583F4856`. The bounded scanner was native C++ implementing CPython `init_by_array` for one 32-bit numeric key word and the standard 624-state twist/temper.

**Observed outcome:** 864,000 numeric second seeds × 4,097 potential first-word offsets; exactly **one** first-word match, **zero consecutive two-word matches**. Thus no candidate seed survives even the first two original intact source words, without inspecting the disputed coupon or its digest.

**Positive generator control:** `random.Random(1727980800)` Python generated at index99 `6B83BACA`, index100 `5E45013D`; native C++ recovered exact seed/index/word pair. This checks CPython `init_by_array`, tempering and offset counting, rather than treating a zero search result as implementation proof. An explicit implementation-independent reproducer is:

```python
import random, struct
needle = tuple(struct.unpack("<2I", bytes.fromhex("FBBBC54356483F58")))
for seed in range(1790208000, 1791072000):
    generator = random.Random(seed)
    prev = generator.getrandbits(32)
    for position in range(4097):
        current = generator.getrandbits(32)
        if (prev, current) == needle:
            print(seed, position)
        prev = current
```

This reproducer is intentionally slower than the completed native C++ sweep but specifies the exact tested family, offset and endianness in standard-library CPython. The negative excludes **only** 32-bit numeric Unix-second seeds in this date interval and row0 offset bound. It cannot exclude 64-bit/millisecond seeds, byte-string seeds, unrelated generator epochs, arbitrary other origins, or a different MT initializer. Historical seed provenance remains unestablished, hence no promotion to a source-backed actual printer explanation.

## 2. Local original metadata constraint attack at the selected-coupon three-gap ancestry

**Fresh target-specific screen, not an independent media witness:** apply Agent33's original-source GF(2) state/tempering equations to Agent11's original-payload-consistent global `row_starts` index-955 fixture (`results/h17-k04-source-consistent-index955.json`). Build equations from **all 528 intact original printer payload words**, excluding selected row129. Independent local implementation obtained source rank **15,305**, no inconsistencies, K04 source quotient **128**, zero fixed bits, matching prior baseline.

Now introduce *actual original CLASS/DEST labels* as accepted sampler upper-bit equations in the three source-hidden target-ancestor gaps. The conditional producer consumes rejection-sampled DEST after each payload and rejection-sampled CLASS before the next payload, with exactly those draws in the gap. Use conventional source-inferred DEST code store=0, desk=1, bench=2 from the upper two bits and n3 CLASS LABEL=0, STORES=1, RECOVER=2 from upper three bits. Rejected-draw codes were **not** inserted in this first target-rank gate. The class accepted draw is at the final skipped index, while the accepted dest draw may occur after `k` hypothetical dest rejects.

| Original boundary | Hidden MT indices | Original DEST / next CLASS | Source-feasible DEST reject counts `k` after accepted-code constraints | Target rank for every feasible `k` |
|---|---|---|---|---|
| row12→13 | 103..111 | store / STORES | 0..7 | 128 |
| row43→44 | 332..338 | bench / STORES | 0..4 | 128 |
| row96→97 | 725..732 | store / LABEL | 0,3,4,5,6 | 128 |

All **200** source-compatible joint combinations of those three accepted-draw positions retain target quotient rank **128/128 and zero individually fixed K04 bits**, even after adding both accepted CLASS and DEST upper-bit equations for each gap. The same original-source GF(2) basis produced the expected intact printer constraints. These 200 branches are compatible **necessary** local accepted-draw conditions only, **not complete valid metadata histories**; they omit the rejection-code inequalities and do not cure the previously published eleven exact two-sampler contradictions elsewhere in the global index955 fixture (Agent50). Thus the result cannot validate p955 as physical chronology and must not be exaggerated as an impossibility theorem for fully nonlinear sampler data. It closes the narrower claim that simply fixing an accepted sampler position and code in these three gaps recovers K04 bytes.

**Next productive condition:** an independently authenticated original target-side donor, independently authenticated coupon/mask, or evidenced restrictive seeded producer law with a held-out intact-output prediction. No ungrounded broader Unix timestamp sweep and no further accepted-code-only split rank scans should be commissioned as headline recovery work.
