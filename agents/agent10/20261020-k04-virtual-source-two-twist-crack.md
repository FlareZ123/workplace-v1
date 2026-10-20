# K04: virtual MT-state donor augmentation, no new target-ancestor bridge

**Agent 10, 20 October 2026. Source-only reconstruction and new donor topology probe.** K04/K08 remain missing. No queried acceptance digest, selected row129, mask, or nonce was ingested. Source data are the original ZIP printer spool, SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.

## Crack attempted

The original 42 one-twist relationships identify 25 within-row complete-state and 17 row-start predecessor-bit witnesses. The three previously published 31-bit two-twist original quartets provide additional relative row-index bridges. Directly recorded source words and those inferred bridges leave **74 nonempty indexed source groups** (75 including the selected row129 group, which is withheld and contains no words).

The earlier [external-donor two-twist attack](20261020-k04-two-twist-crosscarrier-crack.md) used only 528 intact source words. Here, a new attempt reconstructs **virtual unprinted generator words** and immediately asks whether *those virtual original-source consequences* can participate in previously inaccessible four-term MT relations, cross a disconnected index group and reach the target ancestors.

For each group, propagate the MT identity exactly, including partial masks:

`X[k+624] = X[k+397] XOR twist(X[k], X[k+1])`

Two known right-hand 32-bit words reconstruct the earlier `X[k]` high bit and `X[k+1]` low31; overlapping constraints infer further full 32-bit states. Iterate the source-derived forward/backward equalities to a fixed point, rejecting conflicting assignments. These are **mathematical consequences** of original source/index hypotheses, not new independently observed file bytes. The local implementation recovers **81 virtual full 32-bit output positions** and **45 partial positions** (15 known low31 and 30 known high1), on top of the 528 intact original payload words. The older Agent23 solver without the extra three two-twist anchors inferred 30 full and 34 partial words; the present larger figures must *not* be advertised as independently authenticated new historical data.

Use these 624 full-or-low31 state observations to join the *two-twist relation*

`(X[u+850] XOR X[u+396]) & BFFFFFFF = F(X[u]) XOR F(X[u+227])`

where `F(x)=twist(0,x)&BFFFFFFF`. A/B input terms require only known low31 bits, whereas C/D require full 32-bit state values. Enumerate **all** feasible ordered A,B pair assignments and C,D pair assignments within the 74 groups. When two terms already reside in one group, they must be separated by exactly 227 (A,B) or 454 (C,D) indexed positions. Between disconnected groups, keep both orientations and make no arbitrary chronological proxy assumption.

A matching 31-bit checksum alone is weak evidence because the enumeration is large. Before creating *any* new group index equality, impose the three exact index gaps 227/396/850 jointly on the existing 42 first-order and three original second-order source row-index equalities and the minimal **four-output-per-row** chronological floor (no CLASS/DEST assumptions). This is exact difference-constraints feasibility over the 133 source-row starts. A stricter ordinary-six-output floor was evaluated separately. Reject matches that imply an original later row precedes an earlier one.

## Observations

| Source experiment item | Observed |
| --- | ---: |
| Fully intact printer output words | 528 |
| Additional inferred virtual full words | 81 |
| Additional partial low31 / high1 source positions | 15 / 30 |
| A/B ordered candidate pair assignments | 378,988 |
| C/D ordered candidate pair assignments | 361,115 |
| 31-bit matching complete quartet assignments | **70** |
| Matched quartet with new disconnected index groups and joint valid chronology (minimum four draws) | **0** |
| Same under conditional ordinary minimum six draws | **0** |
| New target-row43/44-group bridge | **0** |

A narrower initial pilot that used *proxy row order* rather than exact source index chronology produced a tempting low31 match using a virtual state 393 output positions **before** row12 and intact rows21,34,98. The index equations from that hit require `s21 - s12 = -168`, contradicting the observed chronology even under the weakest four-word floor. It is a **false lead**, never a real new donor. The complete all-order 70-collision search with exact joint chronology avoids that failure and has zero new feasible links.

Source-born 31-bit quartets that are already internal to an existing group do reappear, providing existing original algebraic controls. No selected spool word enters the experiment. Exact relative chronology, group linkage and observational independence are distinct gates: a random 31-bit match is insufficient to authenticate the printer producer or infer a missing coupon bit.

## Reproduction scope and next gate

Two locally executed Python 3 standard-library scripts under the original case extraction are `/mnt/data/h17case/k04_virtual_twist_closure.py` and `/mnt/data/h17case/k04_virtual_twist_global_join.py`, importing `k04_two_twist_crosscarriers.py`. These are session-local and not yet checked into the shared repository. All three files read original source data and never consult an acceptance target or contested selected payload. Published assignment and no-link counts above came from actual complete executions, including a separate all-row four-draw-minimum run.

**Stopping decision:** a virtual word already algebraically determined by intact source cannot be presumed to supply the independent entropy missing at K04. This larger original-source observation closure yields zero newly consistent inter-group MT positioning links, including to either coupon ancestor side. Reopen only for an authentic **new external source** observation with independently supported producer/index, or an original ESC-N coupon/mask correction witness. Additional virtual-model ranks and speculative caption dictionaries are poor substitutes. Original REC8 remains six accepted components, K04/K08 unresolved, combined not accepted.
