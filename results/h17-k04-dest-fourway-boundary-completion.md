# K04: at the boundary donor alignment, original DEST metadata reduces the 16-way coupon completion to four

**Agent 7, 20 October 2026, source-conditional constructive cracking step.** Read-only SFT: [`agents/agent7/k04_dest_fourway_boundary_sft.py`](../agents/agent7/k04_dest_fourway_boundary_sft.py). **Actual selected K04 bytes remain unrecovered.** This note combines the existing [Agent 8 two-window 16-candidate recurrence](h17-k04-target-leverage-constellations.md), the **previously established** ordinary post-payload [DEST sampler](h17-k04-dual-metadata-sampler.md), and [Agent 1's prior all-row DEST parity gate](h17-k04-all-row-destination-parity-target-projection.md) specifically at the earliest target ancestor geometry. The sampler, the bench first-draw MSB rule, and the observation that this earliest boundary knows a predecessor were **all prior art**. The **explicit four-candidate joint completion and seven-draw candidate filtering below** are the contribution.

## Original witness and restricted source placement

The unchanged 43-member ZIP contains the spool with SHA-256
`7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.
Original **zero-based row43** (`PS-261003-0343`) records **DEST=bench**;
row44 (`PS-261003-0344`) records **CLASS=STORES**. Both are intact ordinary jobs, not exceptional RECOVER tail rows. No selected row129 field was used.

Use the **specific conditional** common-MT chronology published as
[`h17-k04-source-consistent-index955.json`](h17-k04-source-consistent-index955.json).
There `s43=328`, `s44=339`, `s129=p=955`. Thus `p-s43=627`, the earliest target alignment:
- `X[p-624]=X[331]`, **the fourth intact row43 payload word**, already known.
- `Q=X[332..335]=X[p-623..p-620]`, first four unprinted words after row43.
- `M=X[728..731]=X[p-227..p-224]`, middle donor window between intact rows96 and97.

The MT19937 recurrence is

`X[p+j] = M[j] XOR twist(P[j],Q[j])` for `j=0..3`,
where `P=[X331,Q0,Q1,Q2]` and
`twist(a,b) = (((a&0x80000000)|(b&0x7FFFFFFF))>>1) XOR (0x9908B0DF if b is odd else 0)`.

**Hypothetically supply four original correctly indexed low31 values Q0..Q3 and four full original correctly indexed M0..M3.** The first target word becomes uniquely known because `X331` is already intact source. The remaining three words each initially have one unknown predecessor high bit. This is the earlier atlas's `16`-candidate general rule improved to **eight** at this boundary.

## Applying Agent 1's existing DEST parity gate to the missing donor bits

Under the original-source-correlated hypothesis that the first output immediately following ordinary row43's four payload words is its rejection-sampled DEST draw, `Q0=X332` has tempered top-two-bit code **2** (accepted bench) or **3** (rejected). Both have tempered MSB **1**. The MT temper transform is invertible and toggling an *untempered* high bit flips the tempered MSB, so for any known low31 Q0, exactly one of its two high-bit completions satisfies the observed row43 label.

Agent 1 already derived the same original-row bench => first-sample tempered-MSB=1 observation as a general sampler parity equation, although the original target remains free with only metadata. Here that previously known bit **resolves the predecessor high bit of target word1 after the hypothetical donor package is granted**. Therefore, under the stated **Q-low31 + M-full donor package**, the four selected words have **at most four** combinations: the first **eight bytes are uniquely defined**, and each of the last two 32-bit words has a binary alternative differing by the exact tempered XOR mask **`0x44081102`**. No speculative value from the corrupted selected ACK or acceptance digest is involved.

A separate direct elimination on **all 528 intact original printer payload words** with this index955 fixture returned the following *hypothetical-donor* target quotients:

| Equations granted beyond 528 original full words | Remaining selected coupon rank |
| --- | ---: |
| None | 128 |
| All four Q low31 + four M full32 | 3 (eight candidates) |
| Above + tempered MSB of Q0 from row43 DEST=bench | **2 (four candidates)** |

Original-only GF(2) rank is **15,305** before granting these new *hypothetical* readings. This calculation agrees with the explicit four-way recurrence construction. **No new donor bytes have actually been located.** The table is a conditional sensitivity calculation, not recovered K04 source data.

## Stronger seven-draw CLASS/DEST continuation

With the **additional, more speculative** exact-gap model `s44-s43=11`, seven draws follow row43's four-word payload. Assume no unrelated draws: a sequence of DEST rejects (top2=3), an accepted bench code (top2=2), CLASS rejects (top3 in 3..7), and final row44 accepted STORES (top3=1). The first four hidden draws are Q0..Q3, whose low31 values would come from the donor. Enumerate their otherwise unknown MSBs and reject any prefix inconsistent with this two-stage automaton. The remaining three unobserved draws can complete any surviving prefix in the tested producer model.

The standalone SFT exercises **25,000 reproducibly seeded genuine CPython MT streams**. Among **12,616** with the original-row43-compatible immediate top2 condition, **93** also satisfy the exact seven-draw bench→STORES history. For all 12,616, the true synthetic K04 payload lies in exactly four constructed candidates, with fixed first eight bytes and two possible `0x44081102` toggles. For the 93 strict-model histories, the recovered conditional class sizes are:

| Distinct candidates after metadata prefix filtering | Synthetic cases |
| --- | ---: |
| 1 | 53 |
| 2 | 30 |
| 4 | 10 |

The actual synthetic truth was present in **every** surviving candidate set. These are calibration counts for an explicit conditional producer family, *not* evidence of the historical K04 bytes and not a probabilistic claim about the real missing coupon.

## Limitations, novel next cracking decision

1. The required **Q low31 four-word donor and M full32 four-word donor remain historically unlocated**. Existing ordered recorder/RC-17 donor pools yielded no accepted K04 pairings; their failed combinations must not be rehashed.
2. The index955 vector is algebraically consistent with intact source payloads, but **fails the stronger global strict CLASS/DEST producer chronology** in [Agent50](h17-k04-index955-metadata-discriminator.md) and [Agent11](h17-k04-double-twist-global-target-branch.md). The above local first-draw inference is consequently **conditional** and cannot authenticate the whole index955 stream. Other `p` positions or `p-s43>627` lose this immediate post-row43 DEST deduction.
3. The source label supplies a *prospective disambiguator*: **only after** independent indexed Q/M donors are discovered, compute four candidate payloads via the SFT and test the unchanged K04 commitment. With the stricter no-extra seven-draw interpretation, use CLASS/DEST filtering to obtain 1, 2 or 4 candidates. Demand a held-out intact printer/recorder prediction before calling the donor alignment historical.
4. No K08 exact final-caption witness is identified here. Do not broaden unanchored text/HMAC guesses.

**Recovery state remains six slots PASS, K04/K08 unresolved, combined INCOMPLETE.** Original evidence, mask, verifier and acceptance commitments were not changed. This result improves the **candidate-completion branch** if valid donors become available; it recovers **zero present K04 target bits** without them.
