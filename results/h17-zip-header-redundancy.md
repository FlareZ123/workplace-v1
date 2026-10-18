# H-17 local/central ZIP header redundancy check

**Agent 8, 18 October 2026. Read-only, source-relative negative test.**

## Source-model question

Could the surviving trimmed ZIP contain a second copy of the missing K04 coupon or K08 caption in local-header fields that disagree with the decoded central-directory metadata, or in varying member attributes? These are structurally distinct carrier locations from extracted file bytes. No case record directs recovery from ZIP metadata, so this is a bounded container-forensics test.

**Predeclared prediction:** a second data-bearing local-header layer would exhibit unexpected disagreement in local versus central record fields; a member-attribute coding scheme might exhibit variation across entries. Uniform agreement would leave no observed evidence for either simple mechanism.

## Test and results

Run [the read-only standard-library reproducer](check_h17_zip_headers.py) against the unmodified uploaded ZIP (43 members, SHA-256 a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec). It compares eleven local-header fields per member with their central representations: signature, reader-version requirement, flag bits, compression method, DOS time, DOS date, CRC32, compressed length, uncompressed length, filename and local-extra-field absence.

**Observed: 473/473 checked fields consistent, zero mismatches.** All 43 members share one identical tuple of central-directory system/version/flags/volume/internal/external attributes, DOS timestamp, extra length and comment length. The 43 member names appear in lexicographic order. No new data carrier was detected.

Positive controls, applied to **separate disposable copies** of the original ZIP, each changed one byte in the first member's local header. Flipping a CRC byte yielded a reported mismatch for AGENT_PROMPT.txt / crc32; flipping a DOS-time byte yielded a mismatch for AGENT_PROMPT.txt / time. The reproducer detected both changes as predicted. No original bytes were changed.

## Interpretation

This excludes only the straightforward local/central-header disagreement and per-member attribute-variation hypotheses. A uniformly encoded constant, central-directory structure, ZIP entry ordering or arbitrary steganography is not ruled out. Missing originals could also have been omitted from the export. No new K04 coupon or K08 wording was found, hence no new acceptance result. The status remains six PASS, two MISSING. Compare the complementary [ZIP compression and padding audit](h17-secondary-evidence-audit.md), [source-equivalence audit](h17-export-equivalence.md), and [canonical recovery status](README.md).
