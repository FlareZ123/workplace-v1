/* H17 K04: exhaustive replacement of one aligned four-byte MT payload word.
 * Exact SHA256 of the sixteen-byte masked component, original commitment unchanged.
 * Read-only; C/OpenSSL/OpenMP. Selftest replaces bytes 4..7 with 010203A5.
 */
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
static const unsigned char base[16]={0x2C,0xFF,0x14,0x9C,0x50,0xE5,0x45,0x57,0x22,0x8E,0x7D,0xE6,0x0B,0x3E,0xB7,0xC9};
static const unsigned char committed[32]={0x93,0x0A,0x52,0xA1,0xBA,0xB9,0x7C,0xA2,0x96,0x63,0x32,0x13,0x7C,0x99,0xE9,0x92,0x98,0xEA,0x61,0x82,0xFB,0x32,0xAB,0x63,0xA3,0x42,0x1D,0xFB,0x4F,0xD8,0xC9,0xE0};
static unsigned char solution[16];
static int found=0;
static double clock_now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+(double)t.tv_nsec/1e9;}
int main(int argc,char**argv){
 int selftest=(argc>=2 && strcmp(argv[1],"selftest")==0);
 int slot_begin=0,slot_end=4,hi_begin=0,hi_end=256;
 if(selftest){slot_begin=1;slot_end=2;hi_begin=0xA5;hi_end=0xA6;}
 else if(argc==5){slot_begin=atoi(argv[1]);slot_end=atoi(argv[2]);hi_begin=atoi(argv[3]);hi_end=atoi(argv[4]);}
 if(slot_begin<0||slot_end>4||slot_begin>=slot_end||hi_begin<0||hi_end>256||hi_begin>=hi_end)return 3;
 unsigned char expected[32];memcpy(expected,committed,32);
 if(selftest){unsigned char known[16];memcpy(known,base,16);known[4]=0x01;known[5]=0x02;known[6]=0x03;known[7]=0xA5;SHA256(known,16,expected);}
 uint32_t expect[8];for(int i=0;i<8;i++)expect[i]=((uint32_t)expected[i*4]<<24)|((uint32_t)expected[i*4+1]<<16)|((uint32_t)expected[i*4+2]<<8)|expected[i*4+3];
 unsigned long long checked=0;const double start=clock_now();
 fprintf(stderr,"K04 4byte-aligned scan slots=[%d,%d) hi=[%d,%d) threads=%d selftest=%d\n",slot_begin,slot_end,hi_begin,hi_end,omp_get_max_threads(),selftest);
 #pragma omp parallel for collapse(2) schedule(dynamic,1) reduction(+:checked)
 for(int slot=slot_begin;slot<slot_end;slot++)for(int hi=hi_begin;hi<hi_end;hi++){
  SHA256_CTX init,st;SHA256_Init(&init);
  unsigned char block[64]={0};memcpy(block,base,16);block[16]=0x80;block[63]=0x80;
  int idx=slot*4;block[idx+3]=(unsigned char)hi;
  for(uint32_t lo=0;lo<0x1000000;lo++){
   block[idx]=(unsigned char)lo;block[idx+1]=(unsigned char)(lo>>8);block[idx+2]=(unsigned char)(lo>>16);
   memcpy(&st,&init,sizeof(st));SHA256_Transform(&st,block);++checked;
   if(st.h[0]!=expect[0])continue;
   int match=1;for(int j=1;j<8;j++)if(st.h[j]!=expect[j]){match=0;break;}
   if(match){
    #pragma omp critical
    {if(!found){found=1;memcpy(solution,block,16);}}
   }
  }
  if(((slot-slot_begin)*256+hi-hi_begin)%64==0){
   #pragma omp critical
   {fprintf(stderr,"progress slot=%d hi=%d elapsed=%.2fs\n",slot,hi,clock_now()-start);fflush(stderr);}
  }
 }
 printf("checked=%llu elapsed=%.3f found=%d\n",checked,clock_now()-start,found);
 if(found){printf("solution=");for(int i=0;i<16;i++)printf("%02X",solution[i]);printf("\n");}
 return selftest?(found?0:2):(found?0:1);
}
