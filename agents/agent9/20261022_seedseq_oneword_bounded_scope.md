# Agent 9: bounded source-only C++ one-word seed pilot

22 October 2026, approximately 03:03 UTC.

Scope: Test a possible `std::seed_seq` seeded by one 32-bit number, using a four-word initialized MT register quartet recovered from intact printer rows. The inferred quartet is `6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`. Only phases 0 through 620 within a 624-word initialized register are considered. This is conditional on an undocumented printer producer and epoch, and therefore has no authenticated selected-coupon implications.

**Actual finite pilot:** 524,288 numerical seeds from 0 inclusive to 524,288 exclusive; 621 source-state phase comparisons per seed. Original first-word matches: 0; original complete four-word matches: 0. Wall time 8.62 seconds on the available host. A synthetic independent seed `BEEF1234` with a known quartet at phase277 passes the same lookup. Absence of a first-word hit in this tiny fraction of the 32-bit seed domain is unsurprising and cannot exclude a general one-word seed producer.

A full 2^32-space scan would take approximately 19.6 hours at the measured single-process rate before parallelism, and lacks evidence of a shared C++ producer/epoch. Stop rather than expand the search or launch CI. Candidate selected RECOVER output, copied route mask, original slot commitments, and final caption were not used.

A separate earlier source-only PTW-417-to-printer same-ID `seed_seq` seed pilot tested 260 candidates against the *earlier intact* PS-0417 LABEL, 0 hits. Its synthetic control was strengthened to pass through the full enumeration at offset23. Neither trial yields a valid selected coupon or final words. The six accepted REC8 components remain intact; K04 is missing 128 authenticated bits, K08 lacks a final exact inscription.

Local reproducer names: `agent9_seedseq_oneword_heldout.cpp` and `agent9_417_seedseq_holdout.cpp`, under this invocation's `/mnt/data/h17-new/work/`. No resources or verifier modified.
