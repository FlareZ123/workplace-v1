# H-17 K08: three anchored desk-note fragments (Agent 1)

**Date:** 17 October 2026. **Status:** NO_MATCH in the precise search class below. K08 remains unresolved, and the complete REC8 envelope remains unverified.

## Motivation and source

Emily described the final caption through three image families: a room made ready after a watch (mail/11 and N02), the end-of-night mugs and lamp (N13), and the sea/voices at the table (N20). The personal final margin is not quoted in the surviving export, so this experiment deliberately tests only a bounded, *hypothetical* cut-and-paste mechanism; it does not infer that Emily composed this way.

Read-only source: `resources/evidence/crew/noticeboard-and-desk-notes.txt`, SHA-256 `13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb`. Acceptance and nonce are read from the unchanged original `resources/acceptance.json` and `resources/evidence/recovery-routing.json`.

## Exact candidate class

The reproducible standard-library program [k08-three-anchors.py](k08-three-anchors.py) parses N02 text after the introductory colon, full N13 text, and N20's first sentence. It selects **every unique contiguous 2–8-word fragment** touching at least one of the specified anchors in its own source:

| Source | Anchor set | Distinct spans |
| --- | --- | ---: |
| N02 | watch, room, hands | 46 |
| N13 | night, mugs, window, lamp | 85 |
| N20 | sea, voices, table | 62 |

Each candidate uses **exactly one span from each source**, in all six source orders, with each of two separators selected from `" "`, `" and "`, `" while "`. Apply the route's normalized UTF-8/HMAC-SHA256 nonce rule, truncate to 16 bytes, SHA-256 the component, and compare to the unchanged K08 acceptance hash. A positive control derives N02's previously checked component `BF889359B0303F2B2B2FD96AE841210B` before enumeration.

## Observed result and interpretation

**13,090,680 complete candidate assignments tested, zero acceptance matches** (`46 × 85 × 62 × 6 × 3 × 3`). This excludes this particular three-anchored, word-exact, ≤8-word-span / two-connector grammar. It is separate from the existing pairwise-span and ordered-subsequence tests. Some assignments may yield identical normalized captions, so the number reports tested assignments rather than a guaranteed count of distinct phrases.

This test does **not** authenticate any wording, disprove arbitrarily phrased captions, or establish which part of the absent final margin is missing. Captions with other vocabulary, more or fewer spans, different ordering/joiners, or entirely original wording remain possible. The evidence boundary stays unchanged: seek an authenticated final margin, original envelope, or verbatim contemporaneous quotation; use the original unmodified acceptance inventory to check any proposed wording. K04 also remains unresolved.

## Reproduce

From a repository checkout with `resources/`: `python results/k08-three-anchors.py`. The script is read-only and uses only Python's standard library. It also accepts an unpacked case folder in place of `resources/` when run from that folder's `work/` subdirectory.
