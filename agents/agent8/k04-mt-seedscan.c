/*
 * H-17 K04 exact CPython random.Random(uint32 seed) seed/offset search.
 *
 * Original spool payloads imply MT19937 twist correlations; this tests the
 * much narrower hypothesis that a uint32 scalar seed initialized CPython's
 * init_by_array RNG, and the first four payload words occur within a bounded
 * number of initial RNG outputs. Source files and acceptance are never edited.
 *
 * Build with GCC + OpenMP: gcc -O3 -fopenmp -o k04seed k04-mt-seedscan.c
 * Invoke k04seed start count max_offset. Positive fixture:
 * replace target with Python random.Random(12345678) first four words and run
 * k04seed 12345678 1 16: FOUND offset=0.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <omp.h>

#define N 624
#define M 397
#define MATRIX_A 0x9908b0dfU
#define UPPER_MASK 0x80000000U
#define LOWER_MASK 0x7fffffffU

struct mt { uint32_t a[N]; int ix; };

static void init_genrand(struct mt *s, uint32_t seed) {
    s->a[0] = seed;
    for (int i = 1; i < N; i++)
        s->a[i] = 1812433253U * (s->a[i-1] ^ (s->a[i-1] >> 30)) + i;
    s->ix = N;
}

static void init_by_array(struct mt *s, uint32_t seed) {
    init_genrand(s, 19650218U);
    int i = 1;
    for (int k = N; k > 0; k--) {
        s->a[i] = (s->a[i] ^
                    ((s->a[i-1] ^ (s->a[i-1] >> 30)) * 1664525U)) + seed;
        i++;
        if (i >= N) { s->a[0] = s->a[N-1]; i = 1; }
    }
    for (int k = N-1; k > 0; k--) {
        s->a[i] = (s->a[i] ^
                    ((s->a[i-1] ^ (s->a[i-1] >> 30)) * 1566083941U)) - i;
        i++;
        if (i >= N) { s->a[0] = s->a[N-1]; i = 1; }
    }
    s->a[0] = 0x80000000U;
    s->ix = N;
}

static inline void twist(struct mt *s) {
    uint32_t y;
    for (int k = 0; k < N-M; k++) {
        y = (s->a[k] & UPPER_MASK) | (s->a[k+1] & LOWER_MASK);
        s->a[k] = s->a[k+M] ^ (y >> 1) ^
                  ((y & 1) ? MATRIX_A : 0);
    }
    for (int k = N-M; k < N-1; k++) {
        y = (s->a[k] & UPPER_MASK) | (s->a[k+1] & LOWER_MASK);
        s->a[k] = s->a[k+M-N] ^ (y >> 1) ^
                  ((y & 1) ? MATRIX_A : 0);
    }
    y = (s->a[N-1] & UPPER_MASK) | (s->a[0] & LOWER_MASK);
    s->a[N-1] = s->a[M-1] ^ (y >> 1) ^
                ((y & 1) ? MATRIX_A : 0);
    s->ix = 0;
}

static inline uint32_t next(struct mt *s) {
    if (s->ix >= N) twist(s);
    uint32_t y = s->a[s->ix++];
    y ^= y >> 11;
    y ^= (y << 7) & 0x9d2c5680U;
    y ^= (y << 15) & 0xefc60000U;
    y ^= y >> 18;
    return y;
}

int main(int argc, char **argv) {
    uint64_t start = argc > 1 ? strtoull(argv[1], NULL, 0) : 0;
    uint64_t count = argc > 2 ? strtoull(argv[2], NULL, 0) : 1000000;
    int offsets = argc > 3 ? atoi(argv[3]) : 624;
    if (offsets < 1 || offsets > 4096 ||
        count == 0 || start + count > (uint64_t)UINT32_MAX + 1)
        return 2;
    const uint32_t target[4] = {
        0x43C5BBFBU, 0x583F4856U, 0x063FBB64U, 0xA5184579U
    };
    int matches = 0;
    double t = omp_get_wtime();
    #pragma omp parallel reduction(+:matches)
    {
        struct mt s;
        #pragma omp for schedule(dynamic,8192)
        for (uint64_t seed = start; seed < start + count; seed++) {
            init_by_array(&s, (uint32_t)seed);
            uint32_t a = 0, b = 0, c = 0, d = 0;
            for (int j = 0; j < offsets + 3; j++) {
                a = b; b = c; c = d; d = next(&s);
                if (j >= 3 && a == target[0] && b == target[1] &&
                    c == target[2] && d == target[3]) {
                    #pragma omp critical
                    printf("FOUND seed=%" PRIu64 " offset=%d\n", seed, j - 3);
                    matches++;
                }
            }
        }
    }
    printf("start=%" PRIu64 " count=%" PRIu64
           " max_offset=%d matches=%d elapsed_sec=%.3f\n",
           start, count, offsets, matches, omp_get_wtime() - t);
    return 0;
}
