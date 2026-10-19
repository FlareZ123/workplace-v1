"""K04 source-only post-payload DEST sampling probe. Usage: python agents/agent2/k04_dest_sampler.py source.zip"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(root / "agent6"), str(root / "agent23")]
from k04_mt_inverse_peel import groups, rows
from k04_mt_rowstart import SPOOL
from k04_mt_ternary_class_gate import close_group, temper

dest_index = {"store": 0, "desk": 1, "bench": 2}


def main(source):
    with ZipFile(source) as archive:
        lines = [x for x in archive.read(SPOOL).decode().splitlines()
                 if x.startswith("2026-")]
    assert len(lines) == 133
    words = rows(source)
    assert words[129] == []
    observations = []
    for entries in groups(source, words).values():
        full, _ = close_group(entries, words)
        for row, start in entries:
            if row >= 128:
                continue
            samples = []
            for k in range(4, 12):
                if start + k not in full:
                    break
                samples.append(temper(full[start + k]) >> 30)
            if samples:
                dest = re.search(r"DEST=([a-z]+)", lines[row]).group(1)
                observations.append((row, dest, samples))
    observations.sort()
    accepted, rejects = [], 0
    for row, dest, samples in observations:
        accept = next((i for i, value in enumerate(samples)
                       if value < 3), None)
        rejects += len(samples) if accept is None else accept
        if accept is not None:
            index = samples[accept]
            assert index == dest_index[dest], (row, dest, samples)
            accepted.append((row, dest, index))
        print(row, dest, samples)
    assert len(observations) == 17
    assert len(accepted) == 13 and rejects == 6
    assert accepted[:3] == [(53, "store", 0), (80, "bench", 2),
                            (82, "desk", 1)]
    print("accepted_destination_witnesses", len(accepted))
    print("later_witnesses", len(accepted) - 3)
    print("observed_rejected_samples", rejects)
    print("model", "2-bit getrandbits(2) rejection-sampled destination AFTER payload")
    print("selected_row129_withheld", True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
