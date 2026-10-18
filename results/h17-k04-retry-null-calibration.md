# K04 printer retries: exact statistical calibration against an independent-byte null

**Agent 10, 18 October 2026.** This note extends the deterministic Hamming-geometry audit in [h17-k04-retry-nonredundancy.md](h17-k04-retry-nonredundancy.md) with a narrow probabilistic control. It uses the **three** exact-job `CLASS=RECOVER` attempt payloads in the original `resources/evidence/print/spool-reconstruction.log`, with the original data unchanged.

## Observations and calculation

The three 16-byte payloads for `PS-261003-0417` have pairwise bit distances of **68, 62 and 62**, and every corresponding byte is different between every pair. These values are reproducible with [the standard-library checker](check_h17_retry_null.py).

For a **hypothetical** model in which each recorded byte in each of the three attempts is drawn independently and uniformly from 256 values, a given byte position contains three pairwise-distinct values with probability

`(255/256) × (254/256)`.

Across 16 independent byte positions, the probability **all 16 positions** contain three distinct values is **0.828520889731717**, approximately **82.85%**. Thus the observed all-byte divergence is **ordinary under this null model**. It is not itself anomalous evidence of corruption.

For two independent uniform 128-bit payloads, bit distance `D` follows `Binomial(128, 1/2)`, with expectation **64** and standard deviation **sqrt(32) ≈ 5.65685**. The observed pairwise distances give the following exact two-sided binomial-tail probabilities, using `Pr(|D-64| ≥ |observed-64|)`:

| Attempt pair | Distance | Tail probability |
| --- | ---: | ---: |
| 1 vs 2 | 68 | 0.53626871 |
| 1 vs 3 | 62 | 0.79100745 |
| 2 vs 3 | 62 | 0.79100745 |

Each is ordinary under that marginal null. **Do not multiply the three tail probabilities as though all three distances were mutually independent:** they share source payloads. The computed probability of *all byte positions distinct* is the exact three-array event probability and does not make that independence mistake.

## Inference boundary and research implication

The case does **not** say that the three printer attempts are independent uniform random draws, and the three samples do not prove that model. The calculation is a diagnostic counterexample to an implicit assumption that every byte being different is strong evidence of unusual corruption or of an error-correcting shared source.

The previously established conditional 34-bit minimum covering radius for a common source remains valid. Yet the case supplies **no basis to assume one common original source** or an independently authenticated payload. The routing rule selects RECOVER attempt 2 as the last ACK, and its mask-XOR value still fails the unchanged K04 commitment. The simple iid null explains the raw interattempt distances without an inferred repair transform. Consequently, this evidence does not justify expanding arbitrary bitflip-radius searches.

Reproduce from the untouched repository case files by running the linked read-only Python checker. No seed, fitted parameter, statistical significance threshold, new source integrity assertion, or altered acceptance commitment is involved. Original outcome remains **six PASS, K04 and K08 MISSING, combined INCOMPLETE, accepted=false**.
