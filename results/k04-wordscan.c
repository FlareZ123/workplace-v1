/* H-17 bounded diagnostic: one corrupted 32-bit word in K04.
   POS is 0, 4, 8, or 12 for aligned four-byte words.
   COUNT replacement values beginning at START, all unsigned 32-bit.
   Original K04 candidate: ESC-N / PS-261003-0417 / last ACK attempt 2,
   payload XOR routing mask, as derived in results/replay_h17.py.
   This is a hypothesis test; no corruption pattern is asserted as fact.

   Requires a C11-compatible compiler and OpenSSL libcrypto.
   Arguments are POS COUNT [START]. A full aligned-word test uses
   COUNT=4294967296, START=0, and POS in {0,4,8,12}.
*/
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <openssl/sha.h>

static const uint8_t expected[32] = {
    0x93,0x0a,0x52,0xa1,0xba,0xb9,0x7c,0xa2,
    0x96,0x63,0x32,0x13,0x7c,0x99,0xe9,0x92,
    0x98,0xea,0x61,0x82,0xfb,0x32,0xab,0x63,
    0xa3,0x42,0x1d,0xfb,0x4f,0xd8,0xc9,0xe0
};
static const uint8_t original[16] = {
    0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,
    0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9
};

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: k04-wordscan POS COUNT [START]\n");
        return 2;
    }
    int pos = atoi(argv[1]);
    uint64_t count = strtoull(argv[2], NULL, 10);
    uint64_t start = argc > 3 ? strtoull(argv[3], NULL, 10) : 0;
    if (pos < 0 || pos > 12 || start + count > 0x100000000ULL) {
        fprintf(stderr, "invalid range\n");
        return 2;
    }
    uint8_t data[16], digest[32];
    memcpy(data, original, 16);
    struct timespec t0, t1;
    timespec_get(&t0, TIME_UTC);
    for (uint64_t n = start; n < start + count; n++) {
        uint32_t val = (uint32_t)n;
        data[pos] = (uint8_t)(val >> 24);
        data[pos + 1] = (uint8_t)(val >> 16);
        data[pos + 2] = (uint8_t)(val >> 8);
        data[pos + 3] = (uint8_t)val;
        SHA256(data, 16, digest);
        if (memcmp(digest, expected, sizeof(expected)) == 0) {
            printf("FOUND pos=%d value=%llu hex=", pos, (unsigned long long)n);
            for (int i = 0; i < 16; i++) printf("%02X", data[i]);
            putchar('\n');
            return 0;
        }
    }
    timespec_get(&t1, TIME_UTC);
    double elapsed = (double)(t1.tv_sec - t0.tv_sec)
                   + (t1.tv_nsec - t0.tv_nsec) / 1e9;
    printf("NO_MATCH pos=%d start=%llu count=%llu seconds=%.3f\n",
           pos, (unsigned long long)start, (unsigned long long)count, elapsed);
    return 1;
}
