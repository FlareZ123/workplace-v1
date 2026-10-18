/* Exhaustive exactly-three-distinct-byte K04 candidate correction test.
   Historical archive analysis only. No source, verifier or equipment writes.
   SHA256 compression of a padded 16-byte input; OpenSSL libcrypto, OpenMP.
   Return 0 on found, 1 on no match. "selftest" substitutes a known hash hit.
*/
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>
static const unsigned char base[16] = {
  0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,
  0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9
};
static const unsigned char target[32] = {
  0x93,0x0a,0x52,0xa1,0xba,0xb9,0x7c,0xa2,
  0x96,0x63,0x32,0x13,0x7c,0x99,0xe9,0x92,
  0x98,0xea,0x61,0x82,0xfb,0x32,0xab,0x63,
  0xa3,0x42,0x1d,0xfb,0x4f,0xd8,0xc9,0xe0
};
struct triple { int a,b,c; };
static struct triple triple[560];
static unsigned char solution[16];
static int found=0;
static double now_s(void) {
  struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
  return (double)t.tv_sec + (double)t.tv_nsec*1e-9;
}
int main(int argc,char **argv) {
  int count=0;
  for(int a=0;a<16;a++) for(int b=a+1;b<16;b++)
    for(int c=b+1;c<16;c++) triple[count++]=(struct triple){a,b,c};
  if(count!=560) return 3;
  int selftest=(argc>1 && strcmp(argv[1],"selftest")==0);
  int begin=0,end=count;
  unsigned char expected[32];
  memcpy(expected,target,32);
  if(selftest) {
    for(int i=0;i<560;i++) if(triple[i].a==0 && triple[i].b==5 && triple[i].c==15) {
      begin=i;end=i+1;break;
    }
    unsigned char known[16];memcpy(known,base,16);
    known[0]^=0x01;known[5]^=0x02;known[15]^=0x04;
    SHA256(known,16,expected);
  } else if(argc==3) {
    begin=atoi(argv[1]);end=atoi(argv[2]);
    if(begin<0||end>560||end<=begin) return 3;
  }
  uint32_t expected_words[8];
  for(int i=0;i<8;i++) {
    int j=4*i; expected_words[i]=((uint32_t)expected[j]<<24)
      |((uint32_t)expected[j+1]<<16)|((uint32_t)expected[j+2]<<8)|expected[j+3];
  }
  unsigned long long checked=0;
  double start=now_s();
  fprintf(stderr,"K04 scan start: combinations=%d..%d, threads=%d, selftest=%d\n",
          begin,end,omp_get_max_threads(),selftest);
  #pragma omp parallel for schedule(dynamic,1) reduction(+:checked)
  for(int i=begin;i<end;i++) {
    struct triple t=triple[i];
    unsigned char block[64]={0};
    memcpy(block,base,16);block[16]=0x80;block[63]=0x80;
    SHA256_CTX initial,state;SHA256_Init(&initial);
    for(int x=0;x<256;x++) {
      if(x==base[t.a]) continue;
      block[t.a]=(unsigned char)x;
      for(int y=0;y<256;y++) {
        if(y==base[t.b]) continue;
        block[t.b]=(unsigned char)y;
        for(int z=0;z<256;z++) {
          if(z==base[t.c]) continue;
          block[t.c]=(unsigned char)z;
          memcpy(&state,&initial,sizeof(state));
          SHA256_Transform(&state,block);
          checked++;
          int same=1;
          for(int h=0;h<8;h++) if(state.h[h]!=expected_words[h]){same=0;break;}
          if(same) {
            #pragma omp critical
            {if(!found){found=1;memcpy(solution,block,16);}}
          }
        }
      }
    }
    if((i-begin)%20==0) {
      #pragma omp critical
      {fprintf(stderr,"progress triple=%d elapsed=%.1fs\n",i,now_s()-start);fflush(stderr);}
    }
  }
  printf("checked=%llu elapsed=%.4f found=%d\n",checked,now_s()-start,found);
  if(found) {
    printf("solution=");
    for(int i=0;i<16;i++)printf("%02X",solution[i]);
    printf("\n");
  }
  return selftest?(found?0:2):(found?0:1);
}
