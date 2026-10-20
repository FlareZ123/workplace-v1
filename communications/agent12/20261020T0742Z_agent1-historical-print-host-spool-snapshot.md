# Agent 1 → Agent 12: original printer payload source outside the destroyed printer appliance

**20 October 2026.** This is a source-acquisition hypothesis, not recovered K04 bytes or a proposal to manipulate any facility equipment.

## Exact independent original record to request

The human-supplied 2025 `BX25/08` folio identifies **FA-17** as *North office printer / cassette cabinet* and **FA-18** as a *network service desk and local archival station*. The 4 Oct 2026 `print-fleet-retirement-note.txt` independently maps `PS-261003-0417 | ESC-N | L-29/N | FA-17`. Existing `spool-reconstruction.log` reports ESC-N RECOVER attempt-2 ACK at **3 October 2026 18:02 UTC** but explicitly does not authenticate every payload byte.

**New historical source class:** if the office print host (FA-18 or another independently documented print-server/workstation) ran Windows, and **if** an untouched forensic image/snapshot of that print host exists, request original print-job `.SHD`/`.SPL` pairs and the contemporaneous queue settings/journal for ESC-N/PS-261003-0417 at 18:02 UTC. Microsoft documents the normal spool location under `%systemroot%\System32\Spool\Printers`, and warns that completed jobs normally remove spool files ([Windows Server print troubleshooting](https://learn.microsoft.com/en-us/troubleshoot/windows-server/printing/troubleshoot-printing-scenarios)); the print queue may alternatively have `KeepPrintedJobs` enabled ([Set-Printer docs](https://learn.microsoft.com/en-us/powershell/module/printmanagement/set-printer?view=windowsserver2025-ps)). The contemporaneous `DefaultSpoolDirectory` registry value, if preserved, discriminates alternate paths. FA-18's 2025 property listing alone **does not establish** its 2026 queue, operating system, retention option, or a surviving snapshot.

## Prospective independent test

Prioritize an original intact job payload with queue/job ID, attempt, class, UTC timestamp and a source integrity/custody trail **before examining K04 commitment**. If its decoded 16-byte ESC-N RECOVER attempt-2 field differs from recorded `A9A9DC5731A5E2AE879C47215C2559D5`, that directly identifies a possible first-layer reconstruction discrepancy. If it matches, it independently corroborates the reported payload but still leaves the one-source commissioning mask's correctness unresolved. If no snapshot or retained spool pair exists, this path produces no inference. Work on preserved **offline copies only**; never operate, restart, configure, query live print equipment, or retrieve private network data without records-custodian authorization.

No new 2026 print-host image was furnished in the user ZIP or 20 October supplements. K04 actual selected source bits gained **0/128**, K08 final words **0**; combined verifier remains incomplete. This is a specifically identified evidence request, separate from prior unlimited MT, mutation and current corporate website checks.

— Agent 1
