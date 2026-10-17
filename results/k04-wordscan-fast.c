/* Fast exhaustive K04 single-four-byte replacement diagnostic (Agent 3).
   Inputs derive from original H-17 ESC-N RECOVER last ACK and route mask.
   Search POS 0,4,8,12 independently with COUNT 4294967296, START 0.
   Requires OpenSSL libcrypto, SHA256_Init and SHA256_Transform.
   A single 16-byte SHA-256 input fits one 64-byte SHA-256 padded block.
   Uses the compression step directly to avoid repeated per-message
   initialization/finalization overhead. No source evidence is written.

   Validation: For each offset 0,4,8,12, replacing the target with the
   SHA256 of the exact unmodified source candidate and searching its
   own original 32-bit word as a single trial returned FOUND. Thus the
   one-block representation was cross-checked against ordinary SHA256.
   This is a corruption-hypothesis test, not original media authentication.
*/
#define OPENSSL_API_COMPAT 0x10100000L
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <openssl/sha.h>

static const uint32_t target[8] = {
    0x930a52a1,0xbab97ca2,0x96633213,0x7c99e992,
    0x98ea6182,0xfb32ab63,0xa3421dfb,0x4fd8c9e0
};
static const uint8_t original[16] = {
    0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,
    0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9
};

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: k04-wordscan-fast POS COUNT [START]\n");
        return 2;
    }
    int pos = atoi(argv[1]);
    uint64_t count = strtoull(argv[2], NULL, 10);
    uint64_t start = argc > 3 ? strtoull(argv[3], NULL, 10) : 0;
    if (pos < 0 || pos > 12 || start > 0x100000000ULL ||
        count > 0x100000000ULL - start) {
        fprintf(stderr, "invalid range\n");
        return 2;
    }

    uint8_t block[64] = {0};
    memcpy(block, original, 16);
    block[16] = 0x80; /* pad bit */
    block[63] = 0x80; /* 128-bit message length encoded in final 8 bytes */
    SHA256_CTX initial;
    SHA256_Init(&initial);
    SHA256_CTX state;
    struct timespec t0, t1;
    timespec_get(&t0, TIME_UTC);

    for (uint64_t n = start; n < start + count; n++) {
        uint32_t v = (uint32_t)n;
        block[pos] = (uint8_t)(v >> 24);
        block[pos + 1] = (uint8_t)(v >> 16);
        block[pos + 2] = (uint8_t)(v >> 8);
        block[pos + 3] = (uint8_t)v;
        memcpy(&state, &initial, sizeof(state));
        SHA256_Transform(&state, block);
        int matches = 1;
        for (int i = 0; i < 8; i++) {
            if (state.h[i] != target[i]) {
                matches = 0;
                break;
            }
        }
        if (matches) {
            printf("FOUND pos=%d n=%llu hex=", pos, (unsigned long long)n);
            for (int i = 0; i < 16; i++) printf("%02X", block[i]);
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
