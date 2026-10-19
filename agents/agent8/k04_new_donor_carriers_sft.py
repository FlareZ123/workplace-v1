"""SFT: new original K01/K03/K02 source-carrier attacks on K04 MT ancestor windows.

Usage: python k04_new_donor_carriers_sft.py ORIGINAL_CASE_ZIP
Read-only. Neither the disputed K04 ACK nor any acceptance digest is used.
"""
import collections
import datetime
import hashlib
import json
import re
import struct
import sys
import zipfile

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAINT_SHA = "c00944558636fbcc7e91b81e8e838ffd13fcd5a30d121b41951888766a8a0e32"
TELE_SHA = "3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f"
TRANSFER_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"
LOW = 0x7fffffff


def undo_right(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & 0xffffffff


def undo_left(y, shift, mask):
    x = y
    for _ in range(8):
        x = y ^ ((x << shift) & mask)
    return x & 0xffffffff


def untemper(y):
    return undo_right(undo_left(undo_left(undo_right(y, 18), 15, 0xefc60000), 7, 0x9d2c5680), 11)


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9d2c5680
    x ^= (x << 15) & 0xefc60000
    return (x ^ (x >> 18)) & 0xffffffff


def inverse_pair(m, e):
    z = m ^ e
    odd = z >> 31
    return (((z ^ (0x9908b0df if odd else 0)) << 1) | odd) & 0xffffffff


def original_rows(z):
    data = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(data).hexdigest() == SPOOL_SHA
    payloads = re.findall(rb"PAYLOAD=([A-F0-9]{32})", data)
    assert len(payloads) == 133
    rows = [tuple(untemper(word) for word in struct.unpack("<4I", bytes.fromhex(payload.decode()))) for payload in payloads]
    rows[129] = ()  # selected coupon is never used as an ancestor
    return rows


def pair_index(rows):
    result = collections.defaultdict(list)
    for a, first in enumerate(rows):
        for b in range(a + 1, len(rows)):
            second = rows[b]
            for j, m in enumerate(first):
                for k, e in enumerate(second):
                    result[inverse_pair(m, e) & LOW].append((a, j, b, k))
    assert sum(map(len, result.values())) == 138336
    return result


def source_fullword_probe(z, index):
    ink = []
    for name in ("03", "06"):
        data = z.read("evidence/mail/" + name + ".eml").decode("utf-8")
        ink.extend(re.findall(r"WN-14 / group [ABCD] / ([0-9A-F]{8})", data))
    assert set(ink) == {"049AAB2E", "CD7C6023", "1CDE7A82", "4303C91A"}
    receipts = z.read("evidence/maintenance/seal-receipts.jsonl")
    assert hashlib.sha256(receipts).hexdigest() == MAINT_SHA
    serials = [json.loads(x)["serial"].split("SG-")[1] for x in receipts.splitlines()]
    assert len(serials) == 44 and all(re.fullmatch("[A-F0-9]{8}", x) for x in serials)
    for name, values in (("K01_SIGNED_WN14", ink), ("K03_SEAL_SERIALS", serials)):
        matches = []
        for j, literal in enumerate(values):
            for endian in ("little", "big"):
                state = untemper(int.from_bytes(bytes.fromhex(literal), endian)) & LOW
                for witness in index.get(state, ()):
                    matches.append((j, literal, endian, witness))
        print(name, "tokens", len(values), "orientations", len(values) * 2, "inverse_word_matches", len(matches))
        for item in matches:
            print("CARRIER_MATCH", item)
        assert not matches


def high16_options(m, e):
    low = inverse_pair(m, e) & LOW
    return {temper(low) >> 16, temper(low | 0x80000000) >> 16}


def source_halfword_probe(z, rows):
    transfers = z.read("evidence/transfers/transfer-audit.jsonl")
    assert hashlib.sha256(transfers).hexdigest() == TRANSFER_SHA
    ax = [json.loads(x) for x in transfers.splitlines()]
    ax = sorted((x for x in ax if x.get("transfer") == "AX-7778" and x.get("kind") == "CHUNK"), key=lambda x: (x["seq"], x["attempt"]))
    assert len(ax) == 16
    ax_words = [int(x["checkpoint"], 16) for x in ax]
    predicted = [high16_options(rows[34][j], rows[64][j]) for j in range(4)]
    true_ax_run = [((x & 255) << 8) | (x >> 8) for x in ax_words[11:15]]
    assert all(value in allowed for value, allowed in zip(true_ax_run, predicted))
    print("AX7778_4WORD_INDEPENDENT_POSITIVE_CONTROL PASS source positions 11:15 / printer rows34,64")

    data = z.read("evidence/telemetry/freeze-export.jsonl")
    assert hashlib.sha256(data).hexdigest() == TELE_SHA
    records = [json.loads(x) for x in data.splitlines()]
    full = [(i, r) for i, r in enumerate(records) if r["tag"] == "LT-204" and r["field"] == "DIAG_WORD"]
    assert len(full) == 33
    valid = [(i, r) for i, r in full if r["seq"] in range(8) and r["revision"] in range(1, 5)]
    assert len(valid) == 32
    views = {
        "SEQ_REV": [r["value"] for _, r in sorted(valid, key=lambda t: (t[1]["seq"], t[1]["revision"]))],
        "REV_SEQ": [r["value"] for _, r in sorted(valid, key=lambda t: (t[1]["revision"], t[1]["seq"]))],
        "FILE": [r["value"] for _, r in valid],
        "UTC": [r["value"] for _, r in sorted(valid, key=lambda t: (datetime.datetime.fromisoformat(t[1]["ts"]), t[1]["seq"], t[1]["revision"]))],
    }
    good = [r for _, r in valid if r["quality"] == "GOOD" and r["state"] == "HOLD"]
    latest = {r["seq"]: r for r in sorted(good, key=lambda r: r["revision"])}
    assert len(latest) == 8
    views["K02_SELECTION"] = [latest[i]["value"] for i in sorted(latest)]

    for label, values in views.items():
        matches = []
        for n in (3, 4):
            for pos in range(len(values) - n + 1):
                chunk = values[pos:pos + n]
                for flip in (False, True):
                    candidates = [((v >> 8) | ((v & 255) << 8)) if flip else v for v in chunk]
                    for a, first in enumerate(rows):
                        if not first:
                            continue
                        for b in range(a + 1, len(rows)):
                            second = rows[b]
                            if not second:
                                continue
                            for j in range(5 - n):
                                for k in range(5 - n):
                                    if all(v in high16_options(first[j + h], second[k + h]) for h, v in enumerate(candidates)):
                                        matches.append((n, pos, flip, a, j, b, k))
        print("K02_DIAG", label, "values", len(values), "3/4-run_matches", len(matches))
        for match in matches:
            print("CARRIER_MATCH", match)
        assert not matches


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python k04_new_donor_carriers_sft.py ORIGINAL_CASE_ZIP"
    with zipfile.ZipFile(sys.argv[1]) as case:
        rows = original_rows(case)
        fingerprint = pair_index(rows)
        source_fullword_probe(case, fingerprint)
        source_halfword_probe(case, rows)
    print("NEW_K04_ANCESTOR_DONORS_ZERO; ORIGINAL_TARGET_AND_CHECKER_UNTOUCHED")
