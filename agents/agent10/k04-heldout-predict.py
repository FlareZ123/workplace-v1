"""K04 pre-acceptance held-out printer-payload prediction gate.

Reads the original spool, route mask and metadata. Acceptance target intentionally absent.
All models are hypotheses; this is neither a payload correction nor a recovered key.
"""
from pathlib import Path
import hashlib
import hmac
import json
import re

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MASK64 = (1 << 64) - 1
STEP = 0x9E3779B97F4A7C15
STAR = 0x2545F4914F6CDD1D


def read_spool(root):
    source = (root / "evidence/print/spool-reconstruction.log").read_bytes()
    assert hashlib.sha256(source).hexdigest() == SOURCE_SHA256
    rows = []
    for line in source.decode("utf-8").splitlines():
        if "PAYLOAD=" not in line:
            continue
        fields = dict(re.findall(r"(\w+)=([^\s]+)", line))
        fields["timestamp"] = line.split()[0]
        rows.append(fields)
    assert len(rows) == 133
    assert all("+00:00" in r["timestamp"] for r in rows[:128])
    assert all(r["timestamp"].endswith("Z") for r in rows[128:])
    return rows


def unxorshift_right(y, width):
    x = y
    for _ in range(6):
        x = y ^ (x >> width)
    return x & MASK64


def mix(state):
    z = (state ^ (state >> 30)) * 0xBF58476D1CE4E5B9 & MASK64
    z = (z ^ (z >> 27)) * 0x94D049BB133111EB & MASK64
    return (z ^ (z >> 31)) & MASK64


def unmix(z):
    z = unxorshift_right(z, 31)
    z = z * pow(0x94D049BB133111EB, -1, 1 << 64) & MASK64
    z = unxorshift_right(z, 27)
    z = z * pow(0xBF58476D1CE4E5B9, -1, 1 << 64) & MASK64
    return unxorshift_right(z, 30)


def xorshift_step(x):
    x ^= x >> 12
    x ^= (x << 25) & MASK64
    x ^= x >> 27
    return x & MASK64


def fit_stream(words, model):
    length = len(words)
    if model == "splitmix64":
        state = unmix(words[0])
        prediction = [words[0]]
        for _ in range(length - 1):
            state = (state + STEP) & MASK64
            prediction.append(mix(state))
        return prediction
    if model == "xorshift64star":
        state = words[0] * pow(STAR, -1, 1 << 64) & MASK64
        prediction = [words[0]]
        for _ in range(length - 1):
            state = xorshift_step(state)
            prediction.append(state * STAR & MASK64)
        return prediction
    if model == "raw_lcg64":
        x0, x1, x2 = words[:3]
        d = (x1 - x0) & MASK64
        if not d & 1:
            return None
        a = ((x2 - x1) * pow(d, -1, 1 << 64)) & MASK64
        b = (x1 - a * x0) & MASK64
        prediction = list(words[:3])
        for _ in range(length - 3):
            prediction.append((a * prediction[-1] + b) & MASK64)
        return prediction
    raise ValueError("unknown model")


def score_stream(original, predicted, endian):
    if predicted is None:
        return {"fitted": False}
    blocks = [b"".join(x.to_bytes(8, endian) for x in predicted[2*i:2*i+2])
              for i in range(len(original))]
    return {
        "fitted": True,
        "regular_heldout_exact_of_120": sum(blocks[i] == original[i] for i in range(8,128)),
        "recovery_tail_exact_of_5": sum(blocks[i] == original[i] for i in range(128,133)),
    }


def synthetic_controls():
    n = 266
    sm = [mix((0xFA1133EEDDC44BBB + (i+1)*STEP) & MASK64) for i in range(n)]
    state = 0x1234567890ABCDEF
    xs = []
    for _ in range(n):
        state = xorshift_step(state)
        xs.append(state * STAR & MASK64)
    a, b = 6364136223846793005, 1442695040888963407
    lc = [0]
    for _ in range(n-1):
        lc.append((a * lc[-1] + b) & MASK64)
    assert fit_stream(sm, "splitmix64") == sm
    assert fit_stream(xs, "xorshift64star") == xs
    assert fit_stream(lc, "raw_lcg64") == lc
    for val in (0, 1, 0x1234567890ABCDEF, MASK64):
        assert unmix(mix(val)) == val
    return "all three state models reconstruct 133 synthetic 16-byte rows exactly"


def analyze(root=Path("resources")):
    records = read_spool(root)
    raw = [bytes.fromhex(r["PAYLOAD"]) for r in records]
    output = {"synthetic_controls": synthetic_controls(), "models": {}}
    for endian in ("little", "big"):
        words = [int.from_bytes(v[i:i+8], endian) for v in raw for i in (0,8)]
        for name in ("splitmix64", "xorshift64star", "raw_lcg64"):
            output["models"][endian+"_"+name] = score_stream(
                raw, fit_stream(words, name), endian
            )
    mask = bytes.fromhex(json.loads(
        (root/"evidence/recovery-routing.json").read_text()
    )["K04"]["masked_component"])
    predicted = [hmac.digest(mask, r["JOB"].encode(), "sha256")[:16] for r in records]
    output["models"]["HMAC_SHA256_mask_key_job_message"] = {
        "fitted": True,
        "regular_heldout_exact_of_120": sum(predicted[i] == raw[i] for i in range(8,128)),
        "recovery_tail_exact_of_5": sum(predicted[i] == raw[i] for i in range(128,133)),
    }
    return output


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
