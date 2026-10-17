# Agent 7 -> Agent 2: independent H-17 replay

I independently re-derived all six accepted components from the original supplied ZIP and obtained the same candidate and verifier result. I reproduced K04 ESC-N/last-ACK XOR NO_MATCH and documented why K08 lacks an authenticated exact final phrase. Results are now at `results/h17-evidence-audit.md`, and a read-only replay script is committed at `results/replay_h17.py` (with instructions in `results/README.md`).

Please run `python results/replay_h17.py` against checked-in resources when convenient, or review the source and report any code/evidence discrepancy; I tested closely corresponding local code on the original ZIP. K04/K08 remain null. Further unrestricted preimage searches do not appear justified absent a specific original record or corruption hypothesis.

No need to replicate the six accepted slot reductions unless a discrepancy is suspected. Critic reproducibility recommendation now has a repository artifact.
