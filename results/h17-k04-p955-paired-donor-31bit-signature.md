# H-17 K04: 31-bit original-source signature across a future donor pair

**Agent 6, 29 October 2026.** [Reproducible original-source SFT](../agents/agent6/k04_p955_donor_pair_signature_sft.py). **Conditional source-observation result; no recovered K04 coupon or REC8 PASS.**

## New original-source relationship

The previously published [K04 hypothetical forward-donor atlas](h17-k04-future-donor-target-rank.md) identifies four possible single full 32-bit MT19937 state words in its p955 chronology with positive K04 target leverage: X[728], X[1185], X[1411], X[1412]. None is present as a separately authenticated original record. Agent6 preregistered six prospective two-word pair tests at /mnt/data/h17_agent6_20261029/donor_pair_source_signature_preplan.md, SHA256 dbd0c00cc8ab94f40021f7d8bc59a56c7b41082510ef9e6c39c67f587c757524, before executing the source-only calculation. No broad carrier search or K04 acceptance trial was permitted.

Use the 133-row original printer spool (SHA256 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083), **erase selected row129 before payload decoding**, and impose the existing [hypothetical original-consistent p955 chronology](h17-k04-source-consistent-index955.json). This is a conditional common MT stream model; it contradicts some stricter CLASS/DEST sampler interpretations and is not authenticated historical producer code. All 528 untouched source words give 16,896 GF(2) observations, exact source coefficient rank 15,305, no contradictions.

The source fixes the complete untempered state word X[789] = EB3D818E (original intact spool row105 word0). The MT19937 recurrence at original-state t=788 then forces:

```text
X[1412] = X[1185] XOR twist(X[788], X[789])
X[789] = EB3D818E, and only X[788]'s MSB enters this recurrence.
twist(X[788], EB3D818E) = 359EC0C7 or 759EC0C7.

(X[1185] XOR X[1412]) AND BFFFFFFF = 359EC0C7
```

This is **31 source-fixed independent parity bits** across two otherwise unrecovered 32-bit donor words. It could discriminate an independently recovered genuine pair from false producer-index associations, provided separate historical epoch/order and intact heldout-output evidence exists. It does not reveal the two donor word values, and a matching accidental 31-bit relation is not in itself provenance authentication.

## Exact coefficient ranks and target relevance

| Proposed potential donor(s) | Conditional unknown dimensions | Source-fixed parity bits |
|---|---:|---:|
| Any of 728, 1185, 1411, 1412 alone | 32/32 | 0 |
| Five of six possible pairs other than 1185/1412 | 64/64 | 0 |
| **1185 and 1412 together** | **33/64** | **31** |

The pair's **joint** target leverage is not additive: original K04 selected row129 remains rank128/128 unknown with no new historical witness; hypothetically supplying X[1185] yields target rank97, X[1412] yields rank96, and supplying both still yields rank96. Thus the new 31 parity bits provide a **potential source-integrity check**, not 31 additional authenticated coupon bits.

The first informal calculation combined affine RHS values with zero-valued donor coefficient equations and erroneously counted 30 fixed parities. The corrected source coefficient-only rank gives **31**. Affine elimination independently recovers the actual 31-bit comparison value above and confirms the omitted bit30 remains unknown.

## Independent checks and limits

The [read-only self-test](../agents/agent6/k04_p955_donor_pair_signature_sft.py) uses the exact unchanged original ZIP and the published row-index fixture, runs the complete original-source coefficient and affine constraints, enumerates all six original donor-pair ranks, verifies each of 31 fixed XOR-bit values, and uses five separate seeded native CPython MT19937 generators as recurrence controls (**5/5 PASS**). It never reads selected row129's payload, the mask, slot commitment, nonce or REC8 verifier.

**Historical status:** K04 newly authenticated bits 0/128, K08 exactly attested final words 0, six prior individual slots unchanged, complete REC8 not accepted. No genuine original X[1185] or X[1412] donor or common physical epoch witness is available. A newly preserved target-era cassette buffer, independent printer output or original final caption would be needed to advance recovery.
