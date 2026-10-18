/* H-17 K04 lower-bound cross-check. Read-only; requires OpenSSL libcrypto.
 * Reconstructs the original K04 component from a documented fixed source
 * and tests all changes affecting <=2 bytes, then exactly 3 hex nibbles.
 * These are diagnostic hypothetical corrections, not authenticated media.
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

static const uint8_t base[16] = {
    0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,
    0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9
};
static const uint8_t target[32] = {
    0x93,0x0a,0x52,0xa1,0xba,0xb9,0x7c,0xa2,
    0x96,0x63,0x32,0x13,0x7c,0x99,0xe9,0x92,
    0x98,0xea,0x61,0x82,0xfb,0x32,0xab,0x63,
    0xa3,0x42,0x1d,0xfb,0x4f,0xd8,0xc9,0xe0
};
static uint8_t x[16], digest[32];
static uint64_t checks;

static int matches(void) {
    SHA256(x, sizeof(x), digest);
    checks++;
    return memcmp(target, digest, sizeof(target)) == 0;
}
static void flip_nibble(int n, int delta) {
    x[n / 2] ^= (uint8_t)(delta << (n % 2 == 0 ? 4 : 0));
}
int main(void) {
    uint8_t baseline_sha[32];
    memcpy(x, base, sizeof(x));
    SHA256(x, sizeof(x), baseline_sha);
    if (memcmp(baseline_sha, target, sizeof(target)) == 0) return 2;

    for (int a = 0; a < 16; a++)
        for (int b = a + 1; b < 16; b++) {
            for (int va = 0; va < 256; va++)
                for (int vb = 0; vb < 256; vb++) {
                    x[a] = (uint8_t)va;
                    x[b] = (uint8_t)vb;
                    if (matches()) { puts("FOUND two-byte assignment"); return 3; }
                }
            x[a] = base[a];
            x[b] = base[b];
        }
    printf("two_byte_assignments=%llu matches=0\n",
           (unsigned long long)checks);

    uint64_t earlier = checks;
    for (int a = 0; a < 32; a++)
        for (int b = a + 1; b < 32; b++)
            for (int c = b + 1; c < 32; c++)
                for (int da = 1; da <= 15; da++) {
                    flip_nibble(a, da);
                    for (int db = 1; db <= 15; db++) {
                        flip_nibble(b, db);
                        for (int dc = 1; dc <= 15; dc++) {
                            flip_nibble(c, dc);
                            if (matches()) { puts("FOUND three-nibble change"); return 4; }
                            flip_nibble(c, dc);
                        }
                        flip_nibble(b, db);
                    }
                    flip_nibble(a, da);
                }
    printf("three_nibble_assignments=%llu matches=0\n",
           (unsigned long long)(checks - earlier));
    return memcmp(x, base, sizeof(x)) == 0 ? 0 : 5;
}
