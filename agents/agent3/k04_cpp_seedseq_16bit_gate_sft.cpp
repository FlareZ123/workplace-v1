/*
H-17 Agent 3: bounded native C++ single-uint32 std::seed_seq seed test.
This reproducer is a CONDITIONAL producer gate only; it recovers no K04 bits.

Original ordinary printer observations (rows 0..127, selected row129 and all
late rows withheld) yield 15014 independent GF(2) source constraints on the
pre-first-twist 624x32 register under the published p955 conditional chronology.
They fix S[3]=873F7515 and S[4]=ADD0D034. Source: Agent22's
k04_seedseq_ordinary_partial_inverse_sft.py, whose original spool SHA256 is
7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083.
This source-fixed witness is not a certified historical producer/epoch.

Enumerate all single-word native std::seed_seq inputs 0..65535, generate
624 words as required by std::mt19937 initialization, and compare with those
two original-source-fixed words. A fixed native positive control validates
both the value and complete enumeration. Never reads the selected coupon,
route mask, K04/K08 acceptance hashes, or verifier.
*/
#include <array>
#include <cstdint>
#include <iostream>
#include <random>

int main() {
    constexpr std::uint32_t original_s3 = 0x873F7515U;
    constexpr std::uint32_t original_s4 = 0xADD0D034U;
    std::array<std::uint32_t, 624> output{};

    std::seed_seq control{0x8131U};
    control.generate(output.begin(), output.end());
    if (output[3] != 0x66C0E50EU || output[4] != 0xA2A307BDU) {
        std::cout << "NATIVE_POSITIVE_CONTROL_FAIL\n";
        return 2;
    }

    std::uint64_t positive_pair_matches = 0;
    std::uint64_t original_s3_matches = 0;
    std::uint64_t original_pair_matches = 0;
    for (std::uint32_t seed = 0; seed < 65536U; ++seed) {
        std::seed_seq generator{seed};
        generator.generate(output.begin(), output.end());
        positive_pair_matches +=
            (output[3] == 0x66C0E50EU && output[4] == 0xA2A307BDU);
        original_s3_matches += (output[3] == original_s3);
        original_pair_matches +=
            (output[3] == original_s3 && output[4] == original_s4);
    }

    std::cout << "SEEDS_EXHAUSTED=65536\n"
              << "SYNTHETIC_POSITIVE_PAIR_MATCHES=" << positive_pair_matches << '\n'
              << "ORIGINAL_S3_MATCHES=" << original_s3_matches << '\n'
              << "ORIGINAL_S3_S4_PAIR_MATCHES=" << original_pair_matches << '\n';
    if (positive_pair_matches != 1 || original_pair_matches != 0) {
        std::cout << "GATE_INCOMPLETE\n";
        return 1;
    }
    std::cout << "LOW16_SEEDSEQ_MODEL_EXCLUDED_UNDER_P955\n"
              << "K04_AUTHENTIC_NEW_BITS=0; K08_AUTHENTIC_WORDS=0\n";
    return 0;
}
