"""Leave-one-caption-out exact-word and n-gram calibration on original H-17 ZIP.

This deterministic test never reads acceptance commitments or attempts K08 guesses.
It measures whether a source-only extractive grammar could reproduce known
independent Emily drafts after their exact sentence is withheld.
"""
import hashlib
import re
import sys
import zipfile

NOTES = "evidence/crew/noticeboard-and-desk-notes.txt"
NUMBERS = (2, 6, 17, 18)
SOURCE_SHA256 = "13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb"


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def grams(words, size):
    return {tuple(words[i : i + size]) for i in range(len(words) - size + 1)}


def diagnose(path):
    with zipfile.ZipFile(path) as archive:
        raw = archive.read(NOTES)
        assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
        lines = raw.decode("utf-8").splitlines()
        other_texts = []
        for name in archive.namelist():
            if name == NOTES:
                continue
            try:
                other_texts.append(archive.read(name).decode("utf-8"))
            except UnicodeDecodeError:
                pass
        for number in NUMBERS:
            heading = f"N{number:02d} /"
            index = next(i for i, line in enumerate(lines) if line.startswith(heading)) + 1
            target = tokens(lines[index].split(": ", 1)[1])
            remaining_notes = "\n".join(
                line for i, line in enumerate(lines) if i != index
            )
            contexts = [remaining_notes] + other_texts
            for size in (1, 2, 3):
                surviving = set().union(
                    *(grams(tokens(context), size) for context in contexts)
                )
                target_grams = [
                    tuple(target[i : i + size])
                    for i in range(len(target) - size + 1)
                ]
                missing = sorted(
                    {" ".join(g) for g in target_grams if g not in surviving}
                )
                print(
                    f"N{number:02d} {size}-gram: "
                    f"{len(missing)}/{len(target_grams)} absent; "
                    f"unique absent={missing}"
                )
                if size == 1:
                    assert len(missing) == (3 if number in (2, 6) else 0)
            quoted = any(
                " ".join(target) in " ".join(tokens(context))
                for context in contexts
            )
            assert quoted == (number in (17, 18))
            print(f"N{number:02d}: whole sentence retained elsewhere: {quoted}")


if __name__ == "__main__":
    diagnose(sys.argv[1])
