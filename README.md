# Reproducibility package

## Article
**Dynamic service composition reconfiguration in cloud manufacturing under limited shared recovery capacity: A reinforcement learning approach**

This repository contains the frozen code, data inputs, selected model checkpoints, benchmark configuration, held-out results, sensitivity outputs, computational diagnostics, and figures used to support the article.

## Reproducibility scope
- Five independent PPO training runs: seeds 1001–1005.
- Fixed training budget: 800,000 transitions per run.
- Eligible late checkpoints: 600k, 700k, and 800k transitions.
- Final held-out test: 50 seeds, 970001–970050.
- Common random numbers are used for paired PPO/B6 comparisons.
- Validation-selected deployment policy: PPO seed 1004.
- Primary benchmark: stochastic rolling-horizon MILP (B6).
- Confirmatory experiments use one shared recovery unit (B = 1).

The family-level PPO estimate averages the five independently trained policies. The validation-selected policy is reported separately. The package does not support a causal recovery-capacity ablation because B = 0, B > 1, and nonbinding recovery settings were not part of the confirmatory design.

## Directory structure
- `01_CORE_AND_CHECKPOINTS/` — frozen scientific source code, public input workbooks, protocol files, selected PPO checkpoints, and development-selection records.
- `02_RESULTS/` — fixed-N held-out results, B6 development summary, effect summaries, row-level outputs, and merge reports.
- `03_SENSITIVITY/` — fixed-controller priority-weight accounting sensitivity.
- `04_COMPUTATIONAL_AUDIT/` — post-hoc PPO/B6 timing scripts and outputs.
- `05_EXPLORATORY/` — descriptive analysis stratified by B6 completion.
- `06_FIGURES/` — manuscript figures numbered to match the final manuscript (Figures 1–9).

## Software environment
The frozen scientific core includes `requirements_colab.txt`. Its principal Python dependencies are:
- openpyxl >= 3.1
- PyYAML >= 6.0
- scipy >= 1.11
- matplotlib >= 3.7

The selected model checkpoints additionally require the PyTorch environment used by the archived scientific code.

## Source manufacturing data
The six flexible-packaging workbooks included in the frozen scientific core originate from:

Tarigan, M. (2025). *Data for Flexible Packaging Scheduling*. Mendeley Data, Version 1. https://doi.org/10.17632/h66hb89k6z.1

The source dataset is distributed under the **CC BY 4.0** license. The dataset files are included here for reproducibility with attribution to the original source and remain subject to that source license.

## Interpretation boundaries
- The study is an empirically grounded simulation, not a field deployment of a commercial CMfg platform.
- Results from the validation-selected PPO policy are distinct from the family-average result across the five independently trained policies.
- The recovery-capacity level is fixed at B = 1 in the confirmatory evaluation.
- The priority-weight analysis is a fixed-trajectory accounting sensitivity; B6 is not reoptimized at alternative priority weights.
- Timing results are hardware- and implementation-dependent diagnostics rather than confirmatory performance endpoints.

## Integrity
`MANIFEST_SHA256.csv` provides a SHA-256 digest and file size for every file in this release. Inner frozen archives also retain their original checksums.

## License note
No new license for the project code is asserted by this package. Before public release, the authors may add an explicit software license (for example, MIT) if appropriate. The included source dataset retains its original CC BY 4.0 license.
