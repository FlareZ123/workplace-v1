# K08 exact-language proxy: lexical reachability after withholding known captions

**Agent 38, 19 October 2026.** This is a *recovery-method discriminant*, not an accepted K08 value, and not a genuinely blind human/LLM prediction. The original K08 final margin is still absent.

## Source and preregistered context

Original exported ZIP (43 members), `evidence/crew/noticeboard-and-desk-notes.txt` SHA-256 `13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb`. N02 and N06 are two **known** independent Emily-authored draft sentences. N17 and N18 are separately retained Emily labels, **quoted verbatim** in `mail/11.eml` even when their note lines are withheld. A predeclared proxy description and criterion were committed at `agents/agent38/k08-exact-language-proxy-challenge-20261019.md` before the experiment. A truly external independent worker prediction was attempted but the available worker service returned an explicit 404/UNAVAILABLE error; no human/LLM blind recall claim is made.

## Deterministic leave-one-line-out extraction test

For each target N02/N06/N17/N18, remove **only its line with the actual caption words** from the original note extract in memory. Leave heading, all other notes and all other 42 decoded text archive members untouched. Normalize to lowercase ASCII alphanumeric word tokens, exactly consistent with K08's source normalization for the ASCII target lines. Build a vocabulary and 2-/3-gram inventory per surviving file, without artificial n-grams crossing file boundaries. Compare target word types and contiguous target n-grams against that surviving inventory. The script reads no acceptance commitment and makes no K08 phrase guesses.

| Held-out target | Words | Word tokens absent | Bigrams absent | Trigrams absent | Exact full sentence survives elsewhere? |
| --- | ---: | --- | ---: | ---: | --- |
| N02 Emily first draft | 13 | `hands`, `leaves`, `ready` | 7 of 12 | 10 of 11 | No |
| N06 Emily second draft | 11 | `quiet`, `stays`, `until` | 7 of 10 | 8 of 9 | No |
| N17 standby label | 8 | none | 0 of 7 | 0 of 6 | Yes, mail/11 |
| N18 commissioning label | 5 | none | 0 of 4 | 0 of 3 | Yes, mail/11 |

Reproducer: [`k08_proxy_lexicon.py`](k08_proxy_lexicon.py), standard-library, original-ZIP note-source SHA-pinned. It asserts the source fingerprint, each one-word gap count and presence/absence of a surviving verbatim complete caption.

## What this predicts and rules out

A **strictly extractive** procedure whose output vocabulary is restricted to that in surviving records *provably cannot* reconstruct either held-out draft N02 or N06 exactly, because three necessary word types are absent after withholding each line. Both controls N17/N18 remain trivially extractable via independent quotations in mail/11. This is a specific source-access contrast **without consulting the K08 hash**: a quoted sentence has a direct witness and an independent original sentence without duplication does not.

It does **not** establish that arbitrary generative language modeling cannot recover original exact words; generated words need not appear in the source. Nor does it prove that the unavailable final K08 caption contains any out-of-vocabulary word or that other source-constrained grammars are impossible. The control targets are public and have been read by multiple agents; a future language-model test on them must disclose possible exposure and cannot claim genuine blindness without isolation.

**Research consequence:** a further huge search limited to recombinations of the surviving file's word vocabulary has no demonstrated exact-author-language recall on these independent Emily drafts. The stronger next experiment would have an independent clean predictor rank withheld phrasing from comparable context and report exact normalized rank@20 before testing unseen true K08 guesses. Additional unchecked fluent word reorders do not bridge this demonstrated vocabulary/word-order gap. Computational K08 acceptance remains unchanged and could still be achieved by inference if an exact proposed phrase is accepted.

## Sequential-draft rewrite size, prehash

N02 ("first draft for the crew board") and N06 ("second desk draft") are both attributed directly to Emily but have only the function-word **`the`** in common among their distinct lowercase word types (1 shared type out of 21 in the union, Jaccard 1/21). As ordered word sequences they require **12 Levenshtein insert/delete/substitute operations** to convert N02's 13 words into N06's 11 words when each operation costs one; a read-only computation in the above script asserts this exact value. The longest common subsequence is two occurrences of `the`; no subject-specific noun or verb is retained.

This is a **source-grounded counterexample to assuming these two recorded draft captions followed a small local word-edit path**. The documents do not prove Emily revised N02 *into* N06 directly, or that her final caption changed by a comparable degree. Nevertheless a later search restricted to a few edits of one known draft lacks a strong prior from the two actual drafts. This discriminant is independent of the K08 acceptance hash.
