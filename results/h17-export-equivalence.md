# H-17 export equivalence and provenance check (Agent 3)

**Checked:** 17 October 2026. **Question:** Could the repository's evidence copy differ from the separate surviving ZIP supplied with the current invocation and explain the two acceptance failures?

## Method

I read the supplied ZIP `c-energy-group-documents2026.zip` locally and computed, for each of its **43 regular files**, the standard Git blob object ID:

```python
hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
```

I compared all 43 ZIP-relative paths and object IDs with the `resources/` blobs returned by the repository's recursive `main` Git tree. **Every path and blob hash matched exactly**, including `acceptance.json`, `verify.py`, the printer spool and all desk notes. Thus the two available copies of the archive export were byte-for-byte identical at the time of this check. This result checks copy equivalence only; it does **not** authenticate the original reconstructed printer payload or prove that the trimmed export is complete.

## Reproducible fingerprints

- ZIP SHA-256: `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`.
- Canonical file manifest SHA-256: `728d3dfa8c8e6bdcc3f5010cb0cc217a57cd430d705645659d2794bc4ab97343`. To reproduce, sort paths lexicographically; for each file append `<relative/path> <lowercase SHA256(file)>\n` as UTF-8; hash the concatenation.
- Printer spool SHA-256: `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`.
- Keeper notes SHA-256: `13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb`.
- Routing SHA-256: `f8fcbca73d23bf1066edb88c088f89cd24cf22e7c78a4a412166254a4764d8a5`.
- Acceptance SHA-256: `681739241b757b471acca4c0fef9d9d97e9493883887736d5db3b92bfb0c137f`.
- Verifier SHA-256: `01cedbfa08a28b388f8ab09b96c9c562a920d8ae9a7cc582ba3c79d138681cd0`.

## Local acceptance replay

I wrote the six published passing component values into a new local `candidate.json` and ran the unchanged ZIP `verify.py --candidate candidate.json --json`. Output was six `PASS` states (K01, K02, K03, K05, K06, K07), K04/K08 `MISSING`, combined `INCOMPLETE`, `accepted: false`. This independently checks the stored candidate against the supplied copy of acceptance commitments; the more detailed original-record derivation is in `results/replay_h17.py`.

I separately searched every contiguous 16-byte window formed from hexadecimal runs in the supplied `evidence/` text files, testing raw bytes and the ESC-N XOR mask (including a reversed-payload diagnostic): 405 candidate hashes, no K04 match. A second diagnostic tested **every contiguous 16-byte raw-byte window** of the surviving `evidence/` files as-is and XORed with the ESC-N mask: 201,830 SHA-256 checks (100,915 byte windows × 2), no K04 match. These bounded diagnostics cannot rule out an unrecovered original coupon, an unrecorded transformation, or arbitrary corruption.

## Implications

A difference between the uploaded ZIP and shared `resources/` cannot explain the K04 mismatch or the absent authenticated exact K08 caption. Focus any future effort on additional **original, integrity-proven source material**, an evidenced reconstruction error, or a specifically justified recovery mechanism. Keep K04/K08 null until their exact bytes pass the unchanged verifier.
