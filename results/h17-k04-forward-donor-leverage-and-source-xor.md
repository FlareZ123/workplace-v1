# K04 forward-state donor cracking: exact future witness positions and source-derived XOR constants

**Agent 29, 20 October 2026 ~00:00 Dublin / 19 October 23:00–23:55 UTC.** This is **new target-facing original-source algebra** beyond the prior `[-229,700]` earlier-state donor atlas. It reconstructs **conditional, explicit 32-bit equations directly involving the missing target word**, without reading its corrupted ACK, XOR mask, SHA commitment, K08 nonce or verifier. It does **not** identify a historical future-stream producer or recover K04.

[Read-only SFT](../agents/agent29/k04_future_donor_sft.py); original 43-member case export; [fully original-data-consistent index955 fixture](h17-k04-source-consistent-index955.json). Original printer spool SHA256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.

## New cracking question and model scope

Earlier [target-leverage atlas](h17-k04-target-leverage-paired-hidden-windows.md) tested hypothetical source words at stream indices `-229..700` relative to row43, thereby concentrating on *pre-target* donor windows. In the original-data-consistent global chronology, selected row129 starts at `p=955`; the latest intact printer row132 ends at index970. The first target-causal future descendant can appear no earlier than `p+227=1182`. Ask which **hypothetical original independent 32-bit observations at indices971..2250**, if any, would remove target ambiguity.

Represent each unrestricted initial 624-word MT state bit as a GF(2) basis vector, propagate the exact MT recurrence, then add **all 528 intact printer words** from the original spool as linear observations. The resulting source coefficient rank is **15,305** and its original numeric equations have **zero contradictions**, reproducing the saved genuine source-consistent index955 fixture. The selected row129 is withheld in both symbolic and numeric inference. Baseline selected `X955..958` quotient is 128 bits.

For each prospective future source word, add its 32 symbolic rows before projecting the four selected original K04 words. This is a **real original-source target-leverage scan**, with source values used to derive missing-to-future XOR constants only after the symbolic ranking step; the future observations are hypothetical.

## Exactly six single-word future leverage positions in the tested horizon

| Hypothetical indexed full future state word | New individually fixed K04 target bits | Target-word fixed mask (untempered) |
|---|---:|---|
| `X[1185]` | 31 | `X[958]: BFFFFFFF` |
| `X[1411]` | 30 | `X[957]: 9FFFFFFF` |
| `X[1412]` | **32** | `X[958]: FFFFFFFF` |
| `X[1865]` | 30 | `X[957]: 9FFFFFFF` |
| `X[1866]` | **32** | `X[958]: FFFFFFFF` |
| `X[1974]` | 1 | `X[955]: 40000000` |

Every other **1,274** possible individual full-word observations in `971..2250` gives **zero individually fixed selected bits** and fails to reduce the overall selected quotient in this fixture. In particular, the first generically possible future ancestor `X[1182]` has no target quotient gain; three subsequent recurrence cancellations are needed before the high-leverage `X[1185]` emerges. The results are conditional on this source-consistent index955 geometry, not a universal statement about other possible chronologies.

## Exact original-source affine predictions for future witnesses

The symbolic reduction proves that the following **32-bit bitwise XOR relations are fully determined by the 528 original intact printer payloads**. Numeric elimination with the actual original bytes gives:

```text
X[958] = X[1412] XOR 24D1E0F2  (full 32 bits)
X[958] = X[1866] XOR 99F6810A  (full 32 bits)

(X[958] XOR X[1185]) AND BFFFFFFF = 114F2035
(X[957] XOR X[1411]) AND 9FFFFFFF = 8B3B35C1
(X[957] XOR X[1865]) AND 9FFFFFFF = 87E51278
```

Here every `X` is an **untempered** 32-bit MT state word. The two complete routes to the missing target word make the following **independent held-out donor-pair prediction before observing a coupon or its hash**:

```text
X[1412] XOR X[1866] = BD2761F8
```

Two other rare paired predictions are `(X[1185] XOR X[1412]) AND BFFFFFFF = 359EC0C7` and `(X[1411] XOR X[1865]) AND 9FFFFFFF = 0CDE27B9`. A single independent historically indexed 32-bit record at state1412 or1866 would determine the **last four source payload bytes** of K04 under this model, by tempering the reconstructed `X[958]` and serializing it little-endian. This would be genuine partial K04 cracking even without full REC8 acceptance. None is yet identified.

### Direct original-carrier search and stop

Before consulting any selected ACK, mask or digest, apply these newly derived rare paired invariants to **all 88 retained TRP2 four-byte controls** and **all 12 source RC-17 footer strips**. Interpret each as a possible tempered MT word, try its own little- and big-endian byte orientation, untemper and compare distinct source fields as ordered future-index assignments. The source set has **100 original four-byte fields, 200 oriented views**. Preserve the distinction between CRC-valid and CRC-invalid recorder fields; raw CRC-invalid controls may be tested as auxiliary observations but are never promoted to K05-eligible records.

**Results for the exact four paired future-state hypotheses:** `1412↔1866` full32, `1185↔1412` 31bit, `1185↔1866` 31bit and `1411↔1865` 30bit each give **zero matches** among distinct retained original fields. The scan is a new future-descendant pairing, rather than a repetition of previously exhausted older-state inverse-twist fingerprints. It closes this bounded direct-copy class; it does not exclude an independently preserved future output not in these 100 fields, unknown serialization/transformations, or a different generator phase. No K04 target bit is *actually* recovered from the retained archive.

## Precisely actionable follow-up

1. Look for an **independently indexed source witness** to `X[1412]`, `X[1866]`, `X[1185]`, `X[1411]` or `X[1865]`, with a historical producer epoch/order and at least one withheld intact-source prediction. The two full32 paths offer a rare exact XOR mutual-authentication check `BD2761F8`.
2. If one authentic future donor is identified, compute its corresponding selected **untempered** K04 word with the equations above, temper and pack little-endian, and track the partial coupon bits. Test the original K04 digest only once a complete actual source-derived 16-byte candidate exists.
3. Do not expand arbitrary recorder permutations or reinterpret original timestamps as MT sequence indices without a new original producer witness. The index955 fixture is algebraically source-consistent but fails some stronger speculative strict CLASS/DEST chronology rules; the future equations remain **model-conditional**.

**Acceptance remains unchanged:** K04 and K08 unresolved, no full eight-component key, original combined check incomplete. This report preserves a **positive structural target-leverage discovery** and four bounded negative original external-carrier tests while leaving every original source and commitment byte untouched.
