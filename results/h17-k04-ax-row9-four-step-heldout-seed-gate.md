# K04 AX row9 four-step seed test

Agent 26, 19 October 2026.

Read-only standalone program: [k04_ax_row9_forward_bridge.py](../agents/agent26/k04_ax_row9_forward_bridge.py).

Under the previously proposed six-output row9-to-row10 MT spacing and shared AX/printer source model, the intact row9 source fragment reconstructs S[p-174]=418BDA1E, S[p-173]=2E02BC3D and S[p-172].low31=38EBB043.

Three fully determined seed words from the separate late initialized-state quartet and one partially determined seed word predict the earlier held-out initialized-state word S[p-168] by four consecutive CPython seed updates. Four binary completions are required for each phase. For seed-array lengths 9, 19, 57 and 171, zero predictions match the original source word at any of the 219 phases p402..620.

Actual seeded Python positive controls pass in 144 of 144 cases, across six seed lengths and eight phases. The test never reads the selected K04 output or original acceptance commitments. All historical generator and alignment assumptions remain conditional. K04 and K08 have not been recovered.
