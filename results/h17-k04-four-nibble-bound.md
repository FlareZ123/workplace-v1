# H-17 K04: exhaustive four-distinct-nibble correction bound

**Agent 40, 18 October 2026 UTC. Status: NO_MATCH.** This is a finite *exploratory* error-family exclusion against the original, unchanged K04 commitment. It is not a recovery of the original ESC-N coupon, does not establish actual nibble corruption and does not change the canonical six-PASS/two-MISSING recovery status.

## Original evidence anchor

The incident-date logical ESC-N route in `resources/evidence/archive-labels.ini` resolves to job `PS-261003-0417`. The last acknowledged RECOVER attempt in `resources/evidence/print/spool-reconstruction.log` is attempt 2 (18:02Z), with 16-byte payload `A9A9DC5731A5E2AE879C47215C2559D5`. The route-sheet transcription `resources/evidence/recovery-routing.json` contains XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C`. Applying the stated XOR gives baseline component `2CFF149C50E54557228E7DE60B3EB7C9`.

That baseline's SHA-256 is `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`, different from the untouched `resources/acceptance.json` K04 target `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`. The custodian explicitly cautions that ACK is not a payload-integrity certificate and that routing information is transcribed. There is **no original-record assertion that exactly four hex digits were miscopied**. The computation tests that hypothetical class only.

## Enumerated class and source

Represent the current 16-byte baseline as 32 hexadecimal nibbles, indexed 0–31 from left to right. Choose **exactly four distinct nibble positions** `a < c < d < e`. For each position, XOR the original nibble with one of the 15 nonzero four-bit deltas, preserving all other nibbles. SHA-256 the resulting 16 bytes and compare with the original 32-byte slot commitment.

The exhaustive assignment count is `C(32,4) × 15^4 = 1,820,475,000`. Every assignment has exactly four changed nibbles. Search source: [k04-four-nibble-scan.c](k04-four-nibble-scan.c). It checks the baseline's known SHA-256 before enumeration, invokes OpenSSL's SHA256 on 16 bytes, and neither reads nor writes original evidence. The C source includes optional position-range arguments to split long runs.

The 29 disjoint executed shards were indexed by `c`, the **second-smallest** changed nibble position, from 1 through 29. For fixed `c`, exactly `c × C(31-c,2) × 15^4` assignments were checked. Every completed shard returned NO_MATCH and its expected assignment count. The [full shard ledger](h17-k04-four-nibble-progress.json) records all 29 counts and the zero-match outcomes. Their sum is the exact full coverage count above.

## Independent correctness control

Before interpreting the real target, an independent Python computation created a synthetic four-nibble correction to the known baseline: change nibble positions 0,1,2,3 by nonzero XOR deltas 1,2,3,4, obtaining `3ECB149C50E54557228E7DE60B3EB7C9`. I computed SHA-256 of those 16 bytes and rebuilt the same scanner with **only its target digest** replaced by that artificial digest. On shard `a=0,c=1`, the scanner returned `MATCH a=0,c=1,d=2,e=3` with the correct four deltas and complete 16-byte component. The original target was never changed in the original scan. The synthetic test supports the implementation's ability to detect in-class matches; it supplies no historical evidence.

## Interpretation and restrictions

**Result:** 1,820,475,000 tested four-nibble assignments, **zero original K04 matches**. Combined with the previously verified exclusion of zero through three changed nibbles in [minimum-correction-footprint](h17-k04-minimum-correction-footprint.md), any component that passes the unchanged original K04 commitment must differ from the currently derived baseline in **at least five hex-nibble positions**. The other established independent necessary bounds still apply: at least three changed bytes, seven changed bits, and a changed-byte span of at least five positions.

This is a mathematical bound on candidate differences relative to the current source-derived value. It **does not imply** the true original printer media experienced five bad nibbles, that the route or mask transcription is genuine, or that a five-nibble search is historically motivated. For a single-layer correction, XOR preserves nibble differences equally if the inaccurate layer was the mask instead of the payload; if multiple layers are wrong, the bound applies only to their combined resulting K04 value.

No K04 original payload, corrected mask, authenticated K08 final caption or combined REC8 key was recovered. Maintain K04 and K08 as null in the canonical candidate. In line with the [Critic's provenance gate](../communications/broadcast/2026-10-18T0106Z_Critic_evidence-priority-enforcement.md), further speculative mutation radii are lower priority than a source-backed explanation and discriminating independent evidence.
