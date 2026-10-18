# K04 printer-buffer fragment echoes: source-only reproduction

**Agent 4, 18 October 2026.** Outcome: no authenticated correction to K04 and no eight-slot recovery. This report records a narrow audit of literal duplication of the selected, reconstructed printer payload elsewhere in the surviving case. The source file was not modified.

## Source-supported question

The preserved `evidence/print/spool-reconstruction.log` labels the buffer a *retained-fragment export* with unverified payload integrity. `evidence/mail/16.eml` warns that ACK is a dispatch observation rather than a payload-integrity certificate. If a long contiguous piece of the selected payload happened to be copied intact in another preserved source field, that independent copy could be a useful consistency check. A string coincidence without an original-coupon provenance chain would still not authenticate it.

This literal-echo model predicts a surviving contiguous raw-byte or ASCII-hex substring of the selected entry in a different original source location. It does not predict an acceptance-committed K04 component by itself.

## Deterministic comparison

1. From original 43-member export `c-energy-group-documents2026.zip`, select the unique `JOB=PS-261003-0417 ATTEMPT=2 STATE=ACK CLASS=RECOVER` line. Recorded bytes: `A9A9DC5731A5E2AE879C47215C2559D5`.
2. Remove **that complete line** from the search corpus to prevent self-echo.
3. Measure the longest contiguous selected-payload substring repeated in all remaining original resource files, then repeat with the printer log excluded entirely. Compare the 16 raw bytes, their 32 ASCII uppercase hex nibbles, and case-insensitive ASCII hex.
4. Permit only paths in the immutable original preservation manifest. Treat the original 43-member ZIP and the current 42-file checked-in `resources/` (one documented removed instruction file) as valid scopes; exclude generated `work/` and candidate outputs.

An independent Python standard-library comparison of the original 43-member ZIP gives:

| Other-file corpus | Raw-byte longest echo | Uppercase ASCII hex longest echo | Case-insensitive ASCII hex longest echo |
| --- | ---: | ---: | ---: |
| All remaining original files, including printer log without selected line | 1 byte | 5 hex characters | 5 hex characters |
| Other original members, excluding printer log | 1 byte | 3 hex characters | 3 hex characters |

These are **longest contiguous substrings**, not numbers of matching candidate keys. Thus the preserved sources have no literal raw echo of two or more consecutive selected bytes elsewhere after removing its entry. They also have no other full hexadecimal copy. This does **not** establish the authentic coupon, nor exclude noncontiguous fragments, transformed representations, a damaged original selected payload or an omitted source. Tiny coincidences carry no integrity weight.

## Reproducibility correction and controls

Earlier `results/check_h17_printer_partial_echoes.py` traversed every file below its argument and asserted exactly 43 files. It therefore could not run on today's 42-file checkout and could admit generated work as supposed evidence in another accidental 43-file corpus.

The maintained scanner now filters original paths using `results/h17-source-blob-manifest.json`, permits only the documented missing `AGENT_PROMPT.txt`, reports ignored generated files, and rejects other missing original paths. A new read-only SFT `results/test_h17_partial_echoes_scope.py` tests clean/dirty output equivalence, injected complete raw/hex synthetic echoes, and rejection of a genuinely missing original source. The source corpus and acceptance commitments remain unchanged.

The manual-only `.github/workflows/h17-source-scope.yml` includes this test. [Workflow run 39165912971](https://github.com/FlareZ123/workplace-v1/actions/runs/39165912971), tested on commit `a8577efff2f734f822bb4b332d4b81a79be9ec75`, completed **successfully** including the new regression. This is a code/source-membership validation, not a new original coupon witness.

**Recovery status remains:** K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING; combined INCOMPLETE; accepted false.
