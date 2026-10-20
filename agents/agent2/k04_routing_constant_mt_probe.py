"""Source-only SFT: test REC8 commissioning constants as putative MT19937 donor words.

Reads the original 43-member H-17 local export ZIP. The selected disputed
printer row129 and every acceptance commitment are excluded. The direct
producer hypothesis is deliberately weak: neither original source identifies
the routing constants as MT-generated or gives an indexed stream epoch.
"""
import collections
import hashlib
import json
import re
import struct
import sys
import zipfile
import zlib

ROUTE_SHA = "f8fcbca73d23bf1066edb88c088f89cd24cf22e7c78a4a412166254a4764d8a5"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
RECORDER_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
LOW31 = 0x7fffffff


def unshift_right(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & 0xffffffff


def unshift_left(y, shift, mask):
    x = y
    for _ in range(8):
        x = y ^ ((x << shift) & mask)
    return x & 0xffffffff


def untemper(y):
    return unshift_right(
        unshift_left(
            unshift_left(unshift_right(y, 18), 15, 0xefc60000),
            7, 0x9d2c5680),
        11)


def inverse_predecessor(middle, end):
    z = middle ^ end
    parity = z >> 31
    return (((z ^ (0x9908b0df if parity else 0)) << 1) | parity) & LOW31


def pinned(z, name, expected):
    content = z.read(name)
    assert hashlib.sha256(content).hexdigest() == expected, name
    return content


def main(path):
    with zipfile.ZipFile(path) as z:
        spool = pinned(z, "evidence/print/spool-reconstruction.log", SPOOL_SHA)
        routing = json.loads(pinned(z, "evidence/recovery-routing.json", ROUTE_SHA))
        recorder = pinned(z, "evidence/recorder/trip-recorder.raw", RECORDER_SHA)
    payloads = re.findall(rb"PAYLOAD=([A-F0-9]{32})", spool)
    assert len(payloads) == 133
    rows = [
        tuple(untemper(w) for w in struct.unpack("<4I", bytes.fromhex(p.decode())))
        if i != 129 else ()
        for i, p in enumerate(payloads)
    ]
    full = {word for row in rows for word in row}
    inverse = collections.defaultdict(list)
    for i, earlier in enumerate(rows):
        for j in range(i + 1, len(rows)):
            for a, m in enumerate(earlier):
                for b, e in enumerate(rows[j]):
                    inverse[inverse_predecessor(m, e)].append((i, a, j, b))
    assert len(full) == 528
    assert sum(map(len, inverse.values())) == 138336

    # Independent real-source calibration, no synthetic forged records.
    record = recorder[16 + 26 * 24:16 + 27 * 24]
    assert zlib.crc32(record[:20]) == int.from_bytes(record[20:24], "little")
    control = untemper(int.from_bytes(record[12:16], "little")) & LOW31
    assert inverse_predecessor(rows[7][3], rows[38][0]) == control
    print("ORIGINAL_CRC_VALID_RECORDER_POSITIVE PASS", control)

    constants = {
        "K04.masked_component": routing["K04"]["masked_component"],
        "K08.desk_nonce": routing["K08"]["desk_nonce"],
    }
    for name, hexstr in constants.items():
        b = bytes.fromhex(hexstr)
        assert len(b) == 16
        for endian in ("little", "big"):
            words = [
                untemper(int.from_bytes(b[i:i + 4], endian))
                for i in range(0, 16, 4)
            ]
            direct = [(i, word) for i, word in enumerate(words) if word in full]
            preceding = [
                (i, inverse[word & LOW31])
                for i, word in enumerate(words) if word & LOW31 in inverse
            ]
            print(name, endian, "DIRECT_FULL", len(direct),
                  "PREDECESSOR_LOW31", len(preceding))
            assert not direct and not preceding
    print("ROUTING_CONSTANTS_NO_DIRECT_MT_DONOR; SELECTED_ROW_WITHHELD")


if __name__ == "__main__":
    assert len(sys.argv) == 2, "python k04_routing_constant_mt_probe.py ORIGINAL_CASE_ZIP"
    main(sys.argv[1])
