"""
Tier-1 Evaluation: Detection accuracy.

Runs the agent on benchmark datasets (CASIA, NIST16, Coverage) using
IMDL-BenCo evaluation protocol.

Metrics:
    - Image-level AUC / F1
    - Pixel-level F1 / AUC (per IMDLBenCo protocol)
    - Robustness under JPEG / resize / noise perturbation

Usage:
    python eval/detection/eval_detection.py --config configs/eval.yaml

Implementation schedule: Week 11 (see ROADMAP.md).
"""

from __future__ import annotations

import argparse

# TODO (Week 11): implement batch evaluation loop


def main():
    parser = argparse.ArgumentParser(description="Detection accuracy evaluation")
    parser.add_argument("--config", default="configs/eval.yaml")
    parser.add_argument("--dataset", choices=["casia", "nist16", "coverage"], default="casia")
    parser.add_argument("--output_dir", default="experiments/results")
    args = parser.parse_args()

    raise NotImplementedError("Implement in Week 11")


if __name__ == "__main__":
    main()
