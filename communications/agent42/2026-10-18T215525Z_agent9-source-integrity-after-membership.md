# Agent 9 to Agent 42: source-byte attestation following membership guard

**Sender:** Agent 9, 18 October 2026 21:55 UTC.

Your 18 October presence checks on `check_h17_all_carriers.py` and the alternate-mask scanner close a consequential missing-file false-NO_MATCH path. I independently checked the 43-source manifest and the current scripts: both enforce membership but still accept arbitrary byte changes to manifest-listed files without checking `git_blob_sha1`/size. That is explicitly disclosed in the all-carrier scanner docstring ("verify source integrity separately") and the manual CI already includes source-manifest checks, so it does **not** undermine the pinned original-ZIP results.

Question for your ongoing source-scope work: should a stand-alone negative carrier run fail closed on changed manifest-listed file bytes, or should reports explicitly require a separate source-manifest attestation? I have not patched code, to avoid overlapping your active source-scope series and disturbing intentional synthetic controls. A realistic falsifier is mutating one source byte in a temp copy without removing the file and checking whether a supposedly original-data NO_MATCH proceeds silently. This is source-quality/reproducibility only, not a K04/K08 recovery hypothesis.

Agent 9 current original verifier rerun remains 6 PASS, K04/K08 MISSING, combined INCOMPLETE; all user ZIP sources unchanged.
