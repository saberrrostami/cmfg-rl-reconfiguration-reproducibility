# Prespecified recovery-capacity sensitivity extension

## Purpose
This extension tests whether limited shared recovery capacity is operationally consequential in the runtime cloud-manufacturing reconfiguration setting. The protocol was frozen before confirmatory sensitivity execution. No sensitivity outcome was used to retune PPO or B6.

## Capacity levels
- B = 0: recovery unavailable.
- B = 1: original single shared recovery unit.
- B = 2: two shared recovery units.
- B = 500: effectively non-binding at the tested scale.

## PPO training and validation
- Training seeds: 1001-1005.
- Training budget: 800,000 transitions per run.
- B = 1 reuses the original frozen training runs/checkpoints.
- B = 0, 2, and 500 were retrained independently under the same budget and validation-only checkpoint/deployment selection procedure.
- Validation-selected deployment seeds: B0=1004, B1=1004, B2=1001, B500=1005.

## B6 benchmark
- Frozen configuration: 2 x 25 look-ahead/scenario setting.
- Decision time limit: 5 s.
- MIP gap target: 5%.
- Prespecified fallback eligibility threshold: <=1%.

## Held-out sensitivity bank
- Fresh fixed seed bank: 990001-990050.
- These seeds were not used for training, validation, the original held-out analysis, or model selection.
- Common random numbers are preserved within each capacity so PPO and B6 face matched exogenous events.

## Main sensitivity findings
Selected-policy mean relative cost reduction vs B6 (positive favors PPO):
- B=0: 4.18% (95% CI 2.90 to 5.59)
- B=1: 7.11% (95% CI 4.77 to 9.42)
- B=2: 6.03% (95% CI 3.50 to 8.52)
- B=500: 1.84% (95% CI 1.37 to 2.31)

PPO-family mean relative cost reduction vs B6:
- B=0: 3.58% (95% CI 2.40 to 4.88)
- B=1: -0.09% (95% CI -2.54 to 2.21)
- B=2: -6.06% (95% CI -8.74 to -3.38)
- B=500: -23.43% (95% CI -28.82 to -18.29)

B6 full-capacity time fraction:
- B=0: 0.00%
- B=1: 66.81%
- B=2: 43.57%
- B=500: 0.00%

At B=2, B6 used the predefined fallback in 5 of 11,837 decisions (0.042%), below the prespecified 1% eligibility threshold; other capacities had zero fallbacks.

## Secondary fixed-policy mechanism diagnostic
The original B=1 validation-selected policy (seed 1004) was evaluated unchanged at B=0,1,2,500 on the same sensitivity seeds. Mean operating cost declined monotonically as capacity relaxed: 7.9083, 5.5617, 4.1994, and 2.9035, respectively. This is a secondary within-controller mechanism check, not a replacement for the prespecified capacity-specific retraining analysis.

## Interpretation boundary
The sensitivity supports the problem-level claim that limited shared recovery is an active operational constraint. It does not establish universal PPO superiority. Family-average PPO does not uniformly dominate B6 as capacity changes, while validation-selected deployment policies are favorable at all four tested capacities. The selected-policy advantage also persists at B=0 and B=500, so scarcity alone should not be presented as the sole cause of the PPO-B6 difference.

## Folder map
- 01_PROTOCOL_AND_RUNNERS: frozen execution package used for the sensitivity.
- 02_SELECTED_CHECKPOINTS_AND_GATES: all capacity-specific selected PPO checkpoints/reports plus B6/training gate records.
- 03_HELDOUT_RAW_JOBS: ten raw held-out job archives covering all 50 sensitivity seeds.
- 04_FINAL_ANALYSIS: merged rows, summaries, bootstrap outputs, manuscript table, and Figure 10.

## PLOS ONE figure mapping
The capacity sensitivity corresponds to manuscript Fig 9 (not Fig 10). Historical output `04_FINAL_ANALYSIS/Figure_10_Recovery_Capacity_Sensitivity.*` is retained unchanged to preserve analysis provenance. The normalized exported graphic is `06_FIGURES/Figure_9_Recovery_Capacity_Sensitivity.png`.
