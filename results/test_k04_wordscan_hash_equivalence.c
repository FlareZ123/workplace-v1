/* K04 full-range scanner: deterministic differential hash control.
 * Cross-check its one-block SHA256_Transform representation against the
 * ordinary OpenSSL SHA256 digest at 13 byte offsets, 1000 trial values each.
 * This tests only hashing equivalence, not source provenance.
 *
 * Compile with a C11 compiler and OpenSSL libcrypto, then run this file.
 * No original evidence or commitments are changed.
 */
#define OPENSSL_API_COMPAT 0x10100000L
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

int main(void) {
    static const uint8_t original[16] = {
        0x2c, 0xff, 0x14, 0x9c, 0x50, 0xe5, 0x45, 0x57,
        0x22, 0x8e, 0x7d, 0xe6, 0x0b, 0x3e, 0xb7, 0xc9
    };
    uint32_t state = 0x8e2acc51;
    SHA256_CTX initial;
    SHA256_Init(&initial);
    int checks = 0;

    for (int position = 0; position <= 12; ++position) {
        for (int sample = 0; sample < 1000; ++sample) {
            state ^= state << 13;
            state ^= state >> 17;
            state ^= state << 5;
            uint32_t value = state;

            uint8_t message[16], block[64] = {0}, digest[32];
            memcpy(message, original, 16);
            message[position] = (uint8_t)(value >> 24);
            message[position + 1] = (uint8_t)(value >> 16);
            message[position + 2] = (uint8_t)(value >> 8);
            message[position + 3] = (uint8_t)value;

            memcpy(block, message, 16);
            block[16] = 0x80;
            block[63] = 0x80;
            SHA256_CTX computed;
            memcpy(&computed, &initial, sizeof(computed));
            SHA256_Transform(&computed, block);
            SHA256(message, 16, digest);

            for (int word = 0; word < 8; ++word) {
                uint32_t expected =
                    ((uint32_t)digest[word * 4] << 24) |
                    ((uint32_t)digest[word * 4 + 1] << 16) |
                    ((uint32_t)digest[word * 4 + 2] << 8) |
                    (uint32_t)digest[word * 4 + 3];
                if (computed.h[word] != expected) {
                    fprintf(stderr, "FAIL position=%d sample=%d word=%d\n",
                            position, sample, word);
                    return 1;
                }
            }
            ++checks;
        }
    }

    printf("PASS: %d SHA-256 differential controls, 13 positions\n", checks);
    return 0;
}
