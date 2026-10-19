"""K04 source-only categorical filter over Agent41's existing ordered donor corpus.

Run: python agents/agent7/k04_dest_filter_ordered_donors.py original-case.zip
Does not inspect any K04 selected ACK, XOR mask, nonce or commitment.
"""
import hashlib
from pathlib import Path
import sys
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "agent41"))
from k04_hidden_window_run_attack import (
    HASHES, procedure_runs, recorder_runs, temper
)

SOURCES = {
    "recorder": "evidence/recorder/trip-recorder.raw",
    "procedure": "evidence/procedures/RC-17-scans.txt",
}


def early_allowed(codes):
    for finish in range(4, 9):
        if all(
            code in ((6, 7) if 4 + i < finish
                     else (4, 5) if 4 + i == finish
                     else (3, 4, 5, 6, 7))
            for i, code in enumerate(codes)
        ):
            return True
    return False


def main(source):
    with ZipFile(source) as archive:
        data = {k: archive.read(path) for k, path in SOURCES.items()}
    for key, raw in data.items():
        assert hashlib.sha256(raw).hexdigest() == HASHES[key]

    runs = recorder_runs(data["recorder"]) + procedure_runs(
        data["procedure"].decode("utf-8")
    )
    assert len(runs) == 298
    a = b = 0
    for states, label in runs:
        codes = tuple(temper(state) >> 29 for state in states)
        a += early_allowed(codes)
        b += all(code >= 3 for code in codes)
    assert (a, b) == (52, 67)
    print("original_source_natural_ordered_runs", len(runs))
    print("conditional_d11_p627_ancestor_A_signature_matches", a)
    print("conditional_d11_p627_ancestor_B_signature_matches", b)
    print("joint_ordered_run_pairings_not_yet_excluded", a * b)
    print("original_88_804_pairs_already_sha_tested_by_Agent41", True)
    print("new_checksum_matches_claimed", 0)
    print("K04_K08", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python agents/agent7/k04_dest_filter_ordered_donors.py "
            "original-case.zip"
        )
    main(Path(sys.argv[1]))
