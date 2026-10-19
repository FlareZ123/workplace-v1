"""Test H-17 source-derived CPython Random.seed(str) candidates without K04 hashes.

Run: python agents/agent8/k04_string_seed_fingerprint.py original-case.zip
Requires the repository's existing Agent 1, 23, and 31 MT source parsers.
The selected spool row129, route mask and commitments are excluded from discovery.
"""
import hashlib
import random
import re
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent1"))
from k04_python_seed_fragments import extract_pairs, fragments
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import untemper

TERMS = (
    "H17", "H-17", "H_17", "H17-IR-261003", "IR-261003-H17", "IR261003",
    "H17-IR261003", "H17-IR-261003", "IR-261003", "20261003", "2026-10-03",
    "03-Oct-2026", "October 3 2026", "ESC-N", "escrow", "printer", "spool",
    "archive", "recovery", "CEG", "CEG-ARCHIVE-RECOVERY/v1", "PS-261003-0417",
    "PS-261003-0300", "random", "Random", "MT19937", "rec8", "REC8/1",
    "records", "Records", "source", "simulator", "seed", "trial",
)


def string_key_words(value):
    raw = value.encode("utf-8")
    number = int.from_bytes(raw + hashlib.sha512(raw).digest(), "big")
    count = (number.bit_length() + 31) // 32
    return [(number >> (32 * i)) & 0xFFFFFFFF for i in range(count)]


def phase_index(pairs, sizes=range(17, 70)):
    """Index all two-word CPython seed-array fingerprints of the source window."""
    result = {}
    for n in sizes:
        lookup = defaultdict(list)
        for phase in range(393):
            words = fragments(pairs, phase, n)
            assert words is not None and len(words) == 2
            first = (phase + 229) % n
            second = (first + 1) % n
            lookup[(first, words[first], words[second])].append(phase)
        result[n] = lookup
    return result


def source_candidates(path):
    words, lines = set(), set()
    with ZipFile(path) as archive:
        for name in archive.namelist():
            if not (name.startswith("evidence/") or name == "START_HERE.md"):
                continue
            if name.endswith(".raw") or name == "evidence/print/spool-reconstruction.log":
                continue
            try:
                body = archive.read(name).decode("utf-8")
            except UnicodeDecodeError:
                continue
            for line in body.splitlines():
                line = line.strip()
                if (3 <= len(line) <= 120 and "[censored]" not in line
                        and "PAYLOAD=" not in line and "From:" not in line
                        and "To:" not in line):
                    lines.add(line.rstrip(".! "))
                for word in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{1,35}", line):
                    if not (re.fullmatch(r"[A-Fa-f0-9]{12,}", word)
                            or (word.isdigit() and len(word) > 8)):
                        words.add(word)

    strings = set(TERMS) | words | lines
    for word in words:
        if len(word) < 25:
            strings.update(("H17-" + word, "H-17-" + word, word + "-H17",
                            word + "-20261003", word + "-IR261003",
                            "IR261003-" + word, "20261003-" + word))
    for a in ("H17", "H-17", "IR261003", "IR-261003-H17", "20261003",
              "PS-261003", "CEG"):
        for b in ("printer", "spool", "escrow", "recovery", "archive",
                  "RECOVER", "ESC-N", "Archive", "K04", "random", "MT19937",
                  "261003", "0417"):
            for sep in ("-", ":", "_", "/", " ", ".", ""):
                strings.add(a + sep + b)
                strings.add(b + sep + a)
    return strings, len(words), len(lines)


def synthetic_controls():
    seed = "H17-SYNTHETIC-SEED-PROBE"
    rng = random.Random(seed)
    outputs = [untemper(rng.getrandbits(32)) for _ in range(624)]
    words = string_key_words(seed)
    for phase in (0, 15, 195, 300, 392):
        pairs = [(outputs[phase + i], outputs[phase + i + 227])
                 for i in range(5)]
        lookup = phase_index(pairs, (len(words),))[len(words)]
        found = [p for i in range(len(words))
                 for p in lookup.get((i, words[i], words[(i + 1) % len(words)]), ())]
        assert phase in found, (phase, found)


def main(path):
    synthetic_controls()
    pairs = extract_pairs(path)[0]
    assert pairs[0] == (0x482F6361, 0xA757A2AC)
    index = phase_index(pairs)
    strings, nwords, nlines = source_candidates(path)
    with ZipFile(path) as archive:
        spool = [line for line in archive.read("evidence/print/spool-reconstruction.log").decode().splitlines() if line.startswith("2026-")]
    source_row3 = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", spool[3]).group(1))
    assert source_row3.hex().upper() == "24FF4383374867B2F2FABB2B30F72AAF"
    # Search later MT output cycles too, independently of the first-cycle index.
    control_stream = random.Random("H17-SYNTHETIC-SEED-PROBE").randbytes(8192 * 4)
    assert control_stream.find(control_stream[6500 * 4:6500 * 4 + 16]) == 6500 * 4
    full_matches = []
    matches = []
    for candidate in sorted(strings):
        output_stream = random.Random(candidate).randbytes(8192 * 4)
        at = output_stream.find(source_row3)
        if at >= 0:
            full_matches.append((candidate, at // 4, at % 4))
        key = string_key_words(candidate)
        n = len(key)
        if n not in index:
            continue
        for k in range(n):
            for phase in index[n].get((k, key[k], key[(k + 1) % n]), ()):
                matches.append((candidate, phase))
    print("synthetic_string_seed_controls", 5, "PASS")
    print("selected_row129_withheld", True)
    print("original_commitments_unread", True)
    print("source_words", nwords, "source_lines", nlines)
    print("source_anchored_candidate_strings", len(strings))
    print("first_cycle_phases", 393)
    print("later_cycle_synthetic_control_index", 6500, "PASS")
    print("source_dictionary_SHA256", hashlib.sha256("\\n".join(sorted(strings)).encode()).hexdigest())
    print("full_row3_matches_first_8192_outputs", len(full_matches), full_matches[:20])
    print("source_string_seed_matches", len(matches))
    print("matches", matches[:20])
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
