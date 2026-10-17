/* K04: byte-level retained-fragment mosaic, one exact printer job.
   Each of the 16 payload bytes is selected independently from the
   three RECOVER attempts for job PS-261003-0417. All 3^16 choices are
   enumerated and XORed against the unchanged ESC-N mask; SHA256 of the
   resulting 16-byte component is checked against the original target.
   This diagnostic tests mixed reconstruction fragments only.
   The REQUESTED attempts were not acknowledged and are not verified
   authentic coupons. A matching hash would still require source checks.
   Requires a C compiler and OpenSSL libcrypto.
*/
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

static const unsigned char payload[3][16] = {
    {0xCD,0x3E,0x4F,0x21,0x6A,0xDB,0x2F,0xB1,0x80,0xDA,0x2A,0xA9,0x0B,0x33,0xF7,0xA4},
    {0xA9,0xA9,0xDC,0x57,0x31,0xA5,0xE2,0xAE,0x87,0x9C,0x47,0x21,0x5C,0x25,0x59,0xD5},
    {0x44,0xD5,0x3D,0xFC,0x29,0xD7,0x94,0x3A,0x95,0xD8,0x93,0x71,0xDA,0x58,0xEC,0x64}
};
static const unsigned char mask[16] = {
    0x85,0x56,0xC8,0xCB,0x61,0x40,0xA7,0xF9,
    0xA5,0x12,0x3A,0xC7,0x57,0x1B,0xEE,0x1C
};
static const unsigned char target[32] = {
    0x93,0x0A,0x52,0xA1,0xBA,0xB9,0x7C,0xA2,
    0x96,0x63,0x32,0x13,0x7C,0x99,0xE9,0x92,
    0x98,0xEA,0x61,0x82,0xFB,0x32,0xAB,0x63,
    0xA3,0x42,0x1D,0xFB,0x4F,0xD8,0xC9,0xE0
};

int main(void) {
    unsigned char candidate[16], hash[32];
    const uint32_t trials = 43046721u;
    for (uint32_t n = 0; n < trials; n++) {
        uint32_t x = n;
        for (int i = 0; i < 16; i++) {
            unsigned int k = x % 3;
            x /= 3;
            candidate[i] = payload[k][i] ^ mask[i];
        }
        SHA256(candidate, sizeof(candidate), hash);
        if (memcmp(hash, target, sizeof(target)) == 0) {
            printf("FOUND n=%u K04=", n);
            for (int j = 0; j < 16; j++) printf("%02X", candidate[j]);
            putchar('\n');
            return 0;
        }
    }
    printf("NO_MATCH tested=%u\n", trials);
    return 1;
}
