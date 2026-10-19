"""Retrospective pseudo-missing-caption lexical recovery control.

Run: python agents/agent28/check_k08_leave_one_out.py resources
Never edits any original source record. This tests source-copy recoverability,
not human-blind linguistic reconstruction or actual K08 acceptance.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import sys


TARGETS = ("N02", "N06", "N17", "N18")


def tokens(text: str) -> tuple[str, ...]:
    lowered = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return tuple(cleaned.split())


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources")
    note_path = root / "evidence/crew/noticeboard-and-desk-notes.txt"
    raw_notes = note_path.read_bytes()
    assert sha256(raw_notes).hexdigest() == "13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb"
    note_lines = raw_notes.decode("utf-8").splitlines()
    paths = sorted(p for p in root.rglob("*") if p.is_file())
    assert len(paths) in (42, 43)
    sources = {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
               for p in paths if p.suffix != ".raw"}
    assert len(sources) == len(paths) - 1
    note_name = "evidence/crew/noticeboard-and-desk-notes.txt"

    results = []
    for target_name in TARGETS:
        idx = next(i for i, s in enumerate(note_lines) if s.startswith(target_name + " / "))
        target_line = note_lines[idx + 1]
        target = target_line.split(": ", 1)[1]
        expected_tokens = tokens(target)

        remaining = dict(sources)
        hidden_note_lines = list(note_lines)
        hidden_note_lines[idx + 1] = "[withheld caption]"
        remaining[note_name] = "\n".join(hidden_note_lines)
        source_tokens = {name: tokens(text) for name, text in remaining.items()}
        vocabulary = set(word for words in source_tokens.values() for word in words)
        missing_words = [word for word in expected_tokens if word not in vocabulary]

        longest = 0
        witness = []
        for size in range(len(expected_tokens), 0, -1):
            for start in range(len(expected_tokens) - size + 1):
                sequence = expected_tokens[start:start + size]
                for name, words in source_tokens.items():
                    if any(words[k:k + size] == sequence for k in range(len(words) - size + 1)):
                        witness.append({"words": " ".join(sequence), "source": name})
            if witness:
                longest = size
                break

        results.append({
            "heldout": target_name,
            "words": len(expected_tokens),
            "unseen_word_occurrences": missing_words,
            "longest_exact_other_source_span_words": longest,
            "full_other_source_echo": longest == len(expected_tokens),
            "longest_witnesses": witness[:4],
        })

    assert [(r["heldout"], r["words"], len(r["unseen_word_occurrences"]),
             r["longest_exact_other_source_span_words"], r["full_other_source_echo"])
            for r in results] == [
                ("N02", 13, 3, 3, False),
                ("N06", 11, 3, 3, False),
                ("N17", 8, 0, 8, True),
                ("N18", 5, 0, 5, True),
            ]
    print(json.dumps({"source_member_count": len(paths),
                      "normalization": "same as K08",
                      "holdout_type": "retrospective lexical witness, no generation",
                      "results": results}, indent=2))


if __name__ == "__main__":
    main()
