# Agent 1 continuity: H-17 recovery / three-anchored caption experiment

Run started 17 October 2026 at 21:48:00 UTC. Actual initial uniform 1..10 draw returned **3** (normal mode). Increased root COUNTER from 8 to 9 and claimed identity via `agents/agent1/.lease.json` with run ID `h17-agent1-20261017T214800Z`. The lease's original timestamp is immutable; do not release until after a checkpoint clock comparison shows elapsed >=70 minutes. Use `date` or equivalent actual clock. Initial claim and all subsequent commits were confirmed by GitHub API.

## Reproduced central case state

Read original uploaded ZIP `c-energy-group-documents2026.zip`, original route, custodian, spool, notes, full 20-mail bodies, independent public case reports, Critic direction and other identity memories. Unpacked a local copy at `/mnt/data/h17/`; generated `candidate.json` with six already-reported verified slots and K04/K08 as null, then ran the ZIP's **unchanged** `verify.py --candidate candidate.json --json`. Verifier: K01/K02/K03/K05/K06/K07 PASS; K04 and K08 MISSING; passed=6; combined=INCOMPLETE; accepted=false. No live system or facility hardware was contacted.

Source-selected K04 ACK attempt-2 payload `A9A9DC5731A5E2AE879C47215C2559D5`, XOR mask `8556C8CB6140A7F9A5123AC7571BEE1C`, candidate `2CFF149C50E54557228E7DE60B3EB7C9`: original K04 slot SHA-256 NO_MATCH. Original source explicitly states that ACK is not an integrity certificate. K08 final exact desk wording is not given in surviving text. Existing audits have already established byte-for-byte equivalence of 43 ZIP entries and repository resources, absence of simple ZIP metadata carriers, and a wide set of bounded negative K04/K08 searches. Do not silently promote guesses or relax acceptance.

## New reproducible bounded K08 class

The source `evidence/crew/noticeboard-and-desk-notes.txt` has SHA256 `13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb`. I hypothesized the missing caption was a 3-part exact weave from N02 (watch/room/hands), N13 (night/mugs/window/lamp), N20 (sea/voices/table). Unique 2..8-word contiguous spans containing at least one anchor: 46, 85, 62 respectively. All six note orders and both joiners chosen from [space, " and ", " while "] yielded **13,090,680 candidate assignments**, each passed through exact K08 nonce-HMAC truncation and SHA256 slot commitment. No match. Implemented a read-only Python stdlib test using pre-padded HMAC copy states, with a known N02 positive derivation control.

Committed `results/k08-three-anchors.py` and `results/h17-k08-three-anchor-bound.md`. Source hypothesis is narrow, negative only, and cannot authenticate missing original final wording. Sent a direct coordination message to Agent 3 at `communications/agent3/2026-10-17T215730Z_agent1-three-anchors.md` to distinguish from their two-fragment photo/Emily test.

I also made a quick exploratory **negative** PRNG seed probe: 24 natural seeds, 20,000 consecutive `random.Random(seed).randbytes(16)` outputs each, compared with the 133 spool 16-byte payloads in native and reversed byte order. No match. This is not credible evidence of RNG or uniqueness and is intentionally not published as a substantive result.

## Future work / limitations

- K04 requires an independently authenticated original ESC-N coupon or printer buffer/media with checked bytes; existing reconstructed ACK fails unchanged K04. Agent 3/4 exhaustive bounded bit/word/fragment scans are already extensive and do not resolve source absence.
- K08 requires final authenticated verbatim phrase (desk margin, original envelope image, contemporary quotation), absent from this export. A dictionary or grammar search can only exclude explicitly enumerated classes.
- The original combined commitment cannot be evaluated while K04 or K08 is null. All individual and combined commitments must remain unchanged.
- Existing shared source replay: `results/replay_h17.py`; human-facing synthesis: `results/README.md`. Avoid duplicating their six-slot work. No per-commit Actions workflows.

Agent 1 owns only this memory, lease, and its own report/test/message. Consult other agent broadcasts for changes. The normal-mode prompt expects productive continuation until the 70-minute lease-age checkpoint; preserve useful work periodically.
