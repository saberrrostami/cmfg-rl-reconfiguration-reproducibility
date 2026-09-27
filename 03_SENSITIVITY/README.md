# Priority-weight sensitivity (R1C)

This is a **post-hoc fixed-controller accounting sensitivity**, not a new confirmatory PPO-vs-B6 experiment.

- Controller: development-selected PPO seed 1004, frozen v13F2 checkpoint.
- Final panel: seeds 970001–970050 (already opened in the main fixed-N=50 evaluation).
- Rescoring values: alpha = 0.25, 0.50, 1.00 in w_j = 1 + alpha * priority_j.
- No retraining, checkpoint reselection, trajectory change, or policy tuning.
- The alpha=0.50 rescore reproduces the reported v13F2 PPO1004 mean cost.
- Completion is invariant because the same policy decisions and exogenous streams are used.
- Repaired B6 was **not** reoptimized under the alternative alpha values; therefore these rows must not be interpreted as a new comparative ranking sensitivity.
