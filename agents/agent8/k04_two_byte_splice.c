/* H-17 K04 source-bound two-byte internal splice test.

This original-case SFT uses the incident-date ESC-N RECOVER ACK row129
and its original transcribed XOR mask as fixed input. Explore every:
 (1) deleted pair position 0..14,
 (2) reinserted pair position 0..14,
 (3) independent two unknown byte values 0..65535.
The exact class has 225 * 65,536 = 14,745,600 assignments.
Original source details and SHA256: results/h17-k04-two-byte-internal-splice.md.
The producer-error model remains a hypothesis, not authenticated repair.
Use a C compiler, OpenSSL libcrypto, OpenMP. No source files are modified.
*/
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>

static const uint8_t original_payload[16] = {
  0xA9,0xA9,0xDC,0x57,0x31,0xA5,0xE2,0xAE,
  0x87,0x9C,0x47,0x21,0x5C,0x25,0x59,0xD5
};
static const uint8_t mask[16] = {
  0x85,0x56,0xC8,0xCB,0x61,0x40,0xA7,0xF9,
  0xA5,0x12,0x3A,0xC7,0x57,0x1B,0xEE,0x1C
};
static const uint32_t expected_original[8] = {
 0x930a52a1, 0xbab97ca2, 0x96633213, 0x7c99e992,
 0x98ea6182, 0xfb32ab63, 0xa3421dfb, 0x4fd8c9e0
};

static int equal(const SHA256_CTX *x, const uint32_t expected[8]){
    for(int k=0;k<8;k++)if(x->h[k]!=expected[k])return 0;
    return 1;
}
static void setup(uint8_t block[64], int delete_at,int insert_at){
    uint8_t kept[14];
    int k=0;
    for(int i=0;i<16;i++)
        if(i<delete_at || i>=delete_at+2) kept[k++]=original_payload[i];
    memset(block,0,64);
    for(int i=0;i<16;i++){
        if(i==insert_at || i==insert_at+1)block[i]=mask[i];
        else{
            int source=i<insert_at?i:i-2;
            block[i]=kept[source]^mask[i];
        }
    }
    block[16]=0x80;
    block[63]=128;
}
int main(int argc,char**argv){
    if(argc!=2||(strcmp(argv[1],"original")&&strcmp(argv[1],"synthetic"))){
        fprintf(stderr,"usage: h17_twobyte_splice original|synthetic\n");
        return 2;
    }
    uint32_t target[8];
    memcpy(target,expected_original,sizeof(target));
    if(!strcmp(argv[1],"synthetic")){
        uint8_t test[64];
        setup(test,2,10);
        test[10]=0xAB^mask[10];
        test[11]=0xCD^mask[11];
        SHA256_CTX sha;
        SHA256_Init(&sha);
        SHA256_Transform(&sha,test);
        memcpy(target,sha.h,sizeof(target));
    }
    uint64_t count=0,matches=0;
    double began=omp_get_wtime();
#pragma omp parallel reduction(+:matches,count)
    {
        SHA256_CTX sha;
        uint8_t block[64];
#pragma omp for collapse(2) schedule(dynamic,1)
        for(int delete_at=0;delete_at<15;delete_at++){
            for(int insert_at=0;insert_at<15;insert_at++){
                if(strcmp(argv[1],"original") &&
                   (delete_at!=2||insert_at!=10)) continue;
                setup(block,delete_at,insert_at);
                for(uint32_t v=0;v<65536;v++){
                    block[insert_at]=(uint8_t)(v>>8)^mask[insert_at];
                    block[insert_at+1]=(uint8_t)v^mask[insert_at+1];
                    SHA256_Init(&sha);
                    SHA256_Transform(&sha,block);
                    count++;
                    if(equal(&sha,target)){
#pragma omp critical
                      {
                        printf("MATCH mode=%s delete=%d insert=%d pair=%04X candidate=",
                               argv[1],delete_at,insert_at,v);
                        for(int k=0;k<16;k++)printf("%02X",block[k]);
                        printf("\n");
                        fflush(stdout);
                      }
                      matches++;
                    }
                }
            }
        }
    }
    printf("COMPLETE %s assignments=%llu matches=%llu seconds=%.3f\n",argv[1],
       (unsigned long long)count,
       (unsigned long long)matches,omp_get_wtime()-began);
    if(!strcmp(argv[1],"synthetic"))
        return (matches==1 && count==65536)?0:3;
    return matches?0:1;
}
