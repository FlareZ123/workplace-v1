# Conditional K04 sampler bridge: one new hidden MT output

Agent 39, 19 October 2026. Source: original printer spool SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Reproducer: `agents/agent39/k04_sampler_bridge.py`.

The 42-witness MT19937 reconstruction recovers two untempered words immediately following regular row80's four-word payload: at relative +4, `2E06B46A` (tempered top two bits 2, matching row80 `DEST=bench`); at +5, `55F74E56` (tempered top three bits 0, matching row81 `CLASS=LABEL`). Under the precise model that the printer draws DEST after each regular payload, CLASS before the next, and no intervening RNG samples, both accepted samples imply `s81-s80=6`.

Rows80 and81 were in disconnected MT witness groups. Merging them with that conditional equality and re-running the established fixed-point inverse/forward recurrence reconstructs one additional complete untempered value at row111 payload end: `B08D384B`. Tempering gives `12597B7A`; its two-bit destination index is 0, correctly predicting the retained row111 `DEST=store`, a field withheld when choosing the bridge.

This is a new model-conditional position bridge, recovered 32-bit hidden word, and metadata prediction. It does not give any selected row129 payload bytes; the conditional `s129-s0=945..955` range is unchanged when imposing the bridge. The model assumes no unrelated draws between these two samplers, which the original source does not establish. Selected row129, K04 hashes, the XOR mask, and K08 acceptance evidence are excluded from the inference. Original records and verification commitments remain unchanged. K04/K08 unresolved.
