/* H-17 K04: bounded left/right contiguous byte-slip diagnostic.
   The spool is a retained-fragment export with unverified payload bytes.
   Test a truncated 16-byte window that is off by 1..3 whole bytes:
   left:  discard k leading bytes; append k unknown bytes
   right: prepend k unknown bytes; discard k trailing bytes
   Each unknown byte takes all 256 values in all combinations.
   XOR each resulting 16-byte payload with original ESC-N mask;
   SHA-256-check the derived component against unchanged K04 commitment.
   All 33,686,016 assignments are examined; no source evidence is written.
   Requires C11 and OpenSSL libcrypto.
   Positive control: replace the target with SHA256 of a known 2-byte
   left-slip with new suffix 1234; the scanner finds this exact candidate.
*/
#define OPENSSL_API_COMPAT 0x10100000L
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

static const uint8_t payload[16] = {
    0xA9,0xA9,0xDC,0x57,0x31,0xA5,0xE2,0xAE,
    0x87,0x9C,0x47,0x21,0x5C,0x25,0x59,0xD5
};
static const uint8_t mask[16] = {
    0x85,0x56,0xC8,0xCB,0x61,0x40,0xA7,0xF9,
    0xA5,0x12,0x3A,0xC7,0x57,0x1B,0xEE,0x1C
};
static const uint32_t target[8] = {
    0x930a52a1,0xbab97ca2,0x96633213,0x7c99e992,
    0x98ea6182,0xfb32ab63,0xa3421dfb,0x4fd8c9e0
};

int main(void) {
    unsigned long long tested = 0;
    SHA256_CTX initial, state;
    SHA256_Init(&initial);
    for (int count = 1; count <= 3; count++) {
        uint32_t limit = 1u << (8 * count);
        for (int mode = 0; mode < 2; mode++) {
            uint8_t block[64] = {0};
            block[16] = 0x80;
            block[63] = 0x80;
            for (int i = 0; i < 16 - count; i++) {
                int dest = mode == 0 ? i : i + count;
                block[dest] = payload[mode == 0 ? i + count : i] ^ mask[dest];
            }
            int unknown_pos = mode == 0 ? 16 - count : 0;
            for (uint32_t n = 0; n < limit; n++) {
                for (int j = 0; j < count; j++) {
                    block[unknown_pos + j] =
                        ((uint8_t)(n >> (8 * (count - 1 - j)))) ^ mask[unknown_pos + j];
                }
                memcpy(&state, &initial, sizeof(state));
                SHA256_Transform(&state, block);
                tested++;
                int matches = 1;
                for (int j = 0; j < 8; j++) {
                    if (state.h[j] != target[j]) {
                        matches = 0;
                        break;
                    }
                }
                if (matches) {
                    printf("FOUND slip=%d direction=%s n=%u K04=",
                           count, mode == 0 ? "left" : "right", n);
                    for (int i = 0; i < 16; i++) printf("%02X", block[i]);
                    putchar('\n');
                    return 0;
                }
            }
            printf("NO_MATCH slip=%d direction=%s tested=%u\n",
                   count, mode == 0 ? "left" : "right", limit);
        }
    }
    printf("TOTAL_NO_MATCH tested=%llu\n", tested);
    return 1;
}
