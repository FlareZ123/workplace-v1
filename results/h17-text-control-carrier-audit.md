# H-17 text formatting and control-byte carrier audit

**Agent 15, 18 October 2026.** Scope: the original 43-member H-17 preservation export, reproduced from the supplied ZIP; analysis covers all **42 UTF-8-decodable text files**. The TRP2 `trip-recorder.raw` binary member is excluded, because its arbitrary byte values are recorder measurements rather than textual formatting. The [read-only scanner](check_h17_text_controls.py) includes in-memory positive controls. The original result covers the 43-member uploaded ZIP; after the 18 October maintainer deletion of `resources/AGENT_PROMPT.txt`, use the scanner's `--root` argument pointing to an extracted **original ZIP** to reproduce all 42 text-file observations, or use current repository `resources/` for the 41-file current text subset. The original anomalous-byte counts are unchanged in the subset.

## Why examine this class

The missing K08 keeper phrase is referred to as a desk *margin* and *caption*; the recovered files include OCR-like procedure scans, correspondence and note extracts. An overlooked text-only carrier could in principle survive as zero-width Unicode, unusual nonprinting characters, trailing-space patterns, tabs, carriage returns, or a UTF-8 BOM. This audit tests these specific encodings in raw extracted bytes. It does not assume a hidden caption exists.

## Measurements

- Exactly **42** original non-binary members decode as strict UTF-8, with no UTF-8 BOM.
- Across them, the only code point above U+007F is one U+2014 em dash in `START_HERE.md`'s title. No zero-width Unicode or other non-ASCII characters occur.
- The only ASCII control character apart from normal LF is **U+000C form feed**, occurring **11 times** in `evidence/procedures/RC-17-scans.txt`. These 11 page separators divide its 12 printed procedure sections and are consistent with ordinary scanner pagination; they are not an independently authenticated desk caption.
- **Zero** tab characters, CR characters, NUL bytes, UTF-8 BOMs, or text lines ending in ASCII spaces or tabs.
- In-memory detection controls insert U+200B, TAB, trailing space, and UTF-8 BOM separately; all trigger their expected detector fields.

The text source bytes are preserved; the script does not edit, normalize, or rewrite them.

## Interpretation

This closes a narrow class of **raw text formatting** carriers for the missing caption. It does not rule out acrostics, word-position ciphers, ordinary visible text paraphrases, transformed binary data, unexported original margin writing, or an exact caption reconstructible through some independently evidenced rule. The preserved notes still do not quote the authenticated exact final K08 phrase. K04 remains unresolved independently.

For the overall status and source sufficiency matrix, see [README.md](README.md) and [h17-source-sufficiency-matrix.md](h17-source-sufficiency-matrix.md). The canonical partial candidate retains **six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted=false**.


## Missing-original source guard (Agent 15, 18 October 2026)

The original scanner already restricted directory traversal to the preserved manifest, but unlike its companion all-file carrier scanner, it did not reject a directory missing case records. For example, a root missing `START_HERE.md` could still return a superficially ordinary count if an unrelated file happened to occupy its place. The hardened [read-only scanner](check_h17_text_controls.py) now asserts that every original manifest path is present, permitting only the one documented repository-side deletion of `AGENT_PROMPT.txt`. A deliberately truncated case raises `ValueError` naming the missing path, before its formatted-text census is returned.

The existing [source-scope SFT](test_h17_text_source_scope.py) now includes an explicit negative control that deletes `START_HERE.md` in a disposable copied tree and requires scanner rejection. Earlier ZIP-mode generated-work and missing-source controls for the companion omission scanner remain included. The manual-only [regression run 39175347395](https://github.com/FlareZ123/workplace-v1/actions/runs/39175347395), pinned to commit `a23a01638114bc22a6e79fe8ce9c919f4cde6b1a`, passed all validation stages. The original 43-file text-control observations and the six-of-eight recovery status are unchanged. This is a coverage-reliability correction, not a newly recovered K08 phrase.
