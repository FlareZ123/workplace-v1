/* H-17 K04 bounded media-error diagnostic. Requires OpenSSL libcrypto.
   Explicitly tests bit-flip Hamming balls only; it does not authenticate an ACK. */
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

static const uint8_t original[16] = {
    0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,
    0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9
};
static const uint8_t target[32] = {
    0x93,0x0a,0x52,0xa1,0xba,0xb9,0x7c,0xa2,
    0x96,0x63,0x32,0x13,0x7c,0x99,0xe9,0x92,
    0x98,0xea,0x61,0x82,0xfb,0x32,0xab,0x63,
    0xa3,0x42,0x1d,0xfb,0x4f,0xd8,0xc9,0xe0
};
static uint8_t trial[16];
static uint64_t checks;
static int found;

static void search(int remaining, int next) {
    if (found) return;
    if (remaining == 0) {
        uint8_t digest[SHA256_DIGEST_LENGTH];
        SHA256(trial, sizeof(trial), digest);
        checks++;
        if (memcmp(digest, target, sizeof(target)) == 0) {
            found = 1;
            fputs("MATCH: ", stdout);
            for (size_t i = 0; i < sizeof(trial); i++) printf("%02X", trial[i]);
            putchar('\n');
        }
        return;
    }
    for (int i=next; i <= 128-remaining; i++) {
        trial[i >> 3] ^= (uint8_t)(1u << (i & 7));
        search(remaining-1, i+1);
        trial[i >> 3] ^= (uint8_t)(1u << (i & 7));
        if (found) return;
    }
}

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "Usage: shard <weight> <worker> <shards>\n"); return 2; }
    int weight = atoi(argv[1]), worker = atoi(argv[2]), shards = atoi(argv[3]);
    if (weight < 1 || weight > 6 || shards < 1 || worker < 0 || worker >= shards) return 2;
    memcpy(trial, original, sizeof(original));
    for (int i=worker; i<=128-weight; i+=shards) {
        trial[i>>3] ^= (uint8_t)(1u << (i&7));
        search(weight-1, i+1);
        trial[i>>3] ^= (uint8_t)(1u << (i&7));
        if (found) break;
    }
    printf("weight=%d worker=%d/%d checked=%llu found=%d\n", weight, worker, shards,
        (unsigned long long)checks, found);
    fflush(stdout);
    return found ? 0 : 1;
}
