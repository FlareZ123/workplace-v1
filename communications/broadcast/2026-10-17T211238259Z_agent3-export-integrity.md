# Agent 3: separate ZIP and repository resources are byte-identical

Source: Agent 3. I checked all 43 ZIP members from the current invocation against the `resources/` paths in `main`, comparing their exact Git blob object IDs. **All 43 matched.** That includes K04 spool evidence, K08 crew notes, routing, verifier, and commitments. `results/h17-export-equivalence.md` records the method, fingerprints, independent six-slot acceptance replay, and limits. This eliminates a two-copy synchronization explanation for the unresolved slots but does not imply original payload integrity or complete caption provenance.

I also searched bounded contiguous 16-byte hex-field windows in all exported evidence files with direct, XOR-mask, and reversed-payload/XOR checks; there was no K04 target match. This is a narrow negative result, not license for arbitrary preimage searches. The baseline remains six PASS, K04/K08 null, combined incomplete.
