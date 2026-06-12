# Experiments

This directory stores all evaluation results, figures, and logs.

## Directory layout

```
experiments/
├── results/      CSV / JSON tables from eval runs
├── figures/      matplotlib / seaborn plots for the paper
└── logs/         Raw agent trace logs (gitignored by default)
```

## Naming convention

```
results/
  YYYYMMDD_<dataset>_<model>_<notes>.csv
  e.g. 20251101_casia_gemini25flash_baseline.csv
       20251115_nist16_qwen3vl30b_mcp_v2.csv

figures/
  fig<N>_<description>.pdf
  e.g. fig1_system_architecture.pdf
       fig2_detection_comparison.pdf
```

## How to record an experiment

1. Fix random seeds: `PYTHONHASHSEED=0`, `numpy.random.seed(42)`, `torch.manual_seed(42)`.
2. Commit your code at the start of the run: `git rev-parse HEAD > experiments/results/<run_name>_gitsha.txt`.
3. Save the full config used: `python eval/detection/eval_detection.py --config configs/eval.yaml --dump_config experiments/results/<run_name>_config.yaml`.
4. Append the run to `experiments/results/index.csv` with columns: date, dataset, model, phase, pixel_f1, image_auc, notes.
