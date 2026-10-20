/*
 * H-17 K04: exact seven-bit differences spanning exactly five bytes.
 * Evidence: original archive-labels.ini, spool-reconstruction.log,
 * recovery-routing.json and acceptance.json, with all source bytes unchanged.
 * Standalone OpenSSL C SFT. Compile: cc -O3 -Wall -Wextra -Werror
 * k04_fivebyte_sevenbit_burst_sft.c -lcrypto -o k04_fivebyte_sevenbit_burst_sft
 */
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static const uint8_t BASE[16] = {
    0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,
    0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9
};
static const uint8_t ORIGINAL_TARGET[32] = {
    0x93,0x0a,0x52,0xa1,0xba,0xb9,0x7c,0xa2,
    0x96,0x63,0x32,0x13,0x7c,0x99,0xe9,0x92,
    0x98,0xea,0x61,0x82,0xfb,0x32,0xab,0x63,
    0xa3,0x42,0x1d,0xfb,0x4f,0xd8,0xc9,0xe0
};

static void mutate(uint8_t output[16], int start, const int positions[7]) {
    memcpy(output, BASE, sizeof(BASE));
    for (int j=0; j<7; ++j)
        output[start+positions[j]/8] ^= (uint8_t)(1u << (positions[j]%8));
}
static int search(const uint8_t target[32], int synthetic) {
    uint8_t candidate[16], digest[32];
    uint64_t assignments=0;
    for (int start=0; start<=(synthetic ? 0 : 11); ++start) {
        int p[7]={0,1,2,3,4,5,6};
        uint64_t current=0;
        for (;;) {
            /* An exact five-byte span touches both endpoint bytes.
               All one-to-four-byte spans were exhausted in prior work. */
            if (p[0]<8 && p[6]>=32) {
                mutate(candidate,start,p);
                SHA256(candidate,sizeof(candidate),digest);
                ++current;
                if (memcmp(digest,target,sizeof(digest))==0) {
                    printf("%s HIT window=%d local_bits=",synthetic ? "SYNTHETIC":"ORIGINAL",start);
                    for(int j=0;j<7;++j)printf("%s%d",j?",":"",p[j]);
                    printf(" candidate=");
                    for(int j=0;j<16;++j)printf("%02X",candidate[j]);
                    putchar('\n');
                    return synthetic ? 0 : 2;
                }
            }
            int i=6;
            while(i>=0 && p[i]==40-7+i)--i;
            if(i<0)break;
            ++p[i];
            for(int j=i+1;j<7;++j)p[j]=p[j-1]+1;
        }
        assignments+=current;
        printf("ORIGINAL window=%d candidates=%llu cumulative=%llu\n",
               start,(unsigned long long)current,(unsigned long long)assignments);
        fflush(stdout);
    }
    if(synthetic){fputs("Synthetic positive control not found\n",stderr);return 3;}
    printf("ORIGINAL NO_MATCH unique_minimum_five_byte_span_seven_bit_candidates=%llu\n",
           (unsigned long long)assignments);
    return assignments==UINT64_C(147095424) ? 0 : 4;
}
int main(void) {
    const int synthetic_bits[7]={0,1,2,3,4,5,32};
    uint8_t synthetic[16],digest[32];
    mutate(synthetic,0,synthetic_bits);
    SHA256(synthetic,sizeof(synthetic),digest);
    if(search(digest,1))return 1;
    SHA256(BASE,sizeof(BASE),digest);
    if(memcmp(digest,ORIGINAL_TARGET,32)==0){
        fputs("Original baseline unexpectedly accepted\n",stderr);
        return 5;
    }
    return search(ORIGINAL_TARGET,0);
}
