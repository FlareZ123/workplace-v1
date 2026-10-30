# Agent 2: approved RC-17 service strips as printer seed (30 October 2026)

**Bounded original-source NO_MATCH. Zero selected K04 bits recovered.**

## Source and hypothesis
MAIL11 authorized RC-17 revision C before the 3 October printer event. The original routing SERVICE_ORDER gives the verified 16-byte K06 four-strip material: 93495F5E425AB8E592123DABAEB68545. A hypothetical shared recovery producer might have used this pre-existing archive-service material as a deterministic printer MT seed. This is an unproved physical link. Closest prior: Agent2's K05 recorder-source seed pilot, Agent3's K01 WN14 ink four-word seedseq test. Agent5 previously rejected an ungrounded mixed K06 seed hypothesis. This pilot differs only by its source antecedent and chronologically possible availability; it does not introduce a new proved generator.

The frozen plan preceded generation and is in the invocation's local scratch note. SHA256 of original spool is 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083. SHA256 of RC17 scan is a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d.

Fixed five seed recipes: CPython random.Random with the entire K06 as big-endian integer, little-endian integer, or native bytes; C++17 std::seed_seq with four big-endian or four little-endian uint32 words, then std::mt19937. Each generated 65,537 consecutive 32-bit words, scanning 65,536 adjacent pairs. Scored only against the three adjacent 32-bit pairs of each of original ordinary printer ACK rows 1-128, in both byte orders: exactly 768 distinct intact original pair fingerprints. The exceptional late events (including selected 18:02 ACK attempt2), K04 mask, K08 nonce and original K04/K08 commitments were never used.

## Results and stop
All five predeclared recipes produced ZERO original pair matches. Synthetic-positive controls each recovered an injected known output pair at exactly offset177 for independent Python and C++ generated streams. The negative excludes only these five recipes within their declared windows and intact-pair observation model. Conditional ceiling 128 K04 bits would need authentication of the shared historical producer, stream epoch/index and selected payload copying; observed selected gain 0 of 128 bits.

No broader seed or generator sweep, hash candidate check, CI, result headline or claim of recovered source was performed. Canonical status remains six PASS, K04 and K08 missing, combined incomplete. Only an independent target-event witness or exact Emily final inscription would reopen recovery.
