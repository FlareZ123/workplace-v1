// H-17 direct K04 cracking attempt: UTC-second seeded CPython MT19937.
// Checks one complete, authenticated ordinary printer payload as a 128-bit
// producer discriminator. Target ESC-N row129, mask and REC8 hashes are withheld.
// Source: evidence/print/spool-reconstruction.log, sha256
// 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083
//
// g++ -O3 -std=c++17 k04_utc_seed_direct.cpp -o k04_utc_seed_direct
// k04_utc_seed_direct
// k04_utc_seed_direct 1790208000 1791244800 4096
//
// Historical premise (UNPROVEN): the common printer MT output stream was
// initialized from a UTC Unix-second integer between commissioning and
// 2026-10-05 and reaches intact row3 within 4096 generated outputs.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
class PythonMT {
  static constexpr uint32_t A=0x9908B0DFu, HI=0x80000000u, LO=0x7FFFFFFFu;
  std::array<uint32_t,624> mt{};
  int index=624;
  static uint32_t twist(uint32_t a,uint32_t b){
    uint32_t z=(a&HI)|(b&LO);
    return (z>>1)^((z&1)?A:0);
  }
public:
  void seed(uint32_t key){
    mt[0]=19650218u;
    for(int i=1;i<624;i++)
      mt[i]=1812433253u*(mt[i-1]^(mt[i-1]>>30))+uint32_t(i);
    int i=1;
    for(int k=624;k>0;k--){
      mt[i]=(mt[i]^((mt[i-1]^(mt[i-1]>>30))*1664525u))+key;
      if(++i>=624){mt[0]=mt[623];i=1;}
    }
    for(int k=623;k>0;k--){
      mt[i]=(mt[i]^((mt[i-1]^(mt[i-1]>>30))*1566083941u))-uint32_t(i);
      if(++i>=624){mt[0]=mt[623];i=1;}
    }
    mt[0]=HI; index=624;
  }
  uint32_t next(){
    if(index>=624){
      int k=0;
      for(;k<227;k++) mt[k]=mt[k+397]^twist(mt[k],mt[k+1]);
      for(;k<623;k++) mt[k]=mt[k-227]^twist(mt[k],mt[k+1]);
      mt[623]=mt[396]^twist(mt[623],mt[0]); index=0;
    }
    uint32_t y=mt[index++];
    y^=y>>11;
    y^=(y<<7)&0x9D2C5680u;
    y^=(y<<15)&0xEFC60000u;
    y^=y>>18;
    return y;
  }
};
int main(int argc,char**argv){
  constexpr uint32_t original[4]={0x8343FF24u,0xB2674837u,0x2BBBFAF2u,0xAF2AF730u};
  if(argc==1){
    // Independently established Python 3 random.Random(integer) positives.
    const uint32_t seeds[3]={0,20261003u,1791000000u};
    const uint32_t expected[3][4]={
      {0xD82C07CDu,0x629F6FBEu,0xC2094CACu,0xE3E70682u},
      {0x0735C9C9u,0x9C1BBF9Cu,0xEBF87ED6u,0x01434BE3u},
      {0x245A4B4Au,0x70C30A84u,0xD42F84BDu,0x0429E7DDu}
    };
    for(int i=0;i<3;i++){
      PythonMT rng;rng.seed(seeds[i]);
      for(int j=0;j<4;j++)if(rng.next()!=expected[i][j]){
        std::fprintf(stderr,"CPython control mismatch seed %u word %d\n",seeds[i],j);
        return 1;
      }
    }
    std::puts("CPython MT integer seed controls PASS: 3 seeds x 4 words");
    // Nonzero-offset synthetic 128-bit source block must be found exactly.
    PythonMT fixture;fixture.seed(1791000000u);
    for(int i=0;i<1473;i++)fixture.next();
    uint32_t truth[4]={fixture.next(),fixture.next(),fixture.next(),fixture.next()};
    PythonMT replay;replay.seed(1791000000u);
    uint32_t a=0,b=0,c=0,d=0;
    int synthetic_hits=0;
    for(int pos=0;pos<4099;pos++){
      a=b;b=c;c=d;d=replay.next();
      if(pos>=3 && a==truth[0] && b==truth[1] &&
         c==truth[2] && d==truth[3]){
        if(pos-3!=1473)return 1;
        synthetic_hits++;
      }
    }
    if(synthetic_hits!=1)return 1;
    std::puts("Synthetic full 128-bit offset=1473 recovery: PASS");
    return 0;
  }
  if(argc!=4){
    std::fprintf(stderr,"usage: scanner FIRST_UTC_SECOND EXCLUSIVE_LAST_UTC_SECOND MAX_FIRST_WORD_OFFSET\n");
    return 2;
  }
  uint32_t start=uint32_t(std::strtoull(argv[1],nullptr,10));
  uint32_t stop=uint32_t(std::strtoull(argv[2],nullptr,10));
  uint32_t maxoffset=uint32_t(std::strtoull(argv[3],nullptr,10));
  uint64_t partial=0,complete=0;
  for(uint32_t seed=start;seed<stop;seed++){
    PythonMT rng;rng.seed(seed);
    uint32_t a=0,b=0,c=0,d=0;
    for(uint32_t pos=0;pos<maxoffset+3;pos++){
      a=b;b=c;c=d;d=rng.next();
      if(pos<3||a!=original[0])continue;
      partial++;
      if(b==original[1]&&c==original[2]&&d==original[3]){
        complete++;
        std::printf("COMPLETE_SRC_MATCH seed=%u offset=%u\n",seed,pos-3);
      }
    }
  }
  std::printf("seeds=%u offsets=%u first_word_hits=%llu full_128bit_hits=%llu\n",
    stop-start,maxoffset,(unsigned long long)partial,(unsigned long long)complete);
  return 0;
}
