"""Leave-one-caption-out lexicon recoverability diagnostic for original H-17 ZIP.

Reports whether a word-extractive candidate grammar using tokens that survive
outside a held-out line could reproduce that line's exact words.
Does not test K08 commitments or infer an unknown final caption.
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
            line_index = next(i for i, line in enumerate(lines) if line.startswith(heading)) + 1
            target = lines[line_index].split(": ", 1)[1]
            remaining = "\n".join(
                line for i, line in enumerate(lines) if i != line_index
            )
            lexicon = set(tokens(remaining + "\n" + "\n".join(other_texts)))
            words = tokens(target)
            missing = sorted(set(words) - lexicon)
            print(
                f"N{number:02d}: {len(words)} words, "
                f"{len(missing)} OOV types: {missing}"
            )
            assert bool(missing) == (number in (2, 6))


if __name__ == "__main__":
    diagnose(sys.argv[1])
