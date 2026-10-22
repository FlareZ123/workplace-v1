"""Run a bounded public-index pilot and preserve only its short result summary."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import os
import runpy
import tempfile

capture = StringIO()
with redirect_stdout(capture):
    runpy.run_path("agents/agent27/h17_public_original_code_index_pilot.py", run_name="__main__")
summary = capture.getvalue()
print(summary, end="")
output = Path("h17-agent27-public-index-results.jsonl")
fd, tmp = tempfile.mkstemp(prefix=output.name + ".", dir=output.parent)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(summary)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, output)
finally:
    if os.path.exists(tmp):
        os.unlink(tmp)
