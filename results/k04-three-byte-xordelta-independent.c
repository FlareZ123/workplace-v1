/* Independent exactly-three-byte K04 exclusion audit.
 * Enumerate nonzero XOR deltas instead of raw replacement bytes.
 * Runtime: OpenSSL 1-block SHA-256, OpenMP. Source records untouched.
 */
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>

static const unsigned char base[16] = {0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9};
static const unsigned char original_target[32] = {0x93,0x0a,0x52,0xa1,0xba,0xb9,0x7c,0xa2,0x96,0x63,0x32,0x13,0x7c,0x99,0xe9,0x92,0x98,0xea,0x61,0x82,0xfb,0x32,0xab,0x63,0xa3,0x42,0x1d,0xfb,0x4f,0xd8,0xc9,0xe0};
struct triple { int x,y,z; };
static struct triple triples[560];
static unsigned char found_bytes[16];
static int found=0;
static double wall(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int main(int argc,char **argv){
    int synthetic=(argc>1 && strcmp(argv[1],"synthetic")==0);
    int count=0, select=-1;
    for(int x=0;x<16;x++)for(int y=x+1;y<16;y++)for(int z=y+1;z<16;z++){
        triples[count]=(struct triple){x,y,z};
        if(x==1 && y==7 && z==14)select=count;
        count++;
    }
    if(count!=560||select<0)return 3;
    unsigned char digest[32],known[16];
    memcpy(known,base,16);
    if(synthetic){known[1]^=0x03;known[7]^=0x08;known[14]^=0x30;SHA256(known,16,digest);}
    else memcpy(digest,original_target,32);
    uint32_t wanted[8];
    for(int i=0;i<8;i++)wanted[i]=((uint32_t)digest[4*i]<<24)|((uint32_t)digest[4*i+1]<<16)|((uint32_t)digest[4*i+2]<<8)|digest[4*i+3];
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    unsigned char block_test[64]={0};
    memcpy(block_test,base,16);block_test[16]=0x80;block_test[63]=0x80;
    SHA256_CTX s=ctx;SHA256_Transform(&s,block_test);
    SHA256(base,16,digest);
    for(int i=0;i<8;i++){
       uint32_t word=((uint32_t)digest[4*i]<<24)|((uint32_t)digest[4*i+1]<<16)|((uint32_t)digest[4*i+2]<<8)|digest[4*i+3];
       if(word!=s.h[i]){fprintf(stderr,"padding selfcheck failed at %d\n",i);return 4;}
    }
    const int start=synthetic?select:0,stop=synthetic?select+1:560;
    unsigned long long checked=0;
    double t0=wall();
    #pragma omp parallel for schedule(dynamic,1) reduction(+:checked)
    for(int index=start;index<stop;index++){
        const struct triple t=triples[index];
        unsigned char block[64]={0};memcpy(block,base,16);block[16]=0x80;block[63]=0x80;
        SHA256_CTX init;SHA256_Init(&init);
        for(int dx=1;dx<256;dx++){
            block[t.x]=base[t.x]^(unsigned char)dx;
            for(int dy=1;dy<256;dy++){
                block[t.y]=base[t.y]^(unsigned char)dy;
                for(int dz=1;dz<256;dz++){
                    block[t.z]=base[t.z]^(unsigned char)dz;
                    SHA256_CTX state=init;
                    SHA256_Transform(&state,block);
                    checked++;
                    if(state.h[0]!=wanted[0] || state.h[1]!=wanted[1])continue;
                    int ok=1;
                    for(int i=2;i<8;i++)if(state.h[i]!=wanted[i]){ok=0;break;}
                    if(ok){
                        #pragma omp critical
                        {if(!found){found=1;memcpy(found_bytes,block,16);}}
                    }
                }
            }
        }
    }
    printf("mode=%s triples=%d assignments=%llu matches=%d elapsed_sec=%.3f\n",synthetic?"synthetic":"original",stop-start,checked,found,wall()-t0);
    if(found){printf("solution=");for(int i=0;i<16;i++)printf("%02X",found_bytes[i]);printf("\n");}
    return synthetic?(found&&memcmp(known,found_bytes,16)==0?0:2):(found?2:0);
}
