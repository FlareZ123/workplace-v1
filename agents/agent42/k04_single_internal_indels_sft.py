"""K04 copied-hex interior one-bit/one-nibble indel source-pinned SFT.

Two frozen, finite source-repair families. Original ZIP is read only.
No inference from unattested printer production, no modified commitments.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile

ZIP_SHA = "a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
HEX = "0123456789ABCDEF"


def reverse_byte_bits(data):
    return bytes(int(f"{v:08b}"[::-1], 2) for v in data)


def to_bits(data):
    return "".join(f"{v:08b}" for v in data)


def to_bytes(bits):
    assert len(bits) == 128
    return bytes(int(bits[i:i+8], 2) for i in range(0,128,8))


def bit_edits(payload, order):
    encoded = payload if order == "msb" else reverse_byte_bits(payload)
    bits = to_bits(encoded)
    result = set()
    def add(value):
        raw = to_bytes(value)
        result.add(raw if order == "msb" else reverse_byte_bits(raw))
    for i in range(128):
        part = bits[:i] + bits[i+1:]
        for edge in "01":
            add(edge + part)
            add(part + edge)
    for part in (bits[1:], bits[:-1]):
        for i in range(128):
            for missing in "01":
                add(part[:i] + missing + part[i:])
    return result


def nibble_edits(payload):
    assert len(payload) == 32 and all(c in HEX for c in payload)
    result = set()
    for i in range(32):
        part = payload[:i] + payload[i+1:]
        for v in HEX:
            result.add(v + part)
            result.add(part + v)
    for part in (payload[1:], payload[:-1]):
        for i in range(32):
            for v in HEX:
                result.add(part[:i] + v + part[i:])
    return result


def controls():
    original = bytes.fromhex("C13215A2F46012BD438F909012340022")
    for order in ("msb", "lsb"):
        bits = to_bits(original if order == "msb" else reverse_byte_bits(original))
        variants = (bits[:19] + "1" + bits[19:127],
                    (bits[:51] + "0" + bits[51:])[1:],
                    "1" + bits[:81] + bits[82:],
                    bits[:112] + bits[113:] + "0")
        for i, value in enumerate(variants):
            raw = to_bytes(value)
            if order == "lsb":
                raw = reverse_byte_bits(raw)
            assert original in bit_edits(raw, order), (order, i)
            print("SYNTHETIC_BIT_PASS", order, i, flush=True)
    phrase = original.hex().upper()
    variants = (phrase[:7] + "F" + phrase[7:-1],
                (phrase[:14] + "0" + phrase[14:])[1:],
                "7" + phrase[:21] + phrase[22:],
                phrase[:28] + phrase[29:] + "8")
    for i, value in enumerate(variants):
        assert phrase in nibble_edits(value), i
        print("SYNTHETIC_NIBBLE_PASS", i, flush=True)


def source(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == ZIP_SHA
    with ZipFile(path) as z:
        spool = z.read("evidence/print/spool-reconstruction.log")
        assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
        ini = z.read("evidence/archive-labels.ini").decode()
        current = ini.split("[printer_routes_2026-09-01_to_2026-10-03]", 1)[1].split("[", 1)[0]
        job = re.search(r"^ESC-N=(\S+)$", current, flags=re.MULTILINE).group(1)
        rows = []
        for line in spool.decode().splitlines():
            if not line or line.startswith("#"):
                continue
            data = dict(v.split("=", 1) for v in line.split()[1:])
            if data["JOB"] == job and data["STATE"] == "ACK" and data["CLASS"] == "RECOVER":
                rows.append((int(data["ATTEMPT"]),line.split()[0],data["PAYLOAD"]))
        assert rows == [(2,"2026-10-03T18:02:00Z","A9A9DC5731A5E2AE879C47215C2559D5")]
        mask = bytes.fromhex(json.loads(z.read("evidence/recovery-routing.json"))["K04"]["masked_component"])
        expected = json.loads(z.read("acceptance.json"))["slot_sha256"]["K04"]
    return rows[0][2],mask,expected


def main(path):
    controls()
    copied,mask,expected = source(path)
    b = bytes.fromhex(copied)
    all_bits = bit_edits(b,"msb") | bit_edits(b,"lsb")
    all_nibbles = {bytes.fromhex(t) for t in nibble_edits(copied)}
    print("SOURCE_K04",copied,"BIT_CANDIDATES",len(all_bits),"NIBBLE_CANDIDATES",len(all_nibbles),flush=True)
    for label, candidates in (("BIT",all_bits),("NIBBLE",all_nibbles)):
        hits=[]
        for test in candidates:
            key = bytes(a^b for a,b in zip(test,mask))
            if hashlib.sha256(key).hexdigest() == expected:
                hits.append((test.hex().upper(),key.hex().upper()))
        print("K04_"+label+"_MATCHES",len(hits),"CANDIDATES_TESTED",len(candidates),flush=True)
        for payload, key in hits:
            print("RECOVERED_ORIGINAL_K04",label,payload,key,flush=True)
    print("LIMIT: conditional one-interior-bit or one-hex-digit repair only; media integrity unproven",flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_single_internal_indels_sft.py ORIGINAL_CASE_ZIP")
    main(Path(sys.argv[1]))
