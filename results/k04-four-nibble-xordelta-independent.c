/* Independent K04 exactly-four-distinct-nibble exclusion audit.
 * XOR-and-restore 4-bit changes, OpenSSL one-block SHA-256, OpenMP.
 * No evidence or acceptance files are modified.
 */
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>
static const unsigned char baseline[16]={0x2c,0xff,0x14,0x9c,0x50,0xe5,0x45,0x57,0x22,0x8e,0x7d,0xe6,0x0b,0x3e,0xb7,0xc9};
static const unsigned char acceptance[32]={0x93,0x0a,0x52,0xa1,0xba,0xb9,0x7c,0xa2,0x96,0x63,0x32,0x13,0x7c,0x99,0xe9,0x92,0x98,0xea,0x61,0x82,0xfb,0x32,0xab,0x63,0xa3,0x42,0x1d,0xfb,0x4f,0xd8,0xc9,0xe0};
struct quartet{unsigned char p[4];};
static struct quartet quartets[35960];
static unsigned char solution[16];
static int found=0;
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int main(int argc,char **argv){
 int synthetic=(argc>1 && !strcmp(argv[1],"synthetic"));
 int n=0,selected=-1;
 for(int a=0;a<32;a++)for(int b=a+1;b<32;b++)for(int c=b+1;c<32;c++)for(int d=c+1;d<32;d++){
   quartets[n]=(struct quartet){{a,b,c,d}};
   if(a==0&&b==3&&c==18&&d==31)selected=n;
   n++;
 }
 if(n!=35960||selected<0)return 3;
 unsigned char expected[32],known[16];memcpy(known,baseline,16);
 if(synthetic){known[0]^=0x20;known[1]^=0x04;known[9]^=0x80;known[15]^=0x01;SHA256(known,16,expected);}
 else memcpy(expected,acceptance,32);
 uint32_t goal[8];
 for(int i=0;i<8;i++)goal[i]=((uint32_t)expected[4*i]<<24)|((uint32_t)expected[4*i+1]<<16)|((uint32_t)expected[4*i+2]<<8)|expected[4*i+3];
 unsigned long long count=0;double t0=now();
 int begin=synthetic?selected:0,end=synthetic?selected+1:n;
 #pragma omp parallel for schedule(dynamic,8) reduction(+:count)
 for(int q=begin;q<end;q++){
   int idx[4],shift[4];
   for(int i=0;i<4;i++){idx[i]=quartets[q].p[i]/2;shift[i]=(quartets[q].p[i]&1)?0:4;}
   unsigned char block[64]={0};memcpy(block,baseline,16);block[16]=0x80;block[63]=0x80;
   SHA256_CTX initial;SHA256_Init(&initial);
   for(int x=1;x<16;x++){
     block[idx[0]]^=(unsigned char)(x<<shift[0]);
     for(int y=1;y<16;y++){
       block[idx[1]]^=(unsigned char)(y<<shift[1]);
       for(int z=1;z<16;z++){
         block[idx[2]]^=(unsigned char)(z<<shift[2]);
         for(int w=1;w<16;w++){
           block[idx[3]]^=(unsigned char)(w<<shift[3]);
           SHA256_CTX current=initial;SHA256_Transform(&current,block);count++;
           int ok=1;for(int k=0;k<8;k++)if(current.h[k]!=goal[k]){ok=0;break;}
           if(ok){
             #pragma omp critical
             {if(!found){found=1;memcpy(solution,block,16);}}
           }
           block[idx[3]]^=(unsigned char)(w<<shift[3]);
         }
         block[idx[2]]^=(unsigned char)(z<<shift[2]);
       }
       block[idx[1]]^=(unsigned char)(y<<shift[1]);
     }
     block[idx[0]]^=(unsigned char)(x<<shift[0]);
   }
 }
 printf("mode=%s quartets=%d assignments=%llu matches=%d elapsed_sec=%.3f\n",synthetic?"synthetic":"original",end-begin,count,found,now()-t0);
 if(found){printf("solution=");for(int i=0;i<16;i++)printf("%02X",solution[i]);puts("");}
 return synthetic?(found&&!memcmp(solution,known,16)?0:2):(found?2:0);
}
