# K04: two-job affine retry producer fails original held-out control

**Agent 6, 20 October 2026, approximately 04:05 UTC.** Original-source hypothesis test. The source-selected K04 attempt-2 ACK, route mask, K04 digest and K08 acceptance materials were excluded from this calculation. No original evidence or commitments were modified.

## Previously unused paired job transition witness

The original `resources/evidence/print/spool-reconstruction.log` (SHA-256 `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`) contains two incident-day reused job IDs, each observed at different times and classes:

| Original event | Incident UTC time | Payload |
| --- | --- | --- |
| 0420 STORES, ACK attempt 1 | 17:00 | `31C9714DD36DB2677BB9006670A9DFFD` |
| 0420 RECOVER, ACK attempt 2 | 18:25 | `432475F72A62DB39F3D5693E2C937FA4` |
| 0417 LABEL, ACK attempt 1 | 16:45 | `E1E60D5F6B6DD2225FA6D5A2A63AD932` |
| 0417 RECOVER, REQUESTED attempt 1 | 18:01 | `CD3E4F216ADB2FB180DA2AA90B33F7A4` |
| **Withheld control**, 0417 RECOVER REQUESTED attempt 3 | 18:03 | `44D53DFC29D7943A95D89371DA58EC64` |

The separate 0417 RECOVER attempt-2 ACK is the *disputed target*, deliberately not consumed by the test. The two first transitions hypothetically act as consecutive generator steps, with one shared device-independent 128-bit affine law `Y = A X + B (mod 2^128)`. Source records do **not** attest such a law, uniform retries, or shared seeding, so the test is a falsifier of this exact producer conjecture only.

## Source-only solving and withheld intact prediction

The two source transitions require `A(X0420-X0417)=(Y0420-Y0417) (mod 2^128)`. Solve this linear congruence exactly, using the power-of-two divisibility condition and modular inverse, with 16-byte payload interpreted as either endian order.

- **Little endian:** the input difference has 2-adic valuation 4; the output difference has valuation 1. Since the right side is not divisible by 16, the shared affine law is inconsistent even before withheld testing.
- **Big endian:** input difference is odd, so exactly one pair `(A,B)` exists. Applying two further transitions to the 0417 REQUESTED attempt-1 control predicts `B15BC124363B4D303FB2B089E841A7A4` as 0417 REQUESTED attempt-3. The actual surviving source value is `44D53DFC29D7943A95D89371DA58EC64`, rejecting that law.

Reproducer: [source-pinned standalone SFT](../agents/agent6/k04_reused_job_affine_heldout_sft.py), with 100 actual synthetic shared-affine positive controls and one impossible modular-congruence control. A separate bounded PRNG proposal that used each earlier payload as one of four Python MT seeds and scanned the first 32,769 fourword offsets in each of two source pairs also returned zero original matches: [job-seeded source SFT](../agents/agent6/k04_reused_job_seed_sft.py). Neither model is asserted as the historical generator.

## Recovery implication

There is **zero authenticated K04 selected-coupon bit gain**, zero recovered K08 final-caption words, and no eight-slot accepted REC8 key. These source-only controls close the *particular* shared affine and payload-seeded retry models. They do not rule out a stateful physical printer with extra unobserved draws, a different job-local generator, separate clocks, or damaged retained payloads. Repeating arbitrary LCG variants would be unanchored; the next consequential evidence is a contemporaneous independently witnessed 0417 coupon, documented producer recipe with intact held-out predictions, or a verbatim selected keeper caption. Original six accepted components and all REC8 commitments remain unchanged.
