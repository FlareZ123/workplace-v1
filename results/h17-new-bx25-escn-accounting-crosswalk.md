# New BX25 source: ESC-N property-ticket crosswalk and acceptance gap

**Agent 16 | 20 October 2026, 02:24 UTC. New source-only finding.** Four new corporate supplements were added at maintainer commit `ca43daaec` on 20 October at 02:08 UTC. This report uses their three *readable* source files, plus the older `archive-labels.ini`; it does not examine the encrypted PDF, selected printer payload, mask or K04 commitment. No K04 coupon bit or K08 final word is recovered.

## Literal source-level chain

1. Existing original `resources/evidence/archive-labels.ini` maps the incident-date `ESC-N` logical printer route to `PS-261003-0417`. The new `resources/evidence/h17-supplemental-office-files/print-fleet-retirement-note.txt`, an 04 Oct 2026, 09:18 UTC cabinet-office reconciliation, independently **repeats the ESC-N/job association** and extends it to cabinet `L-29/N`, account `FA-17` and filing reference `H17-POL-17/A3`. This is a second **documentary assertion**, though the two transcriptions could share an unknown upstream asset card.
2. The same fleet return register explicitly lists *five* L-29/N binder ticket IDs: `ST-094`, `ST-081`, `ST-106`, `ST-099`, `ST-112`. All five appear separately as `L29,R3,POSTED,FA-17,H17-POL-17/A3` in `supplier-reconciliation-L29.csv`, with descriptions matching their register roles (lid, guide, separator, hinge, catch). This is **5/5 agreement of exact ticket IDs and the same posted account/jacket**.
3. The reconciliation separately records `RN-052,RISK,R1,FILED,FA-17,BX25/08` as a *property-annex scan inward transfer*, associating the same `FA-17` ledger with folio `BX25/08`. `retired-office-bookmarks.html` describes the historical BX25 scans as **2025 Risk renewal** material, with a four-position numeric release setting for the old desk scanner. The physical release register itself is not retained.
4. This yields a traceable accounting/document path `ESC-N/PS-261003-0417 -> L-29/N -> FA-17/H17-POL-17/A3 -> RN-052/BX25/08`. It is a **referential join**, not a direct assertion that the 2025 PDF holds a 2026 coupon or recoverable generator seed.

## Reconciliation controls that prevent false lineage

| Alternative | New original distinction | Implication |
| --- | --- | --- |
| `ESC-S/PS-261003-0448` | Fleet `L-29/S,LV-42,CS-18/5`; risk `RN-053,LV-42,BX25/12` | Cannot replace `FA-17/BX25/08` merely because ESC-S is a RECOVER route |
| `WATCH-SPARE/PS-261003-0420` | Fleet `L-29/W,ST-09,STORES/FLT`; risk `RN-047,ST-09,BX25/03` | Separate spare route, not ESC-N |
| `ST-099` prior version | `L29,R2,VOID,FA-17,H17-POL-17/A2` vs `R3,POSTED,FA-17,A3` | Do not follow the later-looking supplier line order to an obsolete jacket |
| `ST-112` subsequent version | `L29,R4,HELD,FA-17,H17-POL-17/A4` vs `R3,POSTED,FA-17,A3` | Greatest run number is not the authoritative posting; R4 is held |
| Prior L28 month | `ST-098/ST-087,L28,R3,POSTED,FA-17,A2` | Same account `FA-17` does not alone select the relevant L29 print return |
| 2025 versus 2026 | Bookmarks mark `BX25` as 2025 renewal; K04 selected ACK is 03 Oct 2026 | A 2025-only asset schedule cannot authenticate bytes of a later October 2026 job without an additional historically justified bridging rule |

## Source-first discriminants for a decrypted BX25/08

**Hold out before reading:** because `RN-052` calls this `FA-17` property-annex material, the appropriate *first* predictions are an `FA-17` ledger/asset identity or H-17 Risk/property reference. A different company or unrelated subject would challenge this document link. Merely finding `FA-17` or a printer model would **not** reveal the 2026 attempt-2 payload or validate the XOR mask.

Only if actual PDF text establishes a producer serial/seed, a dated ESC-N order rule, a separately authenticated contemporary coupon/mask or other **new target-bearing witness** should K04 inference progress. A prior-year scanner/asset listing may improve historical mapping but cannot by itself collapse the 128 target bits. K08 needs the *actual final* Emily caption; its appearance in an unrelated 2025 property annex should not be expected or inferred.

**Current information gain:** new documentary corroboration of the ESC-N to PS-261003-0417 association, a complete five-ticket accounting join, precise control exclusions and a new accessible-but-encrypted permitted source. **Recovered K04 target bits 0/128, K08 final exact words 0; unchanged REC8 incomplete.**

Original source bytes, verifier and commitments remain untouched. Agent 9 is pursuing PDF release separately; coordinate with Agent 46 on K04 relevance rather than duplicate PIN enumeration.

## Original-export novelty control (read-only byte search)

To distinguish actual **new material** from a new presentation of the established printer records, Agent16 exhaustively counted exact ASCII references (case-insensitive literal byte matches) across each of the **43 original exported ZIP members**, SHA256 `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`. The original job ID `PS-261003-0417` occurs five times: one in `archive-labels.ini` and four in `spool-reconstruction.log`. In contrast `FA-17`, `H17-POL-17/A3`, `L-29/N`, `BX25/08`, `RN-052` and `ST-094` each occur **zero** times anywhere in the original 43-file export. The 20 October office supplements therefore introduce genuinely **new verbatim identifying fields and joins**, rather than only reprinting those old archive/print references. The zero occurrence is scoped to exact literal spellings and does not prove the underlying ideas absent from other encodings.

The new references still do not identify a complete 128-bit coupon or exact K08 caption. The original export and current supplements were only read; no source was modified.
