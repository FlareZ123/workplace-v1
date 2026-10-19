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

def word_edit_distance(left, right):
    row = list(range(len(right) + 1))
    for i, left_word in enumerate(left, 1):
        next_row = [i]
        for j, right_word in enumerate(right, 1):
            next_row.append(min(
                row[j] + 1,
                next_row[j - 1] + 1,
                row[j - 1] + (left_word != right_word),
            ))
        row = next_row
    return row[-1]


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
        draft_a = tokens(lines[next(
            i for i, line in enumerate(lines) if line.startswith("N02 /")
        ) + 1].split(": ", 1)[1])
        draft_b = tokens(lines[next(
            i for i, line in enumerate(lines) if line.startswith("N06 /")
        ) + 1].split(": ", 1)[1])
        overlap = set(draft_a) & set(draft_b)
        distance = word_edit_distance(draft_a, draft_b)
        assert overlap == {"the"} and distance == 12
        print(f"N02->N06: shared word types={sorted(overlap)}; edit distance={distance}")
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

        census = []
        for i, line in enumerate(lines):
            match = re.match(r"^N(\d{2}) / (\w+)", line)
            if not match:
                continue
            raw_line = lines[i + 1]
            target_line = raw_line.split(": ", 1)[1] if ": " in raw_line else raw_line
            target_words = tokens(target_line)
            remaining = "\n".join(
                note for j, note in enumerate(lines) if j != i + 1
            )
            contexts = [remaining] + other_texts
            lexicon = set().union(*(set(tokens(t)) for t in contexts))
            oov = set(target_words) - lexicon
            exact_quote = any(
                " ".join(target_words) in " ".join(tokens(t))
                for t in contexts
            )
            census.append((int(match.group(1)), match.group(2), len(oov), exact_quote))
        assert len(census) == 24
        assert sum(bool(x[2]) for x in census) == 20
        assert sum(x[3] for x in census) == 2
        emily = [row for row in census if row[1] == "Emily"]
        assert len(emily) == 8 and sum(bool(x[2]) for x in emily) == 6
        print("all 24 notes: 20 have withheld-word OOV; 2 retain exact quotation")
        print("Emily subset: 6 of 8 OOV; quoted exceptions N17/N18")


if __name__ == "__main__":
    diagnose(sys.argv[1])
