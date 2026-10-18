# Agent 35 H-17 recovery continuity (18 October 2026 UTC)

**Invocation mode:** cryptographic random draw 8 -> normal research mode. Claimed lease `agents/agent35/.lease.json` at `2026-10-18T02:36:58.285Z`, verified its successful GitHub push. Incremented root COUNTER from 34 to 35 before claiming. Never refresh the claimed_at timestamp. After each checkpoint compare current real UTC time with it; only perform orderly release at >=70 minutes.

## Case baseline independently observed
- Extracted exact user-supplied 43-member ZIP to local `/mnt/data/h17-agent35/` without modifying source member bytes. Read START_HERE, AGENT_PROMPT, custodian note, routing, records labels, all crew notes, full email trail, spool records, transfer ledger, acceptance and original verifier. Original case scope excludes outside mailboxes/devices.
- Reconstructed canonical six accepted slot values from existing source-grounded research and ran the ZIP's **unchanged** `verify.py` locally on `candidate.json`: K01/K02/K03/K05/K06/K07 PASS; K04 and K08 MISSING; combined INCOMPLETE; accepted false.
- K04 written rule selects incident-date ESC-N `PS-261003-0417`, RECOVER attempt 2 ACK at 18:02Z, payload `A9A9DC5731A5E2AE879C47215C2559D5`. XOR original written mask `8556C8CB6140A7F9A5123AC7571BEE1C` yields `2CFF149C50E54557228E7DE60B3EB7C9`, SHA256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`, failing original K04 commitment `930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0`.
- K08 final personal caption exact words absent; N02/N06 drafts, N17/N18 explicitly other envelopes, mail11/mail20 descriptive and N23 points to unpreserved original margin. No new accepted key found.

## Contributed work
- `results/h17-k04-multiple-source-ambiguity.md`: formalizes three independently necessary K04 assertions: mask copied from commissioning transcription (appears exactly once in case), job mapping from labels transcription, and unchecksummed ACK payload reconstruction. XOR + hash disagreement cannot *identify which assertion* was wrong; warns against treating spool-byte corruption as the only possible source error. Includes precise source anchors, conditional algebra, and falsifiable evidence requirements.
- `communications/broadcast/2026-10-18T0245Z_agent35-k04-integrity-gate.md`: share provenance caveat with other agents.
- Added one qualified source-layer sentence linking note from `results/README.md`, and verified remote fetch.

## Future priorities
- Seek a **new independently supported local source carrier or transformation**, instead of recomputing prior spool mutation or K08 n-gram searches. New hypothesis needs original anchor, provenance mechanism, reduction, discriminating prediction, original hash PASS.
- Avoid overinterpreting solvability assertion in root README. K04/K08 remain null until accepted. No ungrounded manufactured solutions.
