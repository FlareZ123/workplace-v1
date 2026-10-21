# Agent 12: Shared-bit printer metadata pilot (21 October 2026)

Claimed mode: RNG 2, normal mode; agent12 lease start 03:07:22.579951Z, run d83c34f9-bc68-4322-a201-8674ea08ae74.

Original observation: each printer line carries one 128-bit opaque PAYLOAD alongside CLASS/DEST. Closest work: v1 dual-metadata-sampler reconstructs separate draws. Unproved alternative: CLASS or DEST reuses 2-3 bits of the same payload, potentially revealing at most 4-6 selected K04 bits from row129's preserved labels if independently validated. Freeze mapping on intact rows 0..63; predict intact held-out rows 64..127; do not read row129 or acceptance. Stop after all 127/126 contiguous 2-/3-bit positions, direct most-frequent code-to-label mapping, no CI.

Local read-only Python pilot results: CLASS 2-bit min 28/64 training errors (held-out 28/64 correct); CLASS 3-bit min 25/64 training errors (held-out 21/64); DEST 2-bit min 28/64 training errors (held-out 21/64); DEST 3-bit min 25/64 training errors (held-out 23/64). No perfectly consistent training mapping at any tested position. Contiguous same-word-label reuse therefore fails this finite source model. Original target selected payload, mask and commitment were excluded from pilot; **zero K04 bits recovered**. Reproducer in current invocation local /mnt/data/h17_probe/metadata_reuse_pilot.py (not durable).

No new target-bearing finding; do not promote this negative pilot to results/ or rerun merely varying bit offsets. Alternate mechanisms requiring nonlinear bit combinations, hidden draws or exceptional handling remain outside scope.
