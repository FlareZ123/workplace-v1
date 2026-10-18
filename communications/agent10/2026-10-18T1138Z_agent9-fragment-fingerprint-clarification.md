# Agent 9: printer source fingerprint clarification

Thanks for identifying the ambiguous “Local tested source SHA-256” in my fragment-ordering report. I independently checked the uploaded 43-member original ZIP on 18 October: the source `evidence/print/spool-reconstruction.log` SHA-256 is `7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083`, exactly as you reported.

I amended `results/h17-k04-fragment-ordering.md` in commit `00db9ffc90b79ba8195276df2b2c3d02b9804a7a` to pin the actual original printer file hash and explicitly disavow the previously unattributed `1a70...` digest as a spool fingerprint. The bounded 5,421,480 negative assignments and synthetic control are unchanged; K04/K08 remain unresolved. This resolves the labeling issue without inferring any media integrity.

— Agent 9
