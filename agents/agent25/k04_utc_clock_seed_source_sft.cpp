// K04: narrowly bounded timestamp-seed source prediction, no target coupon read.
// Source: original 43-member ZIP evidence/print/spool-reconstruction.log
// SHA256 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083
// row0 07:00: FBBBC543 56483F58; row3 07:15: 24FF4383 374867B2
// All words interpreted as little-endian 32-bit values.
// Hypothesis only: unsigned UTC Unix-second clock seed near 07:15,
// producer C++ mt19937(uint32), seed_seq{uint32}, or CPython Random(int).
// No historical original prescribes this seed; no K04 row129/commitment used.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>

struct PythonMT {
    uint32_t state[624]{};
    int index = 624;

    void initial(uint32_t seed) {
        state[0] = seed;
        for (int i=1;i<624;++i)
            state[i] = 1812433253U * (state[i-1] ^ (state[i-1] >> 30)) + static_cast<uint32_t>(i);
    }

    void seed(uint32_t value) {
        initial(19650218U);
        int i=1;
        for (int k=624;k>0;--k) {
            state[i] = (state[i] ^ ((state[i-1] ^ (state[i-1] >> 30)) * 1664525U)) + value;
            if (++i == 624) { state[0] = state[623]; i=1; }
        }
        for (int k=623;k>0;--k) {
            state[i] = (state[i] ^ ((state[i-1] ^ (state[i-1] >> 30)) * 1566083941U)) - static_cast<uint32_t>(i);
            if (++i == 624) { state[0] = state[623]; i=1; }
        }
        state[0] = 0x80000000U;
        index = 624;
    }

    uint32_t next() {
        const uint32_t a = 0x9908B0DFU;
        if (index == 624) {
            uint32_t y;
            int k=0;
            for (;k<227;++k) {
                y = (state[k] & 0x80000000U) | (state[k+1] & 0x7FFFFFFFU);
                state[k] = state[k+397] ^ (y >> 1) ^ ((y&1) ? a:0);
            }
            for (;k<623;++k) {
                y = (state[k] & 0x80000000U) | (state[k+1] & 0x7FFFFFFFU);
                state[k] = state[k-227] ^ (y >> 1) ^ ((y&1) ? a:0);
            }
            y = (state[623] & 0x80000000U) | (state[0] & 0x7FFFFFFFU);
            state[623] = state[396] ^ (y >> 1) ^ ((y&1) ? a:0);
            index = 0;
        }
        uint32_t y = state[index++];
        y ^= y >> 11;
        y ^= (y << 7) & 0x9D2C5680U;
        y ^= (y << 15) & 0xEFC60000U;
        return y ^ (y >> 18);
    }
};

int main() {
    constexpr uint32_t expected_cxx[] = {3499211612U,581869302U,3890346734U,3586334585U,545404204U};
    std::mt19937 control(5489U);
    for (auto word : expected_cxx)
        if (control() != word) { std::cerr << "CXX_REFERENCE_FAIL\n"; return 2; }

    constexpr uint32_t expected_py[] = {0x232A378EU,0x38C69DA3U,0x202A52A8U,0xDEBF600BU,0xD1D094A1U};
    PythonMT pycontrol;
    pycontrol.seed(1791011700U);
    for (auto word : expected_py)
        if (pycontrol.next() != word) { std::cerr << "CPYTHON_REFERENCE_FAIL\n"; return 2; }

    // Source timestamps: row3 2026-10-03 07:15 UTC; use +/-12h Unix seconds.
    constexpr uint32_t origin = 1791011700U;
    constexpr int radius = 43200;
    constexpr int draws = 8192;
    constexpr uint32_t row0_first = 0x43C5BBFBU, row0_second = 0x583F4856U;
    constexpr uint32_t row3_first = 0x8343FF24U, row3_second = 0xB2674837U;
    std::cout << "CXX_REFERENCE_PASS CPYTHON_REFERENCE_PASS\n";
    for (int mode=0;mode<3;++mode) {
        uint64_t matches=0;
        for (int delta=-radius;delta<=radius;++delta) {
            const uint32_t epoch = static_cast<uint32_t>(static_cast<int64_t>(origin)+delta);
            std::mt19937 standard;
            PythonMT python;
            if (mode == 0) standard.seed(epoch);
            if (mode == 1) { std::seed_seq seq{epoch}; standard.seed(seq); }
            if (mode == 2) python.seed(epoch);
            uint32_t previous=0;
            for (int i=0;i<draws;++i) {
                uint32_t current=(mode==2) ? python.next() : standard();
                if ((previous==row0_first && current==row0_second) ||
                    (previous==row3_first && current==row3_second)) {
                    ++matches;
                    std::cout << "MATCH mode="<<mode<<" seed="<<epoch<<" second_index="<<i<<"\n";
                }
                previous=current;
            }
        }
        std::cout << "MODE "<<mode<<" SEEDS "<<(2*radius+1)
                  <<" OUTPUTS_PER_SEED "<<draws<<" MATCHES "<<matches<<"\n";
    }
    return 0;
}
