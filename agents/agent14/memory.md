# Agent 14: H-17 direct-carrier evidence search

Identity claimed 2026-10-17T23:34:00.750Z, invocation counter advanced 16 to 17. Repo: FlareZ123/workplace-v1.

## Verified baseline

Original REC8/1 acceptance is still 6 PASS (K01/K02/K03/K05/K06/K07), K04 and K08 MISSING, combined INCOMPLETE/accepted false. See results/h17-candidate.json and results/h17-verify.json. Strong source-provenance context and bounds in results/README.md and results/h17-source-rule-consistency.md. Other agents already tested massive K04 bit flips, word replacement/reassembly, retry mosaic and K08 draft-fragment grammars; do not duplicate these.

## My investigation

Expanded direct-source carrier extraction over the entire local 43-member ZIP rather than only spool job fields and crew notes. Reproducible read-only script at results/check_h17_all_carriers.py; report results/h17-all-file-carrier-bound.md; synthesis updated in results/README.md.

All 43 original files tested: 108,021 raw 16-byte sliding windows and 432 decoded windows from 32-hex-character runs for K04: 0 matches to fixed XOR/SHA256 acceptance. Across 42 valid UTF-8 source files (trip-recorder.raw excluded only from text), 618,316 contiguous normalized 1–40-word spans for K08: 0 matches to fixed nonce HMAC/truncated-component SHA256 acceptance. Positive-control scanner runs, using synthetic targets derived from actual ACK payload and N01 caption, locate both carrier types.

These are finite, source-grounded negative scopes. They do not rule out damaged/split/alternate-encoded coupon or original caption paraphrase absent from export. Preserve originals and unchanged verifier. Avoid inferring impossibility from a negative test.

## Next useful lines

- Seek evidence-based alternate encodings only if an observed artifact supports one; avoid arbitrary brute-force searches.
- If pursuing source-sufficiency, focus on exact carrier format, reported corruption mechanisms, internal consistency of spool, and archival provenance anomalies rather than K04 random payload preimages.
- For K08, look for a genuinely authenticated exact final-caption quotation/other local carrier rather than expanding improbable sentence grammars.
- Check communications/broadcast/ for Critic warnings and agent overlap.
- At every persistent checkpoint compare actual clock to the lease claimed_at. After >=70 min, preserve state, delete lease as final action; before threshold, continue productive research.

## Additional direct carriers and packaged replay

- Extended results/check_h17_all_carriers.py to check the **final 16-byte K04 and K08 component preimages directly** (raw and hex) in addition to the K04 masked coupon and K08 text spans. Zero hits in 108,021 raw windows and 432 decoded hex windows. Updated results/h17-all-file-carrier-bound.md and results/README.md.
- Created results/h17-source-sufficiency-matrix.md (linked from results/README.md): separate original-source claims, original reduction, visible carriers, source-integrity limitations, chronology and acceptance gates for K04/K08.
- Generated invocation-local /mnt/data/h17-recovery-workpack-agent14.zip containing all 43 original file contents under resources/, candidate, original-verifier JSON, source hashes, and expanded read-only direct-carrier scanner. Independently extracted ZIP, byte-compared all 43 members to original, reran unchanged verify.py (6 PASS/INCOMPLETE), reran scanner (counts 108021/432/618316, zero matches). ZIP SHA256 75bbd8ae28c9c06e6635b9d384e31868d41455b2bd07473b6fc9525fff7734b6. Invocation-local path is not persistent across future agents; repository artifacts are authoritative.
- A broadcast attempt returned a concrete safety-tool error; results and central README are already committed. Avoid repeated identical blocked action.

## Direct-component scanner positive controls

Executed two additional synthetic-commitment controls against exact original file members using expanded search: direct raw K04 component equals the 16-byte spool header at offset 0; direct hex K08 component equals first 16-byte hex PAYLOAD at offset 167 of spool. Both matched. Added this self-test mode to results/check_h17_all_carriers.py, updated report. No original K04/K08 acceptance hits.

## Source-logic challenge and prioritization refinement

Read original route/acceptance/custodian records and mail/11, mail/13, mail/16, mail/20, all 24 crew notes, entire mail thread, original spool and existing multi-agent research. No independent printer ECC/checksum or authenticated final-caption carrier emerged. Original K04 last ACK is unique under explicit route and class; the email chronology discrepancy remains unreconciled, cannot manufacture a corrected payload. Prior agents already test all declared near-copy/mutation classes, and Agent12 now published original-verifier synthetic acceptance-path positive/negative controls. New Critic broadcast on 17 Oct 23:56 directs evidence-first local inference, no further unguided hash-radius sweeps.

Extended results/h17-source-sufficiency-matrix.md: under explicitly hypothetical independent-uniform three-retry model, probability all bytes are pairwise distinct at 16 aligned positions = 0.828520889731717; 32 unanimous bit positions is exactly null expectation. This supports no near-copy redundancy without asserting the actual device is random. Also documented 2^128 K04 candidate domain and the 5.699B Hamming≤6 assignments covering only 1.67484295016e-29 of it absent a source-backed near-error prior. These are conditional mathematical bounds, not recovered bytes.

## Incarnation begun 18 October 2026 23:21:59.843Z

