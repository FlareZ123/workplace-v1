/* H-17 K04: exhaustive exactly-four-distinct-hex-nibble correction test.
 * Source-selected baseline and original acceptance digest are pinned below.
 * Requires OpenSSL libcrypto; read-only. Exit 0=found, 1=no match.
 * Args: first_a exclusive_end_a first_c exclusive_end_c
 */
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
int main(int argc,char **argv){
 static const uint8_t original[16]={0x2C,0xFF,0x14,0x9C,0x50,0xE5,0x45,0x57,0x22,0x8E,0x7D,0xE6,0x0B,0x3E,0xB7,0xC9};
 static const uint8_t target[32]={0x93,0x0A,0x52,0xA1,0xBA,0xB9,0x7C,0xA2,0x96,0x63,0x32,0x13,0x7C,0x99,0xE9,0x92,0x98,0xEA,0x61,0x82,0xFB,0x32,0xAB,0x63,0xA3,0x42,0x1D,0xFB,0x4F,0xD8,0xC9,0xE0};
 static const uint8_t baseline[32]={0x11,0xA7,0xF6,0x06,0x47,0x81,0xA6,0xAC,0x76,0x78,0xDC,0x6D,0xD2,0x47,0x59,0xAF,0x95,0x98,0x1C,0x8A,0x92,0x7F,0x8D,0xA4,0x43,0x65,0x15,0x35,0x4D,0x34,0x54,0x9B};
 uint8_t b[16],h[32];
 unsigned long long count=0;
 int start=0,end=29,cstart=0,cend=30;
 if(argc>1)start=atoi(argv[1]);
 if(argc>2)end=atoi(argv[2]);
 if(argc>3)cstart=atoi(argv[3]);
 if(argc>4)cend=atoi(argv[4]);
 if(start<0||end>29||start>=end) return 3;
 SHA256(original,16,h);
 if(memcmp(h,baseline,32))return 4;
 memcpy(b,original,16);
 for(int a=start;a<end;a++){
  for(int c=a+1;c<30;c++){
   if(c<cstart || c>=cend)continue;
   for(int d=c+1;d<31;d++)for(int e=d+1;e<32;e++){
    int ps[4]={a,c,d,e};
    uint8_t masks[4];
    for(int i=0;i<4;i++)masks[i]=((ps[i]&1)?0x0F:0xF0);
    for(int v1=1;v1<16;v1++)for(int v2=1;v2<16;v2++)for(int v3=1;v3<16;v3++)for(int v4=1;v4<16;v4++){
     uint8_t delta[4]={(uint8_t)v1,(uint8_t)v2,(uint8_t)v3,(uint8_t)v4};
     for(int i=0;i<4;i++){
      int pos=ps[i];
      b[pos/2]=(uint8_t)((b[pos/2]&~masks[i])|((original[pos/2] ^ (delta[i]<<(pos&1?0:4)))&masks[i]));
     }
     SHA256(b,16,h);
     count++;
     if(!memcmp(h,target,32)){
      printf("MATCH a=%d,c=%d,d=%d,e=%d deltas=%d,%d,%d,%d key=",a,c,d,e,v1,v2,v3,v4);
      for(int j=0;j<16;j++)printf("%02X",b[j]);
      puts("");
      return 0;
     }
     memcpy(b,original,16);
    }
   }
   printf("a=%d,c=%d count=%llu\n",a,c,count);
   fflush(stdout);
  }
 }
 printf("NO_MATCH count=%llu\n",count);
 return 1;
}
