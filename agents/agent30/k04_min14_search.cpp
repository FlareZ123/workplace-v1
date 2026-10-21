// Exact conditional search: all minimum-Hamming Q compatible with a shared
// arbitrary 128-bit retry permutation. Historical shared permutation is unproven.
// Build: g++ -O3 -std=c++20 -pthread k04_min14_search.cpp -lcrypto -o k04_min14_search
#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
#include <openssl/sha.h>
using namespace std;
using U128=unsigned __int128;
constexpr int N=16,K=5,T=14;
constexpr int cap[N]={2,5,4,3,6,2,4,6,5,1,5,4,2,8,1,6};
constexpr int coeff[N][K]={{0,0,1,0,-1},{1,-1,-1,0,0},{-1,0,2,0,0},{1,0,-1,-1,0},{0,0,0,-1,0},{0,-1,1,1,0},{0,1,0,-2,0},{1,0,0,0,-2},{0,-1,0,0,1},{0,0,1,0,-1},{0,0,0,-1,1},{1,0,0,0,-1},{0,-1,0,0,0},{0,0,1,0,0},{0,0,0,-1,0}};
constexpr int target[K]={6,-3,2,-3,-11};
constexpr char Ahex[]="CD3E4F216ADB2FB180DA2AA90B33F7A4";
constexpr char Bhex[]="31C9714DD36DB2677BB9006670A9DFFD";
constexpr char Chex[]="44D53DFC29D7943A95D89371DA58EC64";
constexpr char Dhex[]="432475F72A62DB39F3D5693E2C937FA4";
constexpr char Shex[]="A9A9DC5731A5E2AE879C47215C2559D5";
constexpr char maskhex[]="8556C8CB6140A7F9A5123AC7571BEE1C";
constexpr char commitment[]="930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0";
int d(char x){if(x>='0'&&x<='9')return x-'0';if(x>='A'&&x<='F')return x-'A'+10;return x-'a'+10;}
array<unsigned char,16> hex16(const char* x){array<unsigned char,16>a{};for(int i=0;i<16;i++)a[i]=(d(x[2*i])<<4)|d(x[2*i+1]);return a;}
array<unsigned char,32> hex32(const char* x){array<unsigned char,32>a{};for(int i=0;i<32;i++)a[i]=(d(x[2*i])<<4)|d(x[2*i+1]);return a;}
U128 as128(const array<unsigned char,16>& b){U128 v=0;for(auto c:b)v=(v<<8)|c;return v;}
struct Pattern{array<unsigned char,N> f;unsigned long long count;};
vector<Pattern> patterns;
int remLo[N+1][K]{},remHi[N+1][K]{},remCap[N+1]{};
unsigned long long choose[N][9]{};
void construct(int i,int left,array<int,K> remaining,array<unsigned char,N>& f,unsigned long long count){
 if(i==N){if(left==0 && all_of(remaining.begin(),remaining.end(),[](int x){return x==0;}))patterns.push_back({f,count});return;}
 if(left<0||left>remCap[i])return;
 for(int j=0;j<K;j++)if(remaining[j]<remLo[i][j]||remaining[j]>remHi[i][j])return;
 for(int z=0;z<=min(cap[i],left);z++){
  auto r=remaining;
  for(int j=0;j<K;j++)r[j]-=z*coeff[i][j];
  f[i]=z;
  construct(i+1,left-z,r,f,count*choose[i][z]);
 }
}
array<vector<U128>,N> alternatives; // filled per pattern in each thread, not globally
array<vector<int>,N> idx;
atomic<size_t> nextPattern{0};
atomic<unsigned long long> checked{0};
atomic<bool> found{false};
mutex printGuard;
U128 selected,routeMask;
array<unsigned char,32> trueDigest;
void enumerate_mask(const array<vector<U128>,N>& choices,int gi,U128 bitflips,unsigned long long& local){
 if(found.load(memory_order_relaxed))return;
 if(gi==N){
  U128 q=selected^bitflips^routeMask;
  unsigned char payload[16],hash[SHA256_DIGEST_LENGTH];
  for(int i=15;i>=0;i--){payload[i]=static_cast<unsigned char>(q&255);q>>=8;}
  SHA256(payload,16,hash);
  ++local;
  if(memcmp(hash,trueDigest.data(),32)==0){
   lock_guard<mutex> lock(printGuard);
   found=true;
   printf("FOUND K04 COMPONENT=");for(auto x:payload)printf("%02X",x);puts("");
   fflush(stdout);
  }
  return;
 }
 for(auto m:choices[gi])enumerate_mask(choices,gi+1,bitflips|m,local);
}
void worker(){
 unsigned long long local=0;
 while(!found){
  size_t pi=nextPattern.fetch_add(1);
  if(pi>=patterns.size())break;
  auto& p=patterns[pi];
  array<vector<U128>,N> choices;
  for(int g=0;g<N;g++){
   const int total=idx[g].size(),num=p.f[g];
   for(int subset=0;subset<(1<<total);subset++){
    if(__builtin_popcount((unsigned)subset)!=num)continue;
    U128 mask=0;
    for(int i=0;i<total;i++)if(subset&(1<<i))mask|=(U128(1)<<(127-idx[g][i]));
    choices[g].push_back(mask);
   }
  }
  enumerate_mask(choices,0,0,local);
  if(local>=1'000'000){checked.fetch_add(local);local=0;}
 }
 checked.fetch_add(local);
}
int main(int argc,char**argv){
 auto A=hex16(Ahex),B=hex16(Bhex),C=hex16(Chex),D=hex16(Dhex),S=hex16(Shex);
 selected=as128(S);routeMask=as128(hex16(maskhex));trueDigest=hex32(commitment);
 for(int i=0;i<128;i++){
  int byte=i/8,bit=7-i%8;
  int group=(((A[byte]>>bit)&1)<<3)|(((B[byte]>>bit)&1)<<2)|(((C[byte]>>bit)&1)<<1)|((D[byte]>>bit)&1);
  bool selectedOne=(S[byte]>>bit)&1;
  // In every min14 model, even groups flip S-zero to one, odd groups flip S-one to zero.
  if(selectedOne==(group%2==1))idx[group].push_back(i);
 }
 for(int g=0;g<N;g++){
  if(idx[g].size()!=static_cast<size_t>(cap[g])){cerr<<"source mismatch group "<<g<<"\n";return 2;}
  choose[g][0]=1;
  for(int j=1;j<=cap[g];j++)choose[g][j]=choose[g][j-1]*(cap[g]-j+1)/j;
 }
 for(int i=N-1;i>=0;i--){
  remCap[i]=remCap[i+1]+cap[i];
  for(int j=0;j<K;j++){
   int v=cap[i]*coeff[i][j];
   remLo[i][j]=remLo[i+1][j]+min(0,v);
   remHi[i][j]=remHi[i+1][j]+max(0,v);
  }
 }
 array<unsigned char,N> f{};array<int,K> remaining{};copy(begin(target),end(target),remaining.begin());
 construct(0,T,remaining,f,1);
 unsigned long long total=0;for(auto& p:patterns)total+=p.count;
 cout<<"Patterns="<<patterns.size()<<" exact conditional Q="<<total<<"\n"<<flush;
 if(total!=1665398756ULL){cerr<<"count mismatch\n";return 3;}
 // Optional synthetic positive control on a subset of the candidate enumeration.
 // Final production compares against the unmodified original K04 hash.
 int workers=argc>1?stoi(argv[1]):4;
 vector<thread> threads;for(int k=0;k<workers;k++)threads.emplace_back(worker);
 for(auto&th:threads)th.join();
 cout<<"SHA256 checks="<<checked<<" found="<<found<<"\n";
 return found?0:1;
}
