# K04: joint CLASS/DEST sampler constraints still leave the selected 128 bits free

**Agent 38, 19 October 2026 ~09:42 UTC.** This is a new source-conditioned, joint hidden-draw analysis responding to the 19 October Critic's request for a **target projection** instead of another isolated gap floor. No K04 coupon or K08 caption is recovered.

## Exact producer branch and retained source

Use the 42 original printer MT19937 recurrence witnesses, with selected printer row129 excluded from ingestion. Their anchored positions include row43 at 0, row96 at +393, row128 at +623, and row44/row97/row130 at shift `d`, `d+394`, `d+620`. Taking the narrowest **hypothetical** RECOVER-tail model in which no extra generator outputs occur across row128→129→130 sets `d=11` and selected row129's four-word start `p=627`. The two otherwise unobserved, source-critical gaps then have exactly seven outputs after row43 and eight after row96.

Test a very specific, unverified metadata model: an ordinary row's post-payload DEST is selected by CPython-style rejection sampling of a two-bit code in `0..2` (`store=0, desk=1, bench=2`), and the next row's CLASS by rejection sampling of a three-bit code in `0..3`. The observed target-adjacent labels are row43 DEST=bench, row44 CLASS=STORES, row96 DEST=store, row97 CLASS=LABEL. For n=4 CLASS, code3 is conditionally permitted to alias LABEL, exactly as in the earlier Agent50 automaton. A rejected DEST code is 3; a rejected CLASS code is 4..7.

Unlike independent lower-bound minimization, **each candidate partition assigns all sampled output positions in both gaps to either DEST or CLASS**; it imposes the corresponding linear MT19937 *tempered-bit* constraints and evaluates their simultaneous feasibility with both anchored source groups.

## New computation and actual target information

The [read-only reproducer](../agents/agent38/k04_joint_sampler_target_rank.py) uses the same 19,968-variable MT19937 linear representation and 44 intact source payloads as [Agent49's target baseline](h17-k04-gf2-target-independence.md). It projects the target's **128 individual bit expressions modulo every source and metadata equation**; a new canonical reduction explicitly exhausts all known pivots, including those below the first free bit.

| Exact quantity | Result |
| --- | ---: |
| Existing 44-word source observation rank | 1,123 |
| Metadata partition cases: gap43 6 splits × gap96 7 splits × CLASS97 2 choices | **84** |
| Jointly feasible source/metadata partitions | **10** |
| Jointly contradictory partitions | 74 |
| All feasible partitions require first post-row96 DEST draw to accept | **yes** |
| Surviving gap43 DEST draws before acceptance | 1, 2, 3, 4, or 5 |
| Surviving CLASS97 code interpretation | 0 or 3 |
| Combined observation rank in feasible branches | **1,136..1,140** |
| **Rank of 128 target bits modulo all observations, every feasible branch** | **128** |
| Individually determined target bits, every feasible branch | **0** |

This is a stronger obstruction than merely failing local inverse-twist propagation. In the exact tested producer model, **both metadata samplers jointly force 13–17 new independent linear equations, rule out 74 of 84 hypothesized rejection paths, yet still fail to constrain any of the selected four 32-bit output words.** Every 128-bit target vector remains attainable by some unrestricted MT state within each surviving branch.

## Limits and cracking decision

This is neither an authenticated physical printer implementation nor a source-established no-extra-draw RECOVER tail. The actual printer producer could use a different CLASS table, n=3 sampler, other consumption order, cached draws, or a different stream. This conditional calculation does not rule out seed initialization constraints, an independent non-printer control within the **two hidden ancestor gaps**, or other row44 shifts. Source record acquisition timestamps independently challenge a literal on-demand common-MT producer.

**Actionable direction:** the two sampler mechanisms alone, even when aligned simultaneously at the minimum possible target gap, do **not** resolve K04's 128-bit information bottleneck. A target-facing advance must add a **new original source observation inside either ancestor gap** (particularly row43 output+4 and row96 output+7), or an independently justified low-dimensional seed/producer rule. Further isolated integer-gap refinements will not supply 128 missing output bits.

Original record bytes, K04 mask, K08 nonce and REC8 commitments were not modified or used to infer the target. Acceptance remains six individual PASS, K04/K08 MISSING, combined INCOMPLETE.
