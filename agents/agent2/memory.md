# Agent 2 continuity

Claimed 2026-10-17T20:29:45.705916Z, run `b26f853d-bd2c-47ba-8f63-0102629878da` (mode draw 2 = normal). Source case is the 4 October 2026 H-17 local preservation export also mirrored in `resources/`.

## Verified results

Detailed report at [results/h17-recovery.md](../../results/h17-recovery.md). Six slots pass the unchanged `acceptance.json`: K01 `049AAB2E1CDE7A82CD7C60234303C91A`; K02 `0D7E3AB56FB75DA3EB0E2E06786D239E`; K03 `1384AF96E25D6ADA666209CB55E062FA`; K05 `FF8B78200A56E8586DCDA00EF01E4572`; K06 `5DBF40EE52FAAED9A536D3326CF0D95A`; K07 `93495F5E425AB8E592123DABAEB68545`.

The correct K04 spool route produces `2CFF149C50E54557228E7DE60B3EB7C9`, which fails the slot acceptance; do not submit it. K08 keeper wording is not authenticated in the extant drafts; no text span matched the keyed acceptance. Combined commitment remains untestable until both are solved. This is an evidence gap, not evidence of a failed SHA256 implementation.

K04 negative tests: 133 spool payload XOR candidates, exhaustive single/two-byte mutations (~7.9 million), exactly three-nibble mutation (16.74 million), no hit. K08: 150,626 contiguous normalized candidate word spans over surviving texts, no hit. A full local reproducible derivation script and candidate JSON were generated in /mnt/data/H17 (outside GitHub); detailed reproduction parameters in public result.

Additional K04 check: exhaustive 3-adjacent-byte replacement at all 14 offsets = 234,881,024 SHA256 trials; no K04 acceptance match. C source exists in the generated local work package. This further weakens a short local media-burst explanation, without making the payload authenticated.

## Next valuable work

Look for *independent* information able to establish actual ESC-N ACK payload integrity or exact keeper caption. The assignment specifies the export is trimmed, and no external mailbox or facility access is permitted. More arbitrary guesses against K08 or unguided >3-byte search on K04 have very low expected value. If new artifacts arrive, re-test the SHA-256 slot commitments first, then the combined commitment. Never change acceptance.json, verify.py, or surviving evidence.

Repo README rule: avoid per-commit CI. Counter was incremented from 1 to 2 this invocation. Identity lease remains active unless explicitly released according to original prompt's 70-minute age rule.

## New incarnation: 2026-10-17 23:14:57 UTC

Actual RNG draw 2, normal mode. Reclaimed eligible Agent 2 identity, run `h17-agent2-24a1aba7934b91c5`; original `claimed_at` remains `2026-10-17T23:14:57.480235Z`. Increased shared COUNTER 13→14 before claim. Repository README prohibits per-commit CI; none created. Re-extracted user-supplied ZIP and reran untouched `verify.py`: six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false; original file ZIP SHA256 remains `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`.

Retrieved current Git tree via GitHub connector's generic `fetch` endpoint (`/git/trees/main?recursive=1`, not code search). Confirmed `private/` contains only `.gitkeep`, in agreement with Agent 10 broadcast. Read Critic sufficiency and Agent 10 private/carrier messages. Found no separate local evidence beyond `prompt.md` and 43-member ZIP. Updated `results/README.md` to close stale publicly open private-source audit and explicitly flag two source-date anomalies: mail16 dated 03 Oct 07:49 refers to 18:03 later same day, and mail13 dated 02 Oct 09:56 calls AX-7782 a final handoff before the transfer COMMIT of 03 Oct 20:55. Commit `f883ac46ada0cdb9f199a692444d6b8bc4448745`. Neither anomaly supplies alternative accepted K04/K08 values.

Reconfirmed absence of documented K08 final exact caption in crew notes and mail11/mail20; every proposed semantic caption would be a guess unless backed by new source. No unverified bytes promoted. Continue source-grounded investigations or produce a transparent six-slot recovery workpack. Do not confuse this checkpoint with lease release; after each checkpoint check original lease age, and release only when 70 minutes reached.

## New incarnation: 2026-10-18 08:17:17 UTC

Actual uniform mode draw was 8 (normal research). Counter incremented 66→67 (commit `4a1db78d`); successfully claimed eligible Agent 2 identity as `h17-agent2-7b236d80cfcf6a85`, lease `2026-10-18T08:17:17.863499Z` (commit `c50cdeb4`) and verified remote claim. Reviewed top-level README, canonical results/README, latest Critic frontdoor evidence gate, agent mail, and original 43-member ZIP. Current `private/` contains `.gitkeep` only. This invocation did not produce a new authenticated K04 coupon or K08 caption.

Re-extracted user ZIP into `/mnt/data/H17-agent2/`, recreated six-slot candidate with K04/K08 null, ran original `verify.py` (six PASS, two MISSING, combined INCOMPLETE, accepted false). Prepared a self-contained **user-facing handoff**, `/mnt/data/H17_recovery_handoff_20261018.zip`, containing all 43 original evidence members, verbatim original ZIP, per-member SHA256 manifest, candidate, original verifier JSON, a read-only stdlib source-reduction script at `work/rederive.py`, reproducible output, and evidentiary notes. Handoff SHA256 `3979f6105f27bd084f9d6e5b48ccc87947dbb9d0a31cbf63ad9d531f3fe0c2d3`. Independently extracted handoff and reran both replay and unmodified original verifier. This is custodial packaging for the requesting human, not new shared solution research, so no duplicate public `results/` addition made.

Continued source checks confirmed the acknowledged ESC-N attempt-2 component is the known NO_MATCH `2CFF149C50E54557228E7DE60B3EB7C9`, and the authentic final wording of Emily's incident-envelope caption remains unquoted. No source-backed new mechanism passed the Critic's discriminating-prediction gate. Potential future work still requires independently reconstructible original source rather than speculative source mutations or phrase generation. Original evidence and acceptance left unchanged. **Do not treat checkpointing this note as lease release; compare original lease timestamp to actual runtime clock after commit, and if under 70 minutes continue substantive investigation.**
