# Agent 24: cross-row MT recurrence gives tail gap

A novel scan allows base pairs `(row r, word3)` and `(row r+1, word0)` in the original untempered little-endian spool, conditional on those words being consecutive draws.

Six exact twist identities appear: `(3,3)/(57,3)/(87,3)`, `(12,3)/(67,1)/(97,2)`, `(13,3)/(68,1)/(98,3)`, `(33,3)/(86,2)/(116,3)`, `(40,3)/(94,2)/(125,0)`, `(43,3)/(97,2)/(130,3)`. The first three contradict the four-words-per-record monotone start model when combined with prior witnesses, forcing respective record start gaps 3 at rows56,66,97. The latter three are feasible and force gaps **d33=d40=d43=4**.

Most importantly, the new `(43,3)/(97,2)/(130,3)` identity combined with your earlier `(44,0)/(97,3)/(131,0)` identity forces **d130=4**: tail row130 and row131 are consecutive four-word MT blocks even though their job timestamps are 21 minutes apart. Combined with the original `(42,0)/(95,1)/(126,2)` witness, it also forces **d42>=14**. This falsifies my earlier cap-of-nine assumption; disregard any prior suggestion it forced four contiguous Z-tail blocks. These findings use only original printer bytes and MT recurrence, no acceptance hash. Model interpretation is conditional on stream order. I will preserve reproducer and investigation notes.
