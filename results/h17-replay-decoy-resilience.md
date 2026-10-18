# H-17 replay record-selection sensitivity controls

**Agent 14, 18 October 2026.** Original acceptance remains six passed slots, K04 and K08 missing, combined incomplete. This small read-only experiment independently tests three source-selection rules that rely on highest valid revisions, retries and exclusions. It does **not** recover a missing component.

## Independent reductions

The [control script](test_h17_replay_decoys.py) implements K02, K03 and K07 directly from original resources, independently of the already published `replay_h17.py` implementation. Each original source-derived component matches the untouched `acceptance.json` SHA256 commitment.

- **K02:** Keep `LT-204 / DIAG_WORD` rows that are GOOD and HOLD, interpreted in UTC within the half-open interval, then choose the greatest revision at each sequence index, big-endian-pack eight unsigned 16-bit integers, take the first 16 bytes of SHA256.
- **K03:** Use email 04's bay order B,D,A,C; keep only PTW-417 signed CLOSED AS_LEFT records, select greatest revision by bay, join exact serials with `|`, retain the first 16 SHA256 bytes.
- **K07:** Use email 13's AX-7782, require a COMMIT that is not a dry run, select the highest attempt per checkpoint sequence from matching transfer CHUNK records, hash concatenated eight two-byte checkpoints and take the first 16 bytes.

## Adversarial in-memory record controls

For each source, the script appends one **synthetic** row in memory, repeats the independent selection, and checks whether the resulting component's untouched slot digest remains accepted. Synthetic records are never persisted or presented as real evidence.

| Slot | Artificial record condition | Expected outcome | Observed |
| --- | --- | --- | --- |
| K02 | HIGH revision, SUSPECT quality | Ignore; original PASS | As expected |
| K02 | HIGH revision, exactly at exclusive end timestamp | Ignore; original PASS | As expected |
| K02 | HIGH revision, GOOD/HOLD within window | Replace winner; NO_MATCH | As expected |
| K03 | HIGH revision, unsigned CLOSED AS_LEFT | Ignore; original PASS | As expected |
| K03 | HIGH revision, signed CLOSED REMOVED | Ignore; original PASS | As expected |
| K03 | HIGH revision, signed CLOSED AS_LEFT | Replace winner; NO_MATCH | As expected |
| K07 | HIGH attempt for unrelated transfer AX-7783 | Ignore; original PASS | As expected |
| K07 | HIGH attempt for chosen transfer AX-7782 | Replace winner; NO_MATCH | As expected |
| K07 | Extra dry-run COMMIT for AX-7782 | Ignore; original PASS | As expected |

**9/9 in-memory controls passed** using the original 43-member export. Three original K02/K03/K07 components independently passed the original slot commitments before mutation. High ranking does not trump a disqualifying field. All valid high-rank substitutions changed the candidate and failed the corresponding unchanged acceptance hash.

## Reproducibility and limits

Run `python results/test_h17_replay_decoys.py` from a checkout containing the unchanged `resources` directory. For the original unpacked export, place the same script under `results/`. Only the Python standard library is used. No file writes or external access take place.

These controls test **finite synthetic perturbations**, not every malformed record pattern, nor the independent correctness of source selection outside K02/K03/K07. The existing replay covers all six accepted slots; this additional test is orthogonal to Agent 12's separate [synthetic complete-envelope verifier checks](h17-verifier-positive-controls.md). The actual K04 integrity contradiction and missing K08 final caption are unaffected. See [main status](README.md) and [source-sufficiency matrix](h17-source-sufficiency-matrix.md).
