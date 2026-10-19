/* H-17 K04 finite printer word-lane XOR corruption test.
 * Source: retained ESC-N attempt-2 ACK plus copied XOR mask.
 * The four 32-bit words receive the SAME candidate XOR delta.
 * The corruption mechanism is hypothetical. Original evidence unchanged.
 */
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>

static const uint8_t baseline[16] = {
  0x2C,0xFF,0x14,0x9C,0x50,0xE5,0x45,0x57,
  0x22,0x8E,0x7D,0xE6,0x0B,0x3E,0xB7,0xC9
};
static const uint8_t committed[32] = {
  0x93,0x0A,0x52,0xA1,0xBA,0xB9,0x7C,0xA2,
  0x96,0x63,0x32,0x13,0x7C,0x99,0xE9,0x92,
  0x98,0xEA,0x61,0x82,0xFB,0x32,0xAB,0x63,
  0xA3,0x42,0x1D,0xFB,0x4F,0xD8,0xC9,0xE0
};
static uint8_t found_candidate[16];
static unsigned found = 0;

static double now_seconds(void) {
  struct timespec t;
  clock_gettime(CLOCK_MONOTONIC,&t);
  return t.tv_sec + (double)t.tv_nsec / 1e9;
}
int main(int argc,char **argv) {
  const int synthetic = argc>1 && strcmp(argv[1],"synthetic")==0;
  uint8_t goal_bytes[32];
  uint32_t initial[4];
  memcpy(initial,baseline,16);
  if (synthetic) {
    uint32_t target[4];
    for(int i=0;i<4;i++)target[i]=initial[i]^0x1234BEEFU;
    SHA256((const uint8_t *)target,16,goal_bytes);
  } else {
    uint8_t check[32];
    const uint8_t known_prefix[4]={0x11,0xA7,0xF6,0x06};
    SHA256(baseline,16,check);
    if(memcmp(check,known_prefix,4))return 5;
    memcpy(goal_bytes,committed,32);
  }
  uint32_t goal[8];
  for(int i=0;i<8;i++) {
    goal[i]=((uint32_t)goal_bytes[4*i]<<24)
          | ((uint32_t)goal_bytes[4*i+1]<<16)
          | ((uint32_t)goal_bytes[4*i+2]<<8)
          | goal_bytes[4*i+3];
  }
  uint32_t begin_hi=0,end_hi=65536U;
  if(!synthetic && argc==3) {
    begin_hi=(uint32_t)strtoul(argv[1],NULL,10);
    end_hi=(uint32_t)strtoul(argv[2],NULL,10);
    if(begin_hi>=end_hi || end_hi>65536U)return 7;
  }
  uint64_t count=0;
  double t0=now_seconds();
  #pragma omp parallel for schedule(dynamic,4) reduction(+:count)
  for(uint32_t hi=synthetic?0x1234:begin_hi;
      hi<(synthetic?0x1235:end_hi);hi++) {
    uint32_t block[16]={0};
    block[4]=0x00000080U;
    block[15]=0x80000000U;
    SHA256_CTX seeded;
    SHA256_Init(&seeded);
    for(uint32_t lo=0;lo<65536U;lo++) {
      const uint32_t delta=(hi<<16)|lo;
      for(int i=0;i<4;i++)block[i]=initial[i]^delta;
      SHA256_CTX state=seeded;
      SHA256_Transform(&state,(uint8_t *)block);
      count++;
      if(state.h[0]==goal[0]&&state.h[1]==goal[1]
         &&state.h[2]==goal[2]&&state.h[3]==goal[3]
         &&state.h[4]==goal[4]&&state.h[5]==goal[5]
         &&state.h[6]==goal[6]&&state.h[7]==goal[7]) {
        #pragma omp critical
        {
          if(!found) {
            found=1;
            memcpy(found_candidate,block,16);
          }
        }
      }
    }
  }
  printf("mode=%s candidates=%llu matches=%u elapsed_seconds=%.3f\n",
       synthetic?"synthetic":"original",
       (unsigned long long)count,found,now_seconds()-t0);
  if(found) {
    printf("candidate=");
    for(int i=0;i<16;i++)printf("%02X",found_candidate[i]);
    puts("");
  }
  if(synthetic) {
    uint32_t expected[4];
    for(int i=0;i<4;i++)expected[i]=initial[i]^0x1234BEEFU;
    return found&&!memcmp(found_candidate,expected,16)?0:6;
  }
  return found?2:0;
}
