# Agent 31 continuity — H-17 archive recovery

Claimed normal-mode identity on 18 October 2026 at 06:36:02 UTC, run `h17-recovery-agent31-20261018`. Uniform mode draw returned **1**. Initial root COUNTER incremented 57 to 58, with claim confirmed by GitHub readback. Original immutable lease at `agents/agent31/.lease.json`. Check real UTC lease age after each checkpoint; orderly release only if elapsed >=70 minutes.

## Current source-grounded state

Read root `README.md`, current repository synthesis `results/README.md`, original 43-member supplied ZIP, original AGENT_PROMPT, START_HERE, records custodian, route transcription, acceptance commitments, all email bodies, crew notes, selected spool records, printer map, maintenance/procedure records. Read Critic's 18 Oct 01:06 evidence-first and 01:29 freeze-baseline interventions and relevant agent memories/research.

Canonical accepted original REC8/1 slots are K01 `049AAB2E1CDE7A82CD7C60234303C91A`; K02 `0D7E3AB56FB75DA3EB0E2E06786D239E`; K03 `1384AF96E25D6ADA666209CB55E062FA`; K05 `FF8B78200A56E8586DCDA00EF01E4572`; K06 `5DBF40EE52FAAED9A536D3326CF0D95A`; K07 `93495F5E425AB8E592123DABAEB68545`. Original verifier freshly executed on separate local ZIP: six PASS, K04/K08 MISSING, `combined=INCOMPLETE`, `accepted=false` (normal failure exit 1).

K04 selected incident ESC-N exact-job ACK attempt2 payload `A9A9DC5731A5E2AE879C47215C2559D5` XOR recorded mask `8556C8CB6140A7F9A5123AC7571BEE1C` yields `2CFF149C50E54557228E7DE60B3EB7C9`, which fails original K04 SHA target. No independent printer bytes checksum; mapping and mask both transcriptions. K08 last signed keeper caption not literally quoted in surviving sources; N02/N06 draft captions and N17/N18 other-envelope labels are explicit non-final text. No accepted K04 or K08 value recovered.

## Work this incarnation

Created conversation-local `/mnt/data/H17_partial_archive_recovery.zip` with `candidate.json`, `verification.json`, `DERIVATION.md`. Confirmed ZIP CRC and unchanged original verifier acceptance statuses. This is a **user handoff**, not a new original source witness and not a new result in the shared repository. Input file original ZIP untouched. No facility equipment, people, or outside records contacted.

I examined original source artifacts for a new caption/witness or independent K04 mask/payload corroboration. Existing researched boundaries and recent agent notes already cover the obvious candidates, including finite mutation/fragment families, direct text carriers, ZIP metadata, single-source mask+nonce, and chronology. Avoid duplicating work and promoting speculative NO_MATCH families.

## Next priorities

Only pursue a source-anchored local carrier or correction model that supplies original K04 payload/mask or authenticated exact K08 wording. Require observed anchor, historical mechanism, deterministic reduction, prediction beyond hash failure, and untouched commitment PASS (Critic 01:06). Preserve canonical nulls otherwise. Shared synthesized status at `results/README.md`. Current original case export explicitly trimmed; latest repo maintainer says task solvable, but no permitted independent original source yet identified. No per-commit workflows.


## Further local reproducibility and one narrow source-model falsification

Added read-only `work/rederive.py` to the *local user package*; it selects the six accepted components directly from evidence and asserts original per-slot SHA-256 commitments. Kept K04 as diagnostic NO_MATCH and K08 as MISSING. Fresh-extracted nested original ZIP, candidate, source replay and unchanged verifier reproduce byte-for-byte. Current local package `/mnt/data/H17_partial_archive_recovery.zip` includes candidate, original ZIP, work/rederive.py, its JSON audit, verification JSON and derivation note. This is intentionally not copied into shared `results/` because `results/replay_h17.py` already serves the same purpose.

A specific **hypothesized transcription-field swap** was checked because both K04 mask and K08 nonce are 16-byte literals in the same unauthenticated `recovery-routing.json`. Holding source-selected ACK payload constant but substituting the recorded nonce as mask gives `F63AE1F19018E16DAA398CE30F61AD42`; its SHA-256 does **not** match K04. Five known K08 draft/label/theme examples also fail if the recorded K04 mask is used as the HMAC key. This falsifies the simple mutual field transposition under the original source selection, with no new component or historical evidence. Do not expand into invented masks/keys absent another witness.

