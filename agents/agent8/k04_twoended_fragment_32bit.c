/* K04 original commitment direct four-boundary-byte candidate class.

   Tested original source coupon K0 = P_selected XOR M_original from H-17
   c-energy-group-documents2026.zip. Source pins and exact derivation:
   results/h17-k04-two-ended-fragment-32bit-bound.md.

   Enumerates all sixteen-byte candidates that differ from the reported
   K04 baseline ONLY at bytes 0,1,14,15 (count 2^32). This is a bounded,
   unproven media-fragment-end hypothesis, not an asserted authentic
   printer repair. No original source files are modified.

   Build with a C compiler supporting OpenMP and OpenSSL libcrypto.
   Run four arguments? See main usage: start_hi stop_hi mode.
   The sixteen 4096-wide high ranges [0,4096),...,[61440,65536)
   cover the full class. Any MATCH is reported immediately. Original
   no-match completion intentionally returns exit code 1.
*/
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>

static const uint8_t baseline[16] = {
    0x2C,0xFF,0x14,0x9C,0x50,0xE5,0x45,0x57,
    0x22,0x8E,0x7D,0xE6,0x0B,0x3E,0xB7,0xC9
};
static const uint32_t original_digest[8] = {
 0x930a52a1, 0xbab97ca2, 0x96633213, 0x7c99e992,
 0x98ea6182, 0xfb32ab63, 0xa3421dfb, 0x4fd8c9e0
};

static int equals_digest(const SHA256_CTX *ctx,const uint32_t expect[8]){
    return ctx->h[0]==expect[0] && ctx->h[1]==expect[1] &&
           ctx->h[2]==expect[2] && ctx->h[3]==expect[3] &&
           ctx->h[4]==expect[4] && ctx->h[5]==expect[5] &&
           ctx->h[6]==expect[6] && ctx->h[7]==expect[7];
}

int main(int argc,char **argv){
    if(argc!=4){
        fprintf(stderr,"usage: h17_edges4 start_hi stop_hi original|synthetic\n");
        return 2;
    }
    char *end=0;
    uint32_t start=(uint32_t)strtoul(argv[1],&end,0);
    if(!*argv[1]||*end)return 2;
    uint32_t stop=(uint32_t)strtoul(argv[2],&end,0);
    if(!*argv[2]||*end||start>=stop||stop>65536)return 2;
    int synthetic=!strcmp(argv[3],"synthetic");
    if(!synthetic && strcmp(argv[3],"original")){
        fprintf(stderr,"mode invalid\n");
        return 2;
    }
    uint32_t expected[8];
    memcpy(expected,original_digest,sizeof(expected));
    if(synthetic){
        uint8_t blk[64]={0};
        memcpy(blk,baseline,16);
        blk[0]=0xAB;blk[1]=0xCD;
        blk[14]=0x12;blk[15]=0x67;
        blk[16]=0x80;blk[63]=128;
        SHA256_CTX test;
        SHA256_Init(&test);
        SHA256_Transform(&test,blk);
        memcpy(expected,test.h,sizeof(expected));
    }
    uint64_t matches=0;
    double began=omp_get_wtime();
#pragma omp parallel reduction(+:matches)
    {
        uint8_t block[64]={0};
        memcpy(block,baseline,16);
        block[16]=0x80;
        block[63]=128;
        SHA256_CTX work;
#pragma omp for schedule(dynamic,8)
        for(uint32_t hi=start;hi<stop;hi++){
            block[0]=(uint8_t)(hi>>8);
            block[1]=(uint8_t)hi;
            for(uint32_t lo=0;lo<65536u;lo++){
                block[14]=(uint8_t)(lo>>8);
                block[15]=(uint8_t)lo;
                SHA256_Init(&work);
                SHA256_Transform(&work,block);
                if(equals_digest(&work,expected)){
#pragma omp critical
                  {
                    printf("MATCH mode=%s payload-edge=%04X/%04X candidate=",
                           argv[3],hi,lo);
                    for(int j=0;j<16;j++)printf("%02X",block[j]);
                    printf("\n");
                    fflush(stdout);
                  }
                  matches++;
                }
            }
        }
    }
    double duration=omp_get_wtime()-began;
    printf("COMPLETE mode=%s hi=[%u,%u) candidates=%llu matches=%llu seconds=%.3f rate=%.3fM/s\n",
      argv[3],start,stop,
      (unsigned long long)(stop-start)*65536ull,
      (unsigned long long)matches,duration,
      ((stop-start)*65536.0/duration)/1e6);
    if(synthetic)
        return (start<=0xABCD&&stop>0xABCD&&matches==1)?0:3;
    return matches?0:1;
}
