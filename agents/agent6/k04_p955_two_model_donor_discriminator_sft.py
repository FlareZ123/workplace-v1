"""Source-only disjoint donor-pair signatures for two conditional H-17 K04 p955 chronologies.

Run at repo root: python agents/agent6/k04_p955_two_model_donor_discriminator_sft.py original-export.zip.
Never reads disputed row129 payload, K04 mask/commitments, K08 nonce or verifier.
These are incompatible conditional stream-placement models, not authenticated historical producer epochs.
"""
import json
import sys
from pathlib import Path
from agents.agent33.k04_global_target_projection import state_expressions, tempered_expressions
from agents.agent6.k04_p955_donor_pair_signature_sft import add, reduce, source_rows, twist, synthetic_controls


def model(rows, starts, shift):
    terms = state_expressions(shift + 1412)
    source = {}
    for r, words in enumerate(rows):
        for j, word in enumerate(words):
            for expr in terms[shift + starts[r] + j]:
                add(source, expr)

    def extra(positions):
        b = source.copy()
        for pos in positions:
            for expr in terms[shift + pos]:
                add(b, expr)
        return len(b) - len(source)

    target = [expr for pos in range(shift + 955, shift + 959)
              for expr in tempered_expressions(terms[pos])]

    def quotient(positions):
        b = source.copy()
        for pos in positions:
            for expr in terms[shift + pos]:
                add(b, expr)
        before = len(b)
        for expr in target:
            add(b, expr)
        return len(b) - before
    return source, terms, extra, quotient


def run(case_zip, root):
    synthetic_controls()
    rows = source_rows(case_zip)
    assert len(rows) == 133 and rows[129] == [] and len(rows[105]) == 4
    printer_only = json.loads(
        (root / "results/h17-k04-source-consistent-index955.json").read_text(encoding="utf-8")
    )["row_starts"]
    cross_source = json.loads(
        (root / "agents/agent5/k04_crosssource_six_vectors.json").read_text(encoding="utf-8")
    )["row_starts"]["955"]
    assert len(printer_only) == len(cross_source) == 133
    assert printer_only[129] == cross_source[129] == 955
    assert printer_only[105] == 789 and cross_source[105] == 786

    a, at, ad, aq = model(rows, printer_only, 0)
    b, bt, bd, bq = model(rows, cross_source, 400)
    assert len(a) == 15305 and len(b) == 15369
    assert [ad(p) for p in ((1185,), (1412,), (1185, 1412))] == [32, 32, 33]
    assert [bd(p) for p in ((1185,), (1412,), (1185, 1412))] == [32, 32, 32]
    assert [aq(p) for p in ((), (1185,), (1412,), (1185, 1412))] == [128, 97, 96, 96]
    assert [bq(p) for p in ((), (1185,), (1412,), (1185, 1412))] == [128, 96, 96, 96]

    assert ad((789,)) == 0 and ad((788,)) == 32
    earlier = twist(0, rows[105][0])
    earlier_set = {earlier, earlier ^ 0x40000000}
    assert earlier_set == {0x359EC0C7, 0x759EC0C7}
    assert bd((788,)) == bd((789,)) == 0
    later = twist(rows[105][2], rows[105][3])
    assert later == 0x903F9815
    assert later not in earlier_set

    result = {
        "printer_only_p955": {
            "source_rank": len(a),
            "pair_source_fixed_parities": 31,
            "possible_pair_xors": [f"{v:08X}" for v in sorted(earlier_set)],
            "target_rank_with_1185": aq((1185,)), "target_rank_with_1412": aq((1412,))
        },
        "crosssource_p955": {
            "source_rank": len(b),
            "pair_source_fixed_parities": 32,
            "possible_pair_xors": [f"{later:08X}"],
            "target_rank_with_1185": bq((1185,)), "target_rank_with_1412": bq((1412,))
        },
        "predicted_donor_signatures_disjoint": True,
        "historically_authenticated_stream_placement": False,
        "new_K04_original_bits": 0
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Supply unchanged original H-17 ZIP"
    run(Path(sys.argv[1]), Path(__file__).resolve().parents[2])
