# K04: exhaustive first-cycle 32/64-bit seed phase inversion

**Agent 38, 19 October 2026 ~09:32 UTC.** Read-only source-conditioned cracking exclusion. Original K04 coupon row129, all REC8 commitments, K04 XOR mask and K08 nonce are excluded from the search. No K04 or K08 component recovered.

## New coverage relative to the prior short-seed inversion

The existing [Agent1 initialized-state attack](h17-k04-python-initialization-inversion.md) recovered two 32-bit CPython `init_by_array` key fragments from the **five consecutive 227-separated MT word pairs** in the original printer row3 / row34 / row56 / row86 / row116 group. Its 32-/64-bit seed trial only considered source-graph-bounded early positions of the first pair, `p=14..68`, leaving most *absolute* possible first-cycle origins untreated.

A complete first-cycle run of length five requires `0 <= p` and `p+227+4 <= 623`, hence **every possible first-cycle placement is exactly `p=0..392`**. Agent3's later CRC-valid TRP2 origin floor, under a common zero-origin generator hypothesis, makes `p>=321` and leaves the 72-phase subinterval `321..392`. Both earlier small-offset and later cross-carrier-conditioned phases can be tested with exactly the same algebra. The source-derived pair words and their order remain unchanged.

The reproducer [`agents/agent38/k04_firstcycle_shortseed_fullphase.py`](../agents/agent38/k04_firstcycle_shortseed_fullphase.py) reuses the source-pinned extraction from Agent1, reconstructs a 1- or 2-word numeric seed at each `p=0..392`, and predicts the complete ten already retained paired MT outputs by an independent `random.Random(seed)` run. Two synthetic 32-/64-bit seeds deliberately placed at late phase **336** are recovered exactly and reproduce the synthetic outputs.

## Actual result

| Class | Absolute first-pair phases | Complete seed assignments | Full original-source matches |
| --- | --- | ---: | ---: |
| CPython integer seed of 1 × 32-bit word | 0..392 (393 phases) | 0 | **0** |
| CPython integer seed of 2 × 32-bit words | 0..392 (393 phases) | 393 | **0** |
| Recorder-origin-compatible first-cycle subinterval | 321..392 (72 phases, included above) | 72 for 64-bit | **0** |

One-word assignments fail the internally recovered seed-word agreement, while each two-word phase reconstructs one fully specified candidate seed which fails direct source-word prediction. Source pair construction omits row129 before any MT inference. The report does not claim independent physical generation from a printer PRNG: the MT recurrence and common origin are conditional mathematical models of retained bytes.

**New discriminator:** a 32- or 64-bit CPython integer seed whose entire row3 five-pair witness occurs in the *first* 624 untempered MT outputs is now excluded **regardless of first-cycle absolute phase**, including the recorder-linked late phases not covered by the previous bounded early phase search.

## Scope and next constructive lane

A phase `p>=393` crosses the MT twist-cycle boundary and invalidates this initialized-state pair inversion, regardless of numeric seed width. Seeds of **96 bits or longer**, bytes/text initialization, other MT implementations, independent/cached generation, or arbitrary 19,937-bit initial states are not rejected here.

The higher-value follow-up is a cycle-aware reconstruction of seeded state across row7/38's known boundary. The separate conditional `s7=394` case provides seeded `S[623]`, initial `X[0]` and control-supplied `X[1]` (Agent3 origin census). A second contiguous initialized word near `S[623]`, rather than another phase count, would permit an additional independent seed-word equation and begin to address 96+ bit seeds. The directly preceding pair at row7 relative offsets `0,227` currently has only its upper output bit reconstructed, so its remaining low31 is a concrete information bottleneck.

The untouched original acceptance state is **six PASS, K04/K08 MISSING, combined INCOMPLETE**. This report is a generator-model exclusion, not an accepted recovered component.
