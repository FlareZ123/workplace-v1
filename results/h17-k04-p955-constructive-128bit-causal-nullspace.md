# K04: constructive 128-bit causal nullspace at original source-consistent index955

**Agent 29, 20 October 2026 ~00:22 Dublin / 19 October 23:22 UTC.** This is a **new target-first algebraic certificate** for an earlier reported negative observation, not a newly recovered K04 bit or an authenticated historical MT producer. Reproducer: [`agents/agent29/k04_p955_causal_128bit_sft.py`](../agents/agent29/k04_p955_causal_128bit_sft.py). It consumes the unchanged 43-member case ZIP and [Agent 11's genuinely original-source GF(2)-consistent index955 chronology](h17-k04-source-consistent-index955.json). It does not use selected row129 payload values, K04 route/mask, K08 nonce, acceptance commitments or the original verifier.

## New question

Agent11 and Agent33 already established that a **particular all-intact-source-consistent chronology** leaves the four selected K04 words at full rank128 modulo the 528 intact printer words. Can one construct **128 individually specified initial-state perturbations** that change the selected payload while provably leaving *all* intact printer payloads unchanged, without rerunning a 16,896-equation GF(2) elimination? That would expose precise positions a genuinely new source would have to witness to crack the target.

Yes, for that conditional source-consistent **p=955** chronology. This result is a **constructive explanation and new three-gap ancestor map** for the previously reported 128-dimensional quotient, and is not independent evidence of another historical chronology.

## Original source coordinates, no target-byte inference

The [existing fixture](h17-k04-source-consistent-index955.json) has intact row43 at indices328..331 and row44 at339..342; row96 at721..724 and row97 at733..736; row12 at99..102 and row13 at112..115. Selected row129 starts at `p=955`, followed by original intact row130 at959. All intact original printer words, including rows130..132, end by index970. The source spool SHA256 is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.

Let `X[t]` denote untempered MT words, with the standard recurrence

`X[t+624] = X[t+397] XOR twist(X[t],X[t+1])`.

Three critical **unobserved** intervals in this particular original-source index assignment are:

| Location | State index | Historical spool gap |
|---|---:|---|
| Early two-hop donor | `X[104]` | row12→13 |
| Immediate predecessor block | `X[332..335]` | row43→44 |
| Middle donor | `X[728]` (and neighboring middle words) | row96→97 |

No source-derived full printer output is observed in these exact gaps under the published model.

## Explicit 128-direction construction

Consider any unrestricted 624-word initial MT state consistent with the original intact payloads under the fixture. Modify only the following **unobserved early state bits**, and regenerate later MT words. Since `332..335 <397`, these first-cycle words cannot enter an earlier nonnegative-index recurrence as middle operands. Since the latest intact printer index is970 and `p+227=1182`, downstream influence of selected words through a future middle operand is outside the surviving printer horizon.

1. Flip each of the **31 low bits** of `X[332]`, `X[333]`, `X[334]`, and `X[335]`. These 124 independent inputs alter only the corresponding `X[955..958]` target word and their hidden source word before the intact horizon.
2. Flip the **high bit** of `X[332]`, `X[333]`, or `X[334]`. Each of these three independent inputs alters `X[956]`, `X[957]`, or `X[958]`, respectively, plus its hidden initial word. The high bit of `X[335]` is deliberately *not* free: it also alters intact row130's `X[959]`.
3. Flip the **high bit of `X[104]`**. This previously unarticulated target-specific **two-hop direction** changes `X[104] → X[728] → X[955]`, and no other word before the intact horizon. Its target change is complementary to the 31 low-bit directions from `X[332]`; together the 32 inputs span every bit of the first selected word.

The last step follows by applying the recurrence at `t=104` (creating `X[728]`) and at `t=331` (using `X[728]` as middle input to `X[955]`). The MT twist mapping from a predecessor high bit and successor low31 bits to its 32-bit output is invertible. Thus the specified 124+3+1 perturbations have **rank128 across the selected four 32-bit words**. Each preserves every one of the 528 original intact printer words by support location alone, independently of their numeric values.

The code performs all 128 forward-recurrence perturbations for two independently generated unrestricted starting states, checks the **entire source-index horizon 0..970** after each perturbation, asserts no original intact word changes, confirms **rank128**, and explicitly shows the excluded `X[335]` high-bit perturbation would change the known row130 word at959. Both synthetic states passed. The earlier Agent11 fixture supplies an original-data-consistent base state existentially; linearity transports this perturbation certificate to that base without needing to know its seed.

## Stronger source-only theorem: the same 128-direction cut holds over the entire bounded target window

The p=955 construction is a special case of a **uniform source-geometry argument**. For *any* chronology obeying the original two tail MT groups, the source-derived minimum spacing, and the published bounded index window, write `p=s129`, `d=s44-s43`, and `delta=p-s43`. The published source-based conditional ranges are `945 <= p <= 955`, `11 <= d <= 65`, and `627 <= delta <= d+616`. The original observed MT group offsets give `s12=s43-229`, `s13=s44-227`, `s96=s43+393`, `s97=s44+394`, and `s132=s45+621`.

The original tail equalities imply `g44=g97` for `g_r=s[r+1]-s[r]-4`, and `g131=g97-3>=0`. The original 97..131 interval has a total skip budget 94, hence `3 <= g97 <=94`. Therefore all retained later printer output indices satisfy

`s132+3-p <= d+g97+1 <=160 <227`.

The same first-cycle **three hidden ancestor windows** exist for every placement in these ranges:

- `u=p-851` lies strictly between intact rows12 and13.
- `q..q+3=(p-623)..(p-620)` lies strictly between intact rows43 and44.
- `m..m+3=(p-227)..(p-224)` lies strictly between intact rows96 and97.

Additionally `u<=104<397` and `q+3<=335<397`, so no other previous positive-index MT middle operand can carry these directions into intact observations. The same 124 lowbit + 3 highbit + 1 two-hop highbit perturbation basis changes exactly the selected four words and hidden gaps. It leaves **all other intact printer payload words unchanged** for **any complete chronology satisfying these bounds**, as their last observed index is less than `p+227`.

The updated SFT performs an exhaustive arithmetic placement check on all **16,940** triples `(p,d,delta)` in these bounded ranges and checks the two extremal possible `g97` values. The full 128-bit perturbation/rank test is separately performed on the published original-source-consistent index955 fixture with two synthetic starting states. The universal conclusion follows from the displayed index inequalities and the MT recurrence, rather than claiming to have constructed and checked full 133-row original-data fixtures for each of 16,940 options.

**Result:** for the stated conditional common-MT, unrestricted-state and p/d bounded chronology model, **no placement of intact printer payloads alone can decrease K04's 128-dimensional quotient**. This is a new structural strengthening of the earlier result, which explicitly left open whether a different feasible chronology might fix a bit. The theorem does **not** exclude independent new donor records, additional metadata sampler constraints, a restrictive generator seed law, a chronology outside the published bounds, or a non-MT historical producer.

## Research interpretation, limits and cracking gate

**No genuine coupon bits have been recovered.** This provides an exact, source-geometry-specific mathematical certificate that intact full-word printer payloads alone cannot distinguish the 128 selected-bit directions, adding a causal interpretation to Agent33's existing rank128 output. It does **not** establish that index955 is the true producer chronology, that the selected ACK was actually produced from this MT state, or that all 128 directions remain free after imposing extra *conditional* CLASS/DEST rejection-sampler metadata or a restrictive nonlinear seed-initialization law. It does not claim universal full-source nonidentifiability for every chronology.

The **new target-facing source requirement** is sharper than simply “more MT constraints”: a potentially informative independent carrier must reach `X[104]`, the target-side immediate/middle donor gaps `X[332..335]` / `X[728..731]`, or a downstream output at **index1182 or later** where the target can first influence a new nonselected recurrence result. A new ordinary intact printer or external control *before* that future causal horizon and *outside the listed hidden windows* cannot observe these 128 directions in the stated model, however much it raises aggregate source rank. This is a **necessary observability filter**, not a claim that one such witness is sufficient to identify all target bytes.

For follow-up, test any new originally indexed external source observation against the 128 perturbation vectors **before** fitting another global index model or consulting the K04 digest. A successful original witness must collapse at least one of these nullspace directions, then predict a held-out intact source value independent of the disputed row129. This prioritizes genuine candidate-byte cracking instead of repeating conditional chronology exclusions.

**Unchanged acceptance:** six established slots PASS; K04/K08 missing, combined incomplete, `accepted: false`. K08's exact final caption is still not quoted in the retained source.
