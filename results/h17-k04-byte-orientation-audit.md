# K04 byte orientation audit (Agent 5)

The printer log explicitly marks retained payload integrity unverified. I tested a bounded transformation class based on possible consistent bit/byte orientation errors, using the original K04 commitment unchanged.

Across all 133 complete print-spool payloads, each 16-byte value was tested after 64 uniform transformations: 8 within-byte rotations, optional within-byte bit reversal, optional bit complement, optional reversal of the 16-byte stream. Every resulting candidate was XORed with the recorded fixed K04 mask then SHA-256 compared with the acceptance target. The test ran 8,512 transformations, yielding 8,512 distinct candidates and zero matches.

Inputs are the unchanged original export files. The log SHA-256 is 7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083. The selected job PS-261003-0417, ACK attempt 2 remains a mismatch. The script verifies its original bytes and checks a synthetic in-memory positive control before enumerating actual targets.

Reproducer: [read-only checker](check_h17_printer_byte_orientation.py), which uses Python's standard library and the existing resources directory. It accepts an extracted local ZIP directory with --root.

This finite negative result excludes only its specified interpretation of existing log values. It cannot authenticate altered bytes or supply missing originals. K04 and K08 remain unresolved; unchanged REC8 verifier result is six PASS, two MISSING, combined INCOMPLETE, accepted false.
