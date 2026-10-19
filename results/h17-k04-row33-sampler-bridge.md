# K04: new row33→34 metadata bridge yields three MT words and predicts row86 CLASS

**Agent 30, 19 October 2026 ~07:25 UTC.** A new conditional, source-only K04 cracking advance. Reproducer: [`agents/agent30/k04_row33_sampler_bridge.py`](../agents/agent30/k04_row33_sampler_bridge.py). The selected spool ACK row129, masked K04 component, REC8 acceptance commitments and K08 HMAC are excluded from the algorithm. Original printer spool SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. No K04 value is claimed.

## Source-visible anchor and independent inference

The existing 42 source-pinned MT19937 recurrence witnesses split row33 and row34 into distinct position groups. Reconstructing their hidden generator states separately shows **two consecutive full 32-bit MT states** immediately preceding row34's four-word payload. Tempering them gives respectively:

- first output: `A757A2AC` (untempered), `80636C40` (tempered), top **two** bits = **2**, matching intact row33 `DEST=bench`;
- next output: `56FC62AE` (untempered), `097AAF7C` (tempered), top **three** bits = **0**, matching intact row34 `CLASS=LABEL`.

Under the precisely stated conditional producer model, row33 consumes its post-payload DEST sample then row34 consumes its pre-payload CLASS sample with **no other MT draws** between them. Both values are accepted by the empirically identified two-bit DEST / three-bit CLASS selectors. That hypothesis gives `s34-s33=6` and joins the previously disconnected output-position groups, without using any selected ACK value.

## Newly inferred hidden words

Running the existing fixed-point inverse/forward MT recurrence closure on the newly joined source groups (six intact regular rows: 3,33,34,56,86,116) yields **three additional complete words** that were absent from both separate closures:

| Output index relative to s33 | Newly complete untempered MT word |
|---|---|
| -620 | `B30BF870` |
| -224 | `4C457F5B` |
| 399 | `8E4AFDB6` |

The third word has a short source-auditable identity:

```text
X[s33 + 2]   = EAD4C369   (row33 word2)
X[s33 + 3]   = 15C08363   (row33 word3)
X[s33 + 626] = 5DA20CD8   (row116 word0, after the conditional join)

X[s33 + 399] = X[s33 + 626]
               XOR twist(X[s33 + 2], X[s33 + 3])
             = 8E4AFDB6

temper(8E4AFDB6) = 235768BC
top-three-bit index = 1
```

**Independent original-source field prediction:** row86's first payload is at `s33+400`; the inferred word at `s33+399` is its immediately preceding CLASS selector, and its index **1** predicts `STORES`. Original unmodified spool row86 (`PS-261003-0386`) indeed records **`CLASS=STORES`**. That CLASS metadata was not used in fitting the row33→34 bridge or deriving the new word. This is a fresh source-field prediction, separate from Agent39's earlier row80→81 bridge and its row111 destination prediction.

## Scope, caution and actionable follow-up

The two metadata samples are reconstructed in row34's preexisting right-hand state group; the `s34-s33=6` alignment remains an **assumption** (zero unrelated draws), not an authenticated original printer source-code fact. The row86 field is one three-bit observation with a three-way allowed outcome, and was found after screening candidate boundaries; do not promote it to an unconditional K04 recovery or overstate statistical confidence.

This merge does **not** yet contain selected row129 and does not alter the known K04 target index interval. It reveals a previously disjoint six-row phase group and, notably, a new 624-output predecessor word at `s33-620`. That group is a concrete additional input to cycle-aware seed/state inversion, especially work that uses independent TRP2/RC17 source controls. Re-test the join using additional wholly withheld source metadata or a seed/state prediction before escalating it to a fixed historical stream alignment.

**Status:** K04 and K08 unresolved; original eight-component REC8 acceptance remains incomplete. Original documents, masked component and verifier unchanged.


## Follow-on: three expanded 227-separated MT pair runs and a first-cycle seed attack (~07:34 UTC)

This bridge has a stronger consequence than the three state words alone. Before merging the row33 and row34 groups, the right-hand group had three runs of 227-separated MT state-word pairs of lengths **5,4,4**, at old relative positions `-229, 167, 394`. Under `s34-s33=6`, the merged six-row group has three runs of lengths **6,5,5**, now at relative-to-s33 starts **-224, 172, 399**. Each newly reconstructed full word extends one complete run by one pair. Direct source-only detection is preserved in [`agents/agent30/k04_extended_seed_windows.py`](../agents/agent30/k04_extended_seed_windows.py).

Six adjacent 227-separated full output pairs invert to five consecutive initialized first-cycle MT state words, determining **three consecutive 32-bit CPython `init_by_array` numeric seed words** algebraically. This permits a new shifted-origin test beyond Agent48's earlier 32-/64-bit all-phase scan:

- **96-bit / three-word numeric seed, row3 six-pair run wholly in initial 624-output cycle:** every possible phase `p=0..391` was inverted to a full seed and independently run through `random.Random(seed)`. **Zero of 392 candidate phase assignments reproduced the six recorded source pairs**. This exclusion allows an arbitrary pre-spool prefix and does not assume the printer began at output0.
- **128-bit / four-word numeric seed, row3 six-pair run and row10 four-pair run both first-cycle:** source-only 42-witness inequalities give `35 <= q-p <= 90`. The first run has `p<=391`; the second has `q<=393`. The algebraic fragment intersection completed **4,662 four-word seed assignments**, and **zero** regenerated both intact original runs. No original K04 commitment or target row was consulted.

Eight synthetic end-to-end controls using actual CPython `random.Random` 96-/128-bit integer seeds at phases `p=0,125,305,350`, `q=p+35` correctly recovered the integer seeds and passed independent pair regeneration. These are model-specific source-conditioned exclusions. A 128-bit seed with row10 already in a later cycle, longer/string-entropy seeds, other RNGs and still-unresolved inter-group alignments remain open.

**K04 cracking use:** This new six-pair source run is structurally valuable to cycle-aware seed inversion and later-cycle source alignment, especially with the shifted-prefix bound `s0>=292` from original TRP2 controls. Do not treat a first-cycle exclusion as disproof of arbitrary MT19937. The conditional row33→34 bridge and all historical provenance cautions above still apply.
