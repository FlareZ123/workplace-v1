# K04: standard MT19937 one-word scalar seeding excluded in the joined first-cycle spool model

**Agent 21, 20 October 2026 ~13:39 UTC.** Source-only computational exclusion with an exact original-source necessary condition. **Actual selected-coupon bits recovered: 0/128; K08 exact final words: 0.** This is a restricted historical-producer hypothesis, not a recovered key.

## Original source and conditioned alignment

The [Agent26 independent MT inversion](../agents/agent26/k04_seven_residue_gate.py), established from twelve completely intact original spool rows (3,10,33,34,41,56,63,64,86,94,116,125), reconstructs five *consecutive initialized pre-twist MT state words* within a common-output first-cycle model. Original spool bytes SHA-256: `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. The disputed exact-job row129, all mask bytes and commitments are withheld from the inversion. The absolute first-cycle state phase `p` remains unknown in `396..621`, and the five words occupy indices `p-2..p+2`:

`B30BF870 6CE0E225 F4E8FCB2 C517EB25 7D3AAF35`.

These full state words and their allowed phase are **algebraic results under the existing joined common-MT stream placement**, not evidence that the original physical producer used a standard scalar seed. The source-specific reason to test this class is that its initializer is a distinctive necessary fingerprint which can be disproved from a few adjacent initialized-state words without knowing a seed or consulting the K04 digest.

## New conditional falsification

The original MT19937 `init_genrand` single-32-bit-seed initializer used by the standard reference algorithm and conventional scalar-seeded `std::mt19937` satisfies, for `i=1..623`:

`S[i] = (1812433253 * (S[i-1] XOR (S[i-1] >> 30)) + i) mod 2**32`.

For each adjacent observed pair `(a,b)`, the **required absolute initialization index** is therefore fixed as `(b - 1812433253*(a XOR (a >> 30))) mod 2**32`. Applied to the five original-source-inverted values, the four required indices are:

`2115296043, 1211007102, 3776610384, 2011796279`.

Their index values disagree with *every* consecutive index quadruple `p-1,p,p+1,p+2` for `p=396..621`. In fact, none is within `1..623`. Thus **zero first-cycle phases** of the existing conditional source join can come from a standard one-word scalar-seeded MT19937 state initialized by `init_genrand`. No enumeration of seed numbers, alternative coupon payloads or digest guesses is involved.

**Control:** a fresh independent local stdlib SFT used 16 known scalar-seeded synthetic (`seed`, `p`) cases for seeds `0`, `5489`, `123456789`, `0xF00DBEEF` and phases `396,445,562,621`; complete MT outputs were generated and inverted using the original twelve-row placement. All 16 reconstructed initialized-state windows exactly matched synthetic seed initialization, and all 16 derived index quartets matched `[p-1,p,p+1,p+2]`. The source run reproduced the five exact original words above, the four impossible indices, zero compatible phases, and no target read. Reusable repository [source-pinned test](../agents/agent21/k04_std_mt_scalar_sft.py) reuses Agent26's already published original-state inference; the independent local standalone SFT also exists in the invoking environment.

## What this does and does not crack

This is a **new producer-family exclusion** for a particular previously supported printer-state alignment, distinct from CPython `init_by_array` seed-length residue exclusions. It does not exclude all common-MT printer implementations, CPython arbitrary-array initialization, NumPy SeedSequence, alternate first-output epochs, reseeding/restarts, or a chronology outside the joined source model. Nor does it explain the actual selected ESC-N coupon, yield a byte of the authentic 16-byte print field, or provide a final caption. Further blind seed-family tests would have no justified target-information gain without historical producer evidence; do not turn this model exclusion into a new long seed-computation agenda.

The original source and REC8 acceptance records are unchanged; six known slots PASS and K04/K08 remain missing, combined INCOMPLETE, accepted false.
