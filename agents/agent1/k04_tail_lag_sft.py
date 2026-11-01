"""One-row lagged DEST hypothesis for original H-17 exceptional print tail.

Run: python agents/agent1/k04_tail_lag_sft.py original-case.zip
Read-only original files. Do not use the selected ACK payload to fit a rule.
"""
import hashlib
import json
import re
import struct
import sys
from zipfile import ZipFile

SPOOL = "evidence/print/spool-reconstruction.log"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
DEST = {"store": 0, "desk": 1, "bench": 2}
CONTROL_EDGES = (127, 128, 130, 131)


def parse_line(line):
    payload = bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})", line).group(1))
    dest = re.search(r"DEST=(store|desk|bench)", line).group(1)
    return payload, DEST[dest]


def code_last_word(payload):
    return struct.unpack_from("<I", payload, 12)[0] >> 30


def main(path):
    with ZipFile(path) as archive:
        spool = archive.read(SPOOL)
        assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
        rows = [s for s in spool.decode().splitlines() if s.startswith("2026-")]
        assert len(rows) == 133

        # Fitting and four original checks exclude selected row129 PAYLOAD.
        for left in CONTROL_EDGES:
            payload, _ = parse_line(rows[left])
            right_dest = DEST[re.search(r"DEST=(store|desk|bench)", rows[left + 1]).group(1)]
            predicted = code_last_word(payload)
            assert predicted == right_dest, (left, predicted, right_dest)
            print("source_control", f"row{left}->row{left+1}",
                  "last_word_top2", predicted, "next_dest", right_dest, "PASS")

        # An ordinary-row comparison, not a source authentication argument.
        ordinary_matches = sum(
            code_last_word(parse_line(rows[i])[0]) == parse_line(rows[i + 1])[1]
            for i in range(127)
        )
        assert ordinary_matches == 36
        print("ordinary_to_ordinary_comparison", ordinary_matches, "/", 127)

        # Under a one-row-lagged DEST field the next DEST encodes two
        # bits of the selected row's last 32-bit printed word.
        inferred_original_code = DEST[re.search(r"DEST=(store|desk|bench)", rows[130]).group(1)]
        assert inferred_original_code == 2
        print("conditional_selected_row129_last_word_top2", format(inferred_original_code, "02b"))

        # Post-fit diagnosis: read the selected copied payload only now.
        copied, _ = parse_line(rows[129])
        copied_code = code_last_word(copied)
        assert copied_code == 3 and copied[-1] == 0xD5
        print("copied_selected_row129_last_word_top2", format(copied_code, "02b"))
        print("conditional_discordant_bit", "last payload byte bit6", "D5 -> 95")

        corrected = bytearray(copied)
        corrected[-1] ^= 0x40
        assert code_last_word(corrected) == inferred_original_code

        # ONE target-directed, fully formed correction; no repair-radius sweep.
        routing = json.loads(archive.read("evidence/recovery-routing.json"))
        commitment = json.loads(archive.read("acceptance.json"))["slot_sha256"]["K04"]
        mask = bytes.fromhex(routing["K04"]["masked_component"])
        component = bytes(x ^ y for x, y in zip(corrected, mask))
        digest = hashlib.sha256(component).hexdigest()
        assert digest != commitment
        print("one_bit_corrected_print_payload", corrected.hex().upper())
        print("corrected_component_candidate", component.hex().upper())
        print("candidate_sha256", digest)
        print("original_K04_commitment_match", False)
        # Frozen two-fault family: recorded A9 A9 may have copied original
        # byte0 twice, replacing original unknown byte1; separately apply the
        # single last-byte bit correction from the lagged DEST constraint.
        candidate_hashes = []
        for second_byte in range(256):
            alt = bytearray(corrected)
            alt[1] = second_byte
            key = bytes(x ^ y for x, y in zip(alt, mask))
            candidate_hashes.append(hashlib.sha256(key).hexdigest())
        hits = [i for i, value in enumerate(candidate_hashes) if value == commitment]
        synthetic_target = candidate_hashes[0x42]
        assert [i for i, value in enumerate(candidate_hashes)
                if value == synthetic_target] == [0x42]
        assert hits == []
        print("conditional_C1_duplicate_and_C15_bit6_candidates", 256)
        print("two_fault_original_K04_matches", hits)
        print("two_fault_synthetic_positive_control", "PASS")
        print("observed_authentic_selected_coupon_bits", 0, "/ 128")
        print("model_historical_producer_authenticated", False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_tail_lag_sft.py original-case.zip")
    main(sys.argv[1])
