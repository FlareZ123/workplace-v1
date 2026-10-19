// K04 source-conditioned exhaustive inverse of one missing CPython integer seed word.
// Exactly 32-bit key word, known 4 seeded state words, fixed candidate phase, and
// a second independently recovered state word. No REC8 hash, K04 row129, or mask.
// Outputs candidates for a separate full-generator held-out source check.
// Synthetic real-CPython positive control is in k04_seed3_origin_scan.py.
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <mutex>
#include <thread>
#include <vector>

static uint32_t initial[624];

static void initialize() {
    initial[0] = 19650218u;
    for (uint32_t i = 1; i < 624; ++i)
        initial[i] = 1812433253u * (initial[i-1] ^ (initial[i-1] >> 30)) + i;
}

static inline uint32_t next_word(uint32_t a, uint32_t b, uint32_t key,
                                 uint32_t i, uint32_t key_index) {
    uint32_t left = (b + i - 1) ^ (1566083941u * (a ^ (a >> 30)));
    uint32_t right = (initial[i] ^ (1664525u * (left ^ (left >> 30))))
                     + key + key_index;
    return (right ^ (1566083941u * (b ^ (b >> 30)))) - i;
}

int main(int argc, char **argv) {
    if (argc != 13) {
        std::fprintf(stderr,
                     "usage: seed3 phase key0 key1 key2 state0 state1 state2 "
                     "state3 terminal begin count workers\n");
        return 2;
    }
    uint32_t phase = uint32_t(std::strtoul(argv[1], nullptr, 0));
    uint32_t keys[3] = {
        uint32_t(std::strtoul(argv[2], nullptr, 0)),
        uint32_t(std::strtoul(argv[3], nullptr, 0)),
        uint32_t(std::strtoul(argv[4], nullptr, 0))
    };
    uint32_t state[4] = {
        uint32_t(std::strtoul(argv[5], nullptr, 0)),
        uint32_t(std::strtoul(argv[6], nullptr, 0)),
        uint32_t(std::strtoul(argv[7], nullptr, 0)),
        uint32_t(std::strtoul(argv[8], nullptr, 0))
    };
    uint32_t terminal = uint32_t(std::strtoul(argv[9], nullptr, 0));
    uint64_t begin = std::strtoull(argv[10], nullptr, 0);
    uint64_t count = std::strtoull(argv[11], nullptr, 0);
    unsigned workers = unsigned(std::strtoul(argv[12], nullptr, 0));
    if (phase > 392 || workers < 1 || count < 1 ||
        begin + count > (uint64_t(1) << 32)) return 2;
    initialize();

    const uint32_t missing = (phase + 231u) % 3u;
    std::mutex mutex;
    std::atomic<uint64_t> checked{0}, hits{0};
    auto started = std::chrono::steady_clock::now();
    auto worker = [&](unsigned id) {
        uint64_t n = 0;
        for (uint64_t index = begin + id; index < begin + count;
             index += workers) {
            uint32_t key = uint32_t(index);
            uint32_t a = state[2], b = state[3];
            for (uint32_t i = phase + 232; i < 624; ++i) {
                uint32_t j = (i - 1) % 3;
                uint32_t c = next_word(a, b, j == missing ? key : keys[j], i, j);
                a = b;
                b = c;
            }
            if (b == terminal) {
                std::lock_guard<std::mutex> guard(mutex);
                std::printf("FOUND missing_index=%u missing_word=%08X "
                            "full_keys=%08X %08X %08X\n", missing, key,
                            missing == 0 ? key : keys[0],
                            missing == 1 ? key : keys[1],
                            missing == 2 ? key : keys[2]);
                std::fflush(stdout);
                hits++;
            }
            ++n;
        }
        checked += n;
    };
    std::vector<std::thread> pool;
    for (unsigned id = 0; id < workers; ++id)
        pool.emplace_back(worker, id);
    for (auto &t : pool) t.join();
    double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    std::printf("CHECKED phase=%u n=%llu elapsed=%.4f "
                "rate_million_s=%.3f hits=%llu\n",
                phase, static_cast<unsigned long long>(checked.load()),
                elapsed, checked.load() / elapsed / 1e6,
                static_cast<unsigned long long>(hits.load()));
    return 0;
}
