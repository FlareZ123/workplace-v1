// H-17 read-only std::mt19937 time-seed model gate; independent of REC8 hashes.
// Original spool sha256: 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083
// Original intact row PS-261003-0300 first two 32-bit words: FBBBC543 56483F58.
#include <cstdint>
#include <cstdio>
#include <random>
#include <chrono>
int main() {
  const uint32_t low=1790208000u, high=1791072000u; // Sep 24 to Oct 4 UTC, exclusive
  const uint32_t be1=0xFBBBC543u, be2=0x56483F58u;
  const uint32_t le1=0x43C5BBFBu, le2=0x583F4856u;
  std::mt19937 expected(20261003u), replay(20261003u);
  for(unsigned p=0;p<123;++p) expected();
  const auto want1=expected(),want2=expected();
  for(unsigned p=0;p<123;++p) replay();
  if(replay()!=want1||replay()!=want2) return 2;
  uint64_t singles=0, pairs=0;
  const auto clock_start=std::chrono::steady_clock::now();
  for(uint32_t seed=low;seed<high;++seed){
    std::mt19937 mt(seed);
    uint32_t prev=mt();
    for(uint32_t offset=0;offset<4096;++offset){
      const uint32_t next=mt();
      if(prev==be1||prev==le1){
        ++singles;
        if((prev==be1&&next==be2)||(prev==le1&&next==le2)) {
          ++pairs;
          std::printf("PAIR seed=%u offset=%u endian=%s\n",seed,offset,prev==be1?"BE":"LE");
        }else{
          std::printf("single seed=%u offset=%u endian=%s next=%08X\n",seed,offset,prev==be1?"BE":"LE",next);
        }
      }
      prev=next;
    }
  }
  const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-clock_start).count();
  std::printf("control=PASS seeds=%u pair_start_offsets=4096 singles=%llu pairs=%llu elapsed_s=%.3f\n",high-low,(unsigned long long)singles,(unsigned long long)pairs,elapsed);
  return 0;
}
