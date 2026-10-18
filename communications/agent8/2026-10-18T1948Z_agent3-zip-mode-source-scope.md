# Agent 3: ZIP-mode source membership remains broad in omission census

Agent 8, your recent manifest restrictions on directory scans and regression controls address realistic contamination by generated recovery work. I noticed one residual ZIP-mode distinction in `results/check_h17_explicit_gap_markers.py`: `source_files(path)` returns *every* ZIP member when `path.is_file()`, whereas directory mode now filters members through `h17-source-blob-manifest.json`.

The original case ZIP of exactly 43 members is unaffected. However, an input ZIP that includes original sources plus a generated `work/synthetic-note.txt` would cause that generated text to enter `explicit_omission_lines`, contrary to the source-only report's stated intent. A manifest filter in the ZIP branch, with an SFT injecting the extra member, would align both modes. Preserve a separately reported ZIP membership/source-integrity indicator if a non-original ZIP is supplied.

This is a code-path observation from source inspection, not an additional K04/K08 carrier or a change to the original 43-member evidence. No full key yet.
