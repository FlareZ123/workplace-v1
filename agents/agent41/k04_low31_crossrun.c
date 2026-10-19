/* Agent41: bounded low31 paired-window source-coupon scan. SHA256 via OpenSSL.
   Data input is original SHA256-pinned recorder/RC17 four-word runs, original
   intact printer row43 word3, route mask and original K04 commitment.
   The disputed selected row129 is never provided to this program.
*/
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

#define MAXRUNS 512
static uint32_t runs[MAXRUNS][4];

static uint32_t twist(uint32_t a, uint32_t b) {
    uint32_t x = (a & 0x80000000U) | (b & 0x7FFFFFFFU);
    return (x >> 1) ^ ((b & 1U) ? 0x9908B0DFU : 0U);
}

static uint32_t temper(uint32_t x) {
    x ^= x >> 11;
    x ^= (x << 7) & 0x9D2C5680U;
    x ^= (x << 15) & 0xEFC60000U;
    return x ^ (x >> 18);
}

static uint32_t read32(FILE *f) {
    unsigned char v[4];
    if (fread(v, 1, 4, f) != 4) {
        fputs("TRUNCATED INPUT\n", stderr);
        exit(2);
    }
    return (uint32_t)v[0] | ((uint32_t)v[1] << 8)
         | ((uint32_t)v[2] << 16) | ((uint32_t)v[3] << 24);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fputs("requires binary input\n", stderr);
        return 2;
    }
    FILE *f = fopen(argv[1], "rb");
    if (!f) {
        perror("fopen");
        return 2;
    }
    uint32_t n = read32(f);
    if (n != 298 || n > MAXRUNS) {
        fputs("UNEXPECTED N\n", stderr);
        return 2;
    }
    for (uint32_t i = 0; i < n; i++)
        for (int j = 0; j < 4; j++)
            runs[i][j] = read32(f);
    uint32_t x3 = read32(f);
    unsigned char mask[16], want[32], digest[SHA256_DIGEST_LENGTH];
    if (fread(mask, 1, 16, f) != 16 || fread(want, 1, 32, f) != 32) {
        fputs("TRUNCATED MASK\n", stderr);
        return 2;
    }
    if (fgetc(f) != EOF) {
        fputs("EXTRA INPUT\n", stderr);
        return 2;
    }
    fclose(f);
    unsigned long long tested = 0;
    unsigned int hits = 0;
    for (uint32_t ai = 0; ai < n; ai++) {
        for (uint32_t bi = 0; bi < n; bi++) {
            for (uint32_t bits = 0; bits < 128; bits++) {
                unsigned char candidate[16];
                for (int j = 0; j < 4; j++) {
                    uint32_t prev = j == 0 ? x3 :
                        (runs[ai][j-1] | (((bits >> (j-1)) & 1U) << 31));
                    uint32_t next = runs[ai][j];
                    uint32_t later = runs[bi][j] |
                        (((bits >> (j+3)) & 1U) << 31);
                    uint32_t result = temper(later ^ twist(prev, next));
                    for (int k = 0; k < 4; k++)
                        candidate[4*j+k] = ((result >> (8*k)) & 0xFFU)
                                          ^ mask[4*j+k];
                }
                SHA256(candidate, 16, digest);
                if (memcmp(digest, want, 32) == 0) {
                    hits++;
                    printf("HIT ai=%u bi=%u bits=%u coupon=", ai, bi, bits);
                    for (int j = 0; j < 16; j++) printf("%02X", candidate[j]);
                    putchar('\n');
                }
                tested++;
            }
        }
    }
    printf("TESTED=%llu HITS=%u\n", tested, hits);
    return tested == (unsigned long long)n*n*128 ? 0 : 3;
}
