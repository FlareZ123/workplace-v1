# K04: source-grounded future-state XOR fingerprint tested against all original AX checkpoint halfwords

**Agent 9, 20 October 2026 ~04:08 UTC.** A **new halfword carrier class** for the previously established K04 target-facing future-state algebra; no original coupon bits recovered. Original H-17 source records, route mask and acceptance commitments unchanged. This is a bounded original-source negative result, not an authenticated printer producer model.

## Exact source anchor, mechanism, and pre-hash prediction

The original `resources/evidence/transfers/transfer-audit.jsonl` has SHA256 `32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf`: **64 CHUNK checkpoints** spanning AX-7778/7781/7782/7783, each a 16-bit hex `checkpoint` source field. The original `resources/evidence/print/spool-reconstruction.log` SHA256 is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`. Selected printer row129 is *not used*. Some AX source fields are rejected, aborted or dry-run by final transfer acceptance rules, but all 64 are generously retained as hypothetical independent donor carriers. No actual original record states that AX stores the printer's future state positions.

**Calibrated carrier interpretation:** the earlier original-source AX-7778↔intact printer rows34/64 bridge successfully predicts four **tempered output upper-16-bit** checkpoints in the byte-swapped view (original AX-7778 ordered positions11..14). Our SFT asserts all four as an independent original positive control. It therefore tests the **upper** output halfword, not an arbitrary lower-halfword reinterpretation selected after seeing a coincidence.

**Future target-facing predictions:** Agent29's *source-only, conditional index955* original-print GF(2) reduction established four partial or full untempered future-state XOR pairs, independent of the disputed selected row or hash. MT19937 tempering is GF(2)-linear, allowing a finite upper-16 XOR signature set with up to two unknown fullword bits. A genuine historical AX donor pair mapped independently to these positions must pass its exact signature:

| Conditional future indices | Original-source untempered XOR fixed mask / constant | Predicted tempered upper16 XOR set |
| --- | --- | --- |
| X1412 ↔ X1866 | `FFFFFFFF / BD2761F8` | `4692` |
| X1185 ↔ X1412 | `BFFFFFFF / 359EC0C7` | `9376`, `D77E` |
| X1185 ↔ X1866 | `BFFFFFFF / 88B9A13F` | `91EC`, `D5E4` |
| X1411 ↔ X1865 | `9FFFFFFF / 0CDE27B9` | `809D`, `A099`, `C495`, `E491` |

Example: `temper(BD2761F8)=4692D6B0`, so a true indexed pair at1412/1866 predicts checkpoint XOR `4692` in the calibrated upper-halfword view. Importantly, the partial 31/30-bit constraints were **not** converted naively to a fixed upper16 mask; we enumerated the one or two unknown *untempered* bits before applying the linear temper transform.

## Executed test and result

The self-contained [read-only SFT](../agents/agent9/k04_ax_future_donor_halfword_sft.py) asserts original spool/transfer digests, parses 64 checkpoint fields, verifies the four AX-7778→printer positive controls, derives all allowed upper16 pair XOR signatures, and compares each of the **2,016 unordered pairs** under each of **two globally consistent byte orientations**. Neither original selected row129 bytes nor K04 mask, digest, K08 phrase/nonce, or verifier enter the computation.

A locally executed equivalent self-contained program on the original 43-member source produced:

```
ORIGINAL_AX7778_FOUR_HIGH16_POSITIVE_CONTROL PASS
X1412_X1866 ... upper16 ['4692']                     hits=0
X1185_X1412 ... upper16 ['9376','D77E']              hits=0
X1185_X1866 ... upper16 ['91EC','D5E4']              hits=0
X1411_X1865 ... upper16 ['809D','A099','C495','E491'] hits=0
```

All four source-predicted upper16 future-donor pair families have **zero original AX matches** in both orientations. The standalone repo SFT has the same core algorithms and hashes. An attempted one-time manual Actions dispatch of `.github/workflows/h17-k04-ax-future-halfword.yml` returned an explicit safety block; **no CI execution is claimed**. The local executed equivalent passes source positive controls.

**Important non-match:** an ad hoc **lower** 16-bit projection of the full32 1412↔1866 relation yields a superficially interesting byte-swapped XOR `D6B0` between AX-7781 seq5 attempt2 `CC5B` (dry-run transfer) and AX-7783 seq5 attempt1 `7C8D` (aborted transfer). That is **outside** the original AX-7778 calibrated *upper16* carrier interpretation and lacks any original future-state index mapping. It is a useful negative guard against promoting a coincidental lower-halfword value as a genuine donor or newly recovered coupon bytes.

## Provenance and limits

Earlier [Agent29 full32 TRP2/RC17 donor-pair check](h17-k04-forward-donor-leverage-and-source-xor.md) covered 100 independent 4-byte fields, **not these 64 AX two-byte checkpoint fields**. Earlier [Agent9 AX bridge study](../agents/agent9/memory.md) targeted predecessor rows and source-inferred triples, not the published *future* 1412/1866 XOR equations. This is a distinct, target-oriented source carrier class and an original-data positive-controlled negative result.

The verified negative excludes only *direct high16 AX future-donor pairs* in this conditional p955 chronology with a consistent 16bit orientation. It does not exclude a transformed carrier, unseen original future records, a different historical stream alignment, or an authenticated coupon. Crucially the p955 print-payload-consistent layout itself conflicts with stronger CLASS/DEST sampler assumptions and is **not historically proven**. A genuinely indexed future halfword without its paired checkpoint might reduce theoretical target entropy but cannot be located here. **Actual K04 coupon bits recovered 0/128; authenticated K08 final words 0; REC8 still six PASS, two missing, combined INCOMPLETE, accepted false.**

**Decision:** do not widen arbitrary AX halfword permutations or claim that a cross-transfer numerical coincidence authenticates a printer state. Reopen when a new source explicitly indexes an original future output, cassette buffer/mask or recorded final keeper caption.

## Further source-anchored lane discriminator (04:15 UTC)

A later executed self-contained original-export program tested whether the **lower16 channel** behind the apparent `D6B0` coincidence has independent support anywhere in the whole original AX/retained-printer corpus. This is more discriminating than assuming that AX-7781/7783 used a distinct low-halfword format because the published earlier AX-7778 held-out witnesses used high16.

- Enumerate all **132 intact other printer rows** in strictly increasing order, all ordered cross-row pairs, and all four possible aligned three-word starting offsets (first/middle word offsets 0 or 1). For each paired three-word MT inversion, use the exact low31 original predecessor fingerprint and **both** possible predecessor MSBs, giving 276,672 exact three-word predictions per lane.
- Match every predicted upper16 triple or lower16 triple against all 14 sliding triple windows of each of the four original AX groups in both globally consistent native and swapped byte views. This uses original source fields only; selected row129 is withheld, no digest inspected.
- **Upper16 returns exactly 3 triple hits,** all preexisting original AX-7778 positive bridges: rows33/63 at offsets0/1 against AX7778 swapped position5, plus rows34/64 at offsets0/0 (AX7778 swapped position11) and1/1 (position12). **Lower16 returns exactly 0 triple hits**.

The source-only test is now integrated in [the SFT](../agents/agent9/k04_ax_future_donor_halfword_sft.py) after the future-pair check, with these expected original triple witnesses asserted. The executed local equivalent enumerated both lanes and reproduced 3 upper/0 lower matches. Original transfer/spool SHA256 pinned as above; all 64 checkpoint fields included as source prospects.

This is a bounded **falsification of the simple uniform lower16 direct-copy producer interpretation on three consecutive inferred original AX words**. It strengthens the decision to **reject** the single `D6B0` lower-halfword XOR near-hit as evidence for selected K04 output. It does not prove another historical producer or serialization impossible and does not add any authentic K04 bits.
