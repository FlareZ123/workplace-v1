"""Exact joint K04 target quotient for every hypothetical single future MT state word.

This regression targets the historical mistake of testing only individually fixed
bits instead of the full joint target dimension. It reuses Agent29's source-pinned
original printer parser and MT19937 symbolic generator.

Usage: python agents/agent20/k04_exact_future_quotient_sft.py ORIGINAL_CASE.zip

The selected printer row129 bytes, mask, K04 commitment and verifier are never read.
No observed external donor or coupon bytes are inferred by this rank-only test.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
DONOR_SCRIPT = ROOT / "agents/agent29/k04_future_donor_sft.py"
FIXTURE = ROOT / "results/h17-k04-source-consistent-index955.json"
EXPECTED = [
    (1185, 31), (1411, 30), (1412, 32),
    (1865, 30), (1866, 32), (1974, 1),
]

spec = importlib.util.spec_from_file_location("h17_agent29_source_donor", DONOR_SCRIPT)
assert spec is not None and spec.loader is not None
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


def main(archive_path: Path) -> None:
    with ZipFile(archive_path) as archive:
        words, _recorder, _procedure = source.original_source(archive)
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    starts = fixture["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    assert fixture["source_spool_sha256"] == source.SPOOL_SHA

    expressions = source.symbolic_mt(2250)
    baseline: dict[int, int] = {}
    for row, start in enumerate(starts):
        if row == 129:
            continue
        for word in range(4):
            for equation in expressions[start + word]:
                source.add_vector(baseline, equation)
    assert len(baseline) == 15305

    target_joint = baseline.copy()
    for word in range(4):
        for equation in expressions[starts[129] + word]:
            source.add_vector(target_joint, equation)
    assert len(target_joint) - len(baseline) == 128
    print("original_source_rank", len(baseline),
          "source_plus_symbolic_target_rank", len(target_joint))

    informative = []
    for index in range(971, 2251):
        source_with_donor = baseline.copy()
        joint_with_donor = target_joint.copy()
        for equation in expressions[index]:
            source.add_vector(source_with_donor, equation)
            source.add_vector(joint_with_donor, equation)
        donor_gain = len(source_with_donor) - len(baseline)
        nuisance_gain = len(joint_with_donor) - len(target_joint)
        target_quotient_gain = donor_gain - nuisance_gain
        if target_quotient_gain:
            informative.append((index, target_quotient_gain))
    assert informative == EXPECTED, informative
    print("future_indices_tested", 1280)
    print("exact_joint_quotient_hits", informative)
    print("other_individual_donors_with_target_gain", 0)
    print("selected_coupon_bits_actually_recovered", 0)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
