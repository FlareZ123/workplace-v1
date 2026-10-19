"""Original-source GF2-consistent K04 index955 with upper-bit oracle sensitivity.

Run: python agents/agent24/k04_source_consistent_oracle_sft.py original-export.zip
Reads original intact source payloads, excludes selected row129 and all REC8
commitments. Fixture is independently published by Agent50. Requires stdlib.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agents.agent33.k04_global_target_projection import source_rows, solve_target
from agents.agent24.k04_target_optimistic_leakage_sft import target_rank


def main(source):
    fixture = json.loads((ROOT / "results/h17-k04-source-consistent-index955.json").read_text(encoding="utf-8"))
    starts = fixture["row_starts"]
    assert len(starts) == 133 and starts[0] == 0 and starts[129] == 955
    rows = source_rows(Path(source))  # SHA256-checked original spool; selected row removed.
    assert rows[129] == []
    original = solve_target(rows, starts)
    assert original["source_rank"] == 15305
    assert original["target_rank_after_source"] == 128
    assert original["fixed_tempered_target_bits"] == 0
    print("Unchanged original 528-word source: CONSISTENT",
          "source_rank", original["source_rank"],
          "target_rank", original["target_rank_after_source"])
    expected = {0:(128,0), 2:(128,0), 3:(128,0), 16:(128,0),
                20:(128,0), 22:(124,4), 24:(123,5),
                26:(118,10), 28:(113,15), 30:(88,40),
                31:(76,52), 32:(0,128)}
    for bits, (quotient, fixed) in expected.items():
        source_rank, augmented_rank, rank, known = target_rank(starts, bits)
        assert source_rank == 15305 and (rank, known) == (quotient, fixed)
        print("hypothetical top bits of EVERY unprinted draw", bits,
              "augmented_rank", augmented_rank,
              "remaining_selected_bits", rank, "individually_fixed", known)
    print("These optimistic bit observations do not exist in the original export.")
    print("This index955 vector is CLASS/DEST-incompatible under Agent50's separate two-sampler gate.")
    print("No original K04 coupon bytes or K08 wording recovered.")


if __name__ == "__main__":
    main(sys.argv[1])
