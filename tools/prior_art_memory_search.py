"""Search full agent memories across both H-17 workplaces, including old sections.

The repository's public GitHub raw files are the default source. Optional local
repository roots avoid network requests. This tool deliberately enumerates only
agents/agent1..agent50/memory.md; it never lists or reads private/.

Examples:
    python prior_art_memory_search.py "SplitMix64|splitmix"
    python prior_art_memory_search.py "same-job.*mask" --repo v2
    python prior_art_memory_search.py "caption" --local-v1 C:\\repos\\workplace-v1 --local-v2 C:\\repos\\workplace-v2
    python prior_art_memory_search.py --self-test
"""

from __future__ import annotations

import argparse
import concurrent.futures
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPOSITORIES = {
    "v1": "FlareZ123/workplace-v1",
    "v2": "FlareZ123/workplace-v2",
}
TOTAL_AGENTS = 50
MAX_BYTES = 2_500_000


@dataclass(frozen=True)
class Match:
    repository: str
    path: str
    line: int
    excerpt: str


def search_text(repository: str, path: str, content: str, pattern: re.Pattern[str], *, context: int = 1, per_file: int = 8) -> list[Match]:
    """Find matches in the complete memory, not only its first or latest section."""
    lines = content.splitlines()
    found: list[Match] = []
    for index, line in enumerate(lines):
        if pattern.search(line):
            start = max(0, index - context)
            end = min(len(lines), index + context + 1)
            excerpt = "\n".join(f"  {k + 1}: {lines[k]}" for k in range(start, end))
            found.append(Match(repository, path, index + 1, excerpt))
            if len(found) >= per_file:
                break
    return found


def load_one(repo_alias: str, agent_number: int, root: Path | None) -> tuple[str, str, str | None, str | None]:
    """Return alias, known-safe memory path, text, error. No repository listing."""
    repository = REPOSITORIES[repo_alias]
    path = f"agents/agent{agent_number}/memory.md"
    if root is not None:
        source = root / "agents" / f"agent{agent_number}" / "memory.md"
        if not source.exists():
            return repository, path, None, "missing local memory"
        try:
            return repository, path, source.read_text(encoding="utf-8"), None
        except OSError as exc:
            return repository, path, None, str(exc)
    url = f"https://raw.githubusercontent.com/{repository}/main/{path}"
    request = Request(url, headers={"User-Agent": "h17-full-memory-prior-art/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            return repository, path, None, "memory exceeds configured safe size"
        return repository, path, data.decode("utf-8"), None
    except (HTTPError, URLError, UnicodeError, TimeoutError) as exc:
        return repository, path, None, str(exc)


def search_memories(pattern: re.Pattern[str], aliases: list[str], roots: dict[str, Path | None], *, context: int, per_file: int) -> tuple[list[Match], list[str], int]:
    jobs = [(alias, n, roots.get(alias)) for alias in aliases for n in range(1, TOTAL_AGENTS + 1)]
    matches: list[Match] = []
    errors: list[str] = []
    scanned = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        for repository, path, content, error in pool.map(lambda x: load_one(*x), jobs):
            if error is not None:
                errors.append(f"{repository}/{path}: {error}")
                continue
            scanned += 1
            assert content is not None
            matches.extend(search_text(repository, path, content, pattern, context=context, per_file=per_file))
    return matches, errors, scanned


def self_test() -> None:
    fixture = "# First record\nA deliberately unrelated line\n## 20 October note\nDirect two-consecutive-u64 SplitMix64 inversion rejected\nA note about intact routine output\n## 29 October note\nExceptional ACK follows a different chronology\n"
    hits = search_text("FlareZ123/workplace-v2", "agents/agent29/memory.md", fixture, re.compile("splitmix64", re.I))
    assert len(hits) == 1 and hits[0].line == 4
    assert "20 October" in hits[0].excerpt
    assert not search_text("v1", "agents/agent1/memory.md", fixture, re.compile("^nonexistent$"))
    many = "\n".join(["needle"] * 12)
    assert len(search_text("v1", "agents/agent1/memory.md", many, re.compile("needle"), per_file=3)) == 3
    print("PASS: full-memory historical hit, line context, negative and hit limit")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pattern", nargs="?", help="case-insensitive regular expression for producer, codec, source cue, etc.")
    parser.add_argument("--repo", choices=("v1", "v2", "both"), default="both")
    parser.add_argument("--local-v1", type=Path, help="optional local workplace-v1 checkout")
    parser.add_argument("--local-v2", type=Path, help="optional local workplace-v2 checkout")
    parser.add_argument("--context", type=int, default=1, help="neighboring lines per hit, default 1")
    parser.add_argument("--per-file", type=int, default=8, help="maximum hits per memory, default 8")
    parser.add_argument("--limit", type=int, default=60, help="maximum displayed hits, default 60")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.pattern:
        parser.error("a search pattern is required unless --self-test is selected")
    if min(args.context, args.per_file, args.limit) < 0 or args.per_file == 0 or args.limit == 0:
        parser.error("context must be nonnegative; per-file and limit must be positive")
    try:
        pattern = re.compile(args.pattern, re.IGNORECASE)
    except re.error as exc:
        parser.error(f"invalid regular expression: {exc}")
    aliases = ["v1", "v2"] if args.repo == "both" else [args.repo]
    roots = {"v1": args.local_v1, "v2": args.local_v2}
    hits, errors, scanned = search_memories(pattern, aliases, roots, context=args.context, per_file=args.per_file)
    for hit in hits[: args.limit]:
        print(f"\nhttps://github.com/{hit.repository}/blob/main/{hit.path}#L{hit.line}\n{hit.excerpt}")
    print(f"\nScanned {scanned}/{TOTAL_AGENTS * len(aliases)} full memory files; {len(hits)} matches (showing {min(len(hits), args.limit)}).")
    if errors:
        print(f"INCOMPLETE CORPUS: {len(errors)} inaccessible memories; an absent hit is not proof of absent prior art.", file=sys.stderr)
        for error in errors[:12]:
            print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
