"""K04 p955 future-donor authenticator, source-only SFT.

Run: python agents/agent29/k04_future_suffix_witness_sft.py original-case.zip
The observed coupon row129, route mask, slot commitments and K08 are never read.
This mathematical authenticator is conditional on the unverified p955 MT layout.
"""
import json
import random
import sys
from pathlib import Path
from zipfile import ZipFile

from k04_future_donor_sft import (
    ORIGINAL_LAYOUT, MASK32, add_equation, infer_bit, original_source,
    symbolic_mt, untemper,
)


def mt_temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    x ^= x >> 18
    return x & MASK32


def source_basis(observed, starts, expressions):
    result = {}
    for row, start in enumerate(starts):
        if row == 129:
            continue
        for offset, word in enumerate(observed[row]):
            for bit, expression in enumerate(expressions[start + offset]):
                add_equation(result, expression, (word >> bit) & 1)
    assert len(result) == 15305
    return result


def determined_word(basis, expressions):
    value = 0
    for bit, expression in enumerate(expressions):
        fixed = infer_bit(basis, expression)
        assert fixed is not None, "future signature must be entirely source-determined"
        value |= fixed << bit
    return value


def target_xor_constant(basis, expressions, donor_index):
    constant = 0
    for bit in range(32):
        fixed = infer_bit(basis, expressions[958][bit] ^ expressions[donor_index][bit])
        assert fixed is not None, "donor must determine all selected last-word bits"
        constant |= fixed << bit
    return constant


def partial_target_difference(basis, expressions, target_index, donor_index):
    mask = 0
    constant = 0
    for bit in range(32):
        fixed = infer_bit(basis, expressions[target_index][bit] ^ expressions[donor_index][bit])
        if fixed is not None:
            mask |= 1 << bit
            constant |= fixed << bit
    return mask, constant


def main(path):
    with ZipFile(path) as archive:
        observed, _, _ = original_source(archive)
    starts = json.loads(Path(ORIGINAL_LAYOUT).read_text(encoding="utf-8"))["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    expressions = symbolic_mt(2251)
    basis = source_basis(observed, starts, expressions)

    original_constant = target_xor_constant(basis, expressions, 1412)
    second_constant = target_xor_constant(basis, expressions, 1866)
    assert original_constant == 0x24D1E0F2
    assert second_constant == 0x99F6810A
    third_mask, third_constant = partial_target_difference(basis, expressions, 957, 1411)
    assert (third_mask, third_constant) == (0x9FFFFFFF, 0x8B3B35C1)

    suffix_1412 = [determined_word(basis, expressions[i]) for i in (1413, 1414, 1415)]
    suffix_1866 = [determined_word(basis, expressions[i]) for i in (1867, 1868)]
    assert suffix_1412 == [0xCFF3A43D, 0x6F07E907, 0xB81B7C89]
    assert suffix_1866 == [0x81F4D6E4, 0xE7D8B701]
    assert [mt_temper(x) for x in suffix_1412] == [0x758243A9, 0xC4CA6CC8, 0xBAE2035E]
    assert [mt_temper(x) for x in suffix_1866] == [0x7EC6E1CF, 0x40A25EBF]
    # A longer fully source-determined contiguous state beacon six outputs
    # *after* the target-bearing future donor X1412. An unindexed extended
    # external run can be anchored by content before using X1411/X1412.
    beacon_1418 = [determined_word(basis, expressions[i]) for i in range(1418, 1423)]
    assert beacon_1418 == [0x85BDFD0D, 0x036F15CB, 0x9955A20E,
                           0x066B505D, 0x36C8808C]
    assert [mt_temper(x) for x in beacon_1418] == [
        0x9CC93D80, 0x300760A8, 0x7606C13B, 0xD4A5BA9E, 0x3C241095
    ]
    print("source_only_rank", len(basis))
    print("1412_unknown_donor_followed_by_three_fixed_tempered_words",
          "758243A9 C4CA6CC8 BAE2035E")
    print("1866_unknown_donor_followed_by_two_fixed_tempered_words",
          "7EC6E1CF 40A25EBF")
    print("original_pair_witness_xor", f"{original_constant ^ second_constant:08X}")
    print("1418_to_1422_source_determined_160bit_tempered_beacon",
          "9CC93D80 300760A8 7606C13B D4A5BA9E 3C241095")
    print("beacon_little_endian_20bytes", "803DC99CA86007303BC106769EBAA5D49510243C")
    print("X957_X1411_fixed_partial", f"mask={third_mask:08X}", f"offset={third_constant:08X}")
    print("indexed_sixword_run_1410_to_1415_conditional_quotient_gain", 62)

    # Synthetic ACTUAL CPython MT outputs. Withhold selected row129 exactly as above.
    # Predict all 96 signature bits and reconstruct selected X958 from an
    # independently sampled X1412 and source-only constant.
    for seed in (7, 198603, 8131):
        rng = random.Random(seed)
        truth = [untemper(rng.getrandbits(32)) for _ in range(2251)]
        synthetic = [
            None if row == 129 else truth[start:start + 4]
            for row, start in enumerate(starts)
        ]
        b = source_basis(synthetic, starts, expressions)
        for i in (1413, 1414, 1415, 1418, 1419, 1420, 1421, 1422,
                  1867, 1868):
            assert determined_word(b, expressions[i]) == truth[i]
        delta = target_xor_constant(b, expressions, 1412)
        assert (truth[1412] ^ delta) == truth[958]
        mask, value = partial_target_difference(b, expressions, 957, 1411)
        assert mask == 0x9FFFFFFF
        assert ((truth[957] ^ truth[1411]) & mask) == value
        print("seeded_withheld_selected_last_word", seed, "PASS")

    print("real_selected_coupon_payload_unread", True)
    print("actually_recovered_K04_bits", 0)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
