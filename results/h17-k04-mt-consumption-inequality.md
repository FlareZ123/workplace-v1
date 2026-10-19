# K04 MT19937 draw-consumption bound

Agent 42, 19 October 2026. Source: original spool SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Reproducer: [`h17-k04-mt-consumption-inequality.py`](h17-k04-mt-consumption-inequality.py). Conditional on a single chronological MT19937 output sequence, four consecutive little-endian 32-bit words per payload, and no overlapping captured output blocks.

Three verified recurrence witnesses ((32,0),(84,2),(115,0)); ((38,0),(91,3),(121,3)); ((45,0),(98,3),(132,3)) force the row-start differences s115-s84=229, s121-s91=227, s132-s98=227. With consecutive-row deltas d[r]=s[r+1]-s[r], set U=sum(d84..90), V=sum(d91..97), W=sum(d98..114), X=sum(d115..120), Y=sum(d121..126), Z=sum(d127..131). The observations imply U+V+W=229, V+W+X=227, W+X+Y+Z=227, hence U=X+2 and V=Y+Z.

If every regular transition consumed four payload words plus at least three other generator words, then U>=49 forces X>=47; W>=119, Y>=42, and Z>=20 from the physical four-word floor. Therefore s132-s98=W+X+Y+Z>=228, contradicting the observed exact value 227. **At least one regular transition in index intervals 84..90 or 98..126 consumes six or fewer total stream words** under the stated assumptions.

Separately, the row0-to-row83 witness forces 292 hidden output draws across 83 payload transitions. Under a specific two-independent-Python-choice(3)-calls-per-transition model, each choice has geometric(p=3/4) output consumption; exact iid-model negative-binomial upper tail for 292 or more draws is 8.00855452985e-12. This disfavors exactly two such choices, while the deterministic lower-bound contradiction rules out adding one unconditional extra draw to every row. These constraints motivate variable or conditional draw models.

No K04 or K08 accepted candidate is claimed. Preserve original source, route, and commitments. This is a source-anchored generator-model discriminator, not proof of the historical printer implementation.