Actual random mode draw was **7** (normal research). Reclaimed Agent 14 through a current-branch contents-API commit `7d2a456e`, read back lease `783f12fe-f399-4bd7-96e8-07a77380f198` at the original UTC claim time. Reviewed current repository README, full results/README.md, own source-sufficiency matrix, recent Critic evidence-first allocation guidance, and current mail. Agent32 independently reproduced all-file-carrier negative scopes; Agent15 requested an original-source cross-record discriminator.

I independently re-extracted the original 43-member ZIP (SHA256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`), directly reread original custodian/routing/archive-labels/spool and all 20 email messages + 24 crew notes. Re-ran **unchanged original** `verify.py` on six accepted known values and observed exit code 1: K01/K02/K03/K05/K06/K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false. This is a baseline consistency check, **not** another full replay or an added recovery component. Original case input bytes untouched; invocation-local workspace `/mnt/data/H17_original_20261019` not durable across future runs.

Sent source-grounded reply to Agent15 at `communications/agent15/2026-10-18T2331Z_agent14-source-relation-response.md` (commit `4467ae45`). Analysis matches existing `results/h17-k04-multiple-source-ambiguity.md`: the single mask transcription, single retained payload, separate ACK, and non-independent early mail reference cannot isolate a bad mask vs payload. Final keeper caption is described but never quoted in retained original records. No additional locally supported discriminator has been found. Do not repeat old 128-row bitplane, arbitrary mask, phrase grammar or bounded hash search without a new original-record anchor. The user has not requested an incomplete handoff; do not prepare or send a transient six-slot recovery package.

Further investigative direction: prioritize a genuinely new deterministic original-source relation that provides a non-hash falsification step, or identify a material defect in an already relied-on evidence reduction. Confirm source membership if scans are rerun. At persistence checkpoints, measure elapsed against immutable claim `2026-10-18T23:21:59.843Z`; orderly release only at >=70 minutes.


## 20 October 2026 ~04:16Z normal invocation: new K04 TRP2 three-lane source prediction

- Actual uniform mode draw **6/10** in first step; claimed eligible Agent14 lease run `h17-agent14-k04k08-new-target-crack-20261020-4f26` at immutable **2026-10-20T04:15:57.642Z**. Remote commit `e96b6a7` and exact fetched lease confirmed. After each persistence checkpoint compare actual UTC time with that timestamp; orderly release only when lease age >=70 minutes.
- User expressly requires genuinely new K04/K08 cracking and forbids endless canonical replay/packages. No six-slot replay, no package, no original resource/checker/commitment changes. Current canonical accepted six only, K04 target bits0, K08 exact words0.
- **New source-driven producer/order hypothesis with genuine withheld original matches:** original TRP2 node49/event82 cohort seq200–203, seq900–903, seq990–993 correspond to three phase lanes of an interleaved 12-output MT state run indexed -396..-385 relative to printer row9; index step +3 for consecutive seq in any lane. Earlier known 6 printer↔recorder coincidences anchor the putative lane indexing; no novelty claimed for those 6.
- Used **only original intact spool rows 9,40,63,124** (MT relative starts0,229,398,852) to build an exact GF2 printer-only basis rank448, then predicted original TRP2 states without looking at the recorder controls while constructing state constraints: **CRC-bad record41 seq901=9FF49339, 32/32 printer-fixed state bits agree**, and **CRC-good record8 seq991=884AC5C6 agrees at 16/16 printer-fixed bits under mask 4DEE9E40 (expected 084A8440)**. Their new source match ties two more original controls to intact later spool two-step word equations. Agent21's older printer-only report already gave the first record's lower31 1FF49339, but not original seq901's matching full copy or seq991's 16bit masked correspondence.
- New report `results/h17-k04-trp2-three-lane-interleaving-heldout.md` committed 77588ed. Standalone original-SHA-pinned Python stdlib SFT `agents/agent14/k04_trp2_interleaved_cohort_sft.py` committed 7fe681a, independently executed locally on unchanged original ZIP with all holdout asserts passing; remote fetched verified. Tested global p955 528-spool + all12 controls via exact symbolic basis: source rank15305→15433 but K04 selected quotient128/128, *no actual selected bits*. Source source-independent match is promising about upstream order, not historical physical producer/phase or target recovery; seq901 original CRC fails and cannot count as K05 eligible.
- Two targeted inter-agent notices: Agent21 `communications/agent21/20261020T0445Z_agent14_trp2-interleaving-new-heldouts.md`; Agent41 `communications/agent41/20261020T0445Z_agent14_three-lane-cohort-reordering.md`. Asked for target-window index bridge, esp seq300–303 K05 cohort, without forcing an unsupported fourth lane.
- Further SFT improvement: explicit synthetic CPython seeded MT test 1,376 recurrence equations gave zero violations. Source-only 4row model alone yields exact same 32/16 predictions; not dependent on speculative entire global p955 chronology. The physical chronology remains unresolved and four-row alignment is conditional.
- **Next:** Seek *original* producer/order coupling for TRP2 seq300–303 or separately indexed 4-word cohort near K04 target ancestor X104, X332..335, X728..731 or future states X1412/1866. Test any proposed mapping against independent heldout original intact states before target hash. Do not turn this interleaving into a target recovery claim or repeat old RNG seed family/digest scans. For K08, still no exact final margin words; demand newly supplied original quotation or source-defined edit rule.
