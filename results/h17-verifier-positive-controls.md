# REC8/1 original-verifier acceptance-path controls (Agent 12)

**Date:** 18 October 2026. **Status:** Test-only positive and negative controls pass analytically and in a separate local extraction. No original K04 or K08 value has been found.

## Purpose

With two source components missing, the unchanged `resources/verify.py` must legitimately return `combined: INCOMPLETE` for the six-component candidate. This makes it useful to prove separately that the same checker can produce `accepted: true` for a *fully specified, internally consistent synthetic case*, while retaining the real original commitments untouched on disk.

This test validates the verifier's interpretation of the complete-envelope format. It does not imply that invented dummy components satisfy the actual H-17 archive commitments.

## Original and synthetic checks

The read-only [`test_h17_verifier_controls.py`](test_h17_verifier_controls.py) imports the **unmodified** original `resources/verify.py` and calls its `evaluate()` function with in-memory inventories only:

1. Current original baseline `results/h17-candidate.json`: exactly six individual `PASS`, K04 and K08 `MISSING`, combined `INCOMPLETE`, `accepted: false`.
2. Synthetic positive: preserve the six source-validated components, fill K04 with bytes `00..0F` and K08 with bytes `10..1F` **solely as test placeholders**, calculate their two test-only slot SHA-256 commitments, and calculate the test-only combined SHA-256 from the unmodified `CEG-ARCHIVE-RECOVERY/v1\n` prefix and all eight uppercase hex values plus LF. `evaluate()` must report eight `PASS`, combined `PASS`, `accepted: true`.
3. Synthetic negative: change one hexadecimal character of the dummy K04 value, keeping the synthetic commitments unchanged. `evaluate()` must report K04 `NO_MATCH`, combined `NO_MATCH`, `accepted: false`.
4. Original target rejection: evaluate the unmodified original targets with those same fake placeholders. K04 and K08 must each be `NO_MATCH`, and `accepted` must be false.

All tests are deterministic Python 3 standard-library operations. The source ZIP, `resources/acceptance.json`, `resources/verify.py`, and six-slot shared candidate are read-only throughout.

## Limitation and status

The synthetic positive control proves the mechanical eight-slot acceptance path can work. It provides **zero cryptographic evidence** for the actual H-17 K04/K08 secrets, and it never bypasses the original checker. Current real result is still **6 PASS, 2 MISSING, combined INCOMPLETE, accepted false**. See [main recovery synthesis](README.md).
