/* H-17 K08 bounded source-preserving deletion test.
   Enumerates every nonempty ordered word subsequence of the cited Emily
   sentence from note N02, N06, N10, N13, or N20. No inserted/reordered
   words are permitted. N20 uses its first sentence, as marked below.
   Tests HMAC-SHA256(nonce, normalized lowercase ASCII phrase)[:16] by
   SHA-256 against the unchanged K08 inventory commitment.

   Requires a C11-compatible compiler and OpenSSL libcrypto.
   Argument: note number in {2,6,10,13,20}.
   A negative result excludes only these exact subsequence candidate classes.
*/
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/hmac.h>
#include <openssl/sha.h>

static const unsigned char nonce[16] = {
    0x5f,0x93,0x3d,0xa6,0xa1,0xbd,0x03,0xc3,
    0x2d,0xa5,0xcb,0xc2,0x53,0x44,0xf4,0x97
};
static const unsigned char target[32] = {
    0x28,0x5e,0xb6,0xb4,0x19,0x6d,0x21,0xea,
    0xf4,0x7e,0x25,0x14,0x49,0xe6,0x1e,0x0b,
    0xce,0x28,0x74,0x98,0x81,0xcc,0xc5,0xa0,
    0x65,0xca,0x73,0x3b,0x0c,0x3f,0xd7,0x47
};
static const char *source[] = {
    "a good watch leaves the room ready for the next pair of hands",
    "the little lamp stays on until the corridor has gone quiet",
    "the desk copy was meant to sound like us not like a quarterly report i kept going back to the photograph after the last cup",
    "at the end of the night the mugs stood beside the window and somebody had remembered to leave the little lamp on",
    "i wanted the line to hold the sea the end of the night and the voices at the table"
};
static const int note_ids[] = {2, 6, 10, 13, 20};

int main(int argc, char **argv) {
    if (argc != 2) {
        fputs("Specify note number: 2, 6, 10, 13, or 20\n", stderr);
        return 2;
    }
    int id = atoi(argv[1]), idx = -1;
    for (int i = 0; i < 5; i++)
        if (note_ids[i] == id) idx = i;
    if (idx < 0) return 2;

    char src[512];
    strcpy(src, source[idx]);
    char *words[32], *word = strtok(src, " ");
    int n = 0;
    while (word) {
        words[n++] = word;
        word = strtok(NULL, " ");
    }

    uint64_t end = 1ULL << n;
    unsigned char mac[32], digest[32];
    unsigned int maclen;
    for (uint64_t bits = 1; bits < end; bits++) {
        char phrase[512];
        int pos = 0;
        for (int i = 0; i < n; i++) {
            if (!(bits & (1ULL << i))) continue;
            int length = (int)strlen(words[i]);
            if (pos) phrase[pos++] = ' ';
            memcpy(phrase + pos, words[i], length);
            pos += length;
        }
        phrase[pos] = '\0';
        HMAC(EVP_sha256(), nonce, sizeof(nonce),
             (const unsigned char *)phrase, pos, mac, &maclen);
        SHA256(mac, 16, digest);
        if (memcmp(digest, target, sizeof(target)) == 0) {
            printf("FOUND note=%d caption=%s K08=", id, phrase);
            for (int j = 0; j < 16; j++) printf("%02X", mac[j]);
            putchar('\n');
            return 0;
        }
    }
    printf("NO_MATCH note=%d words=%d candidates=%llu\n",
           id, n, (unsigned long long)(end - 1));
    return 1;
}
