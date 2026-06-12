"""
Tier-2 Evaluation: Agent-trajectory faithfulness.

Metrics:
    - Tool selection accuracy       (did agent call the right tool?)
    - Mean reasoning steps          (efficiency)
    - Evidence grounding score      (IoU between cited region and GT mask)
    - LLM-as-judge explanation quality  (0–5 rubric)
    - Regression pass/fail          (no degradation after model/prompt changes)

Usage:
    python eval/trajectory/eval_agent.py --config configs/eval.yaml

Implementation schedule: Week 12 (see ROADMAP.md).
"""

from __future__ import annotations

import argparse

# TODO (Week 12): implement trajectory evaluation loop


def main():
    parser = argparse.ArgumentParser(description="Agent trajectory faithfulness evaluation")
    parser.add_argument("--config", default="configs/eval.yaml")
    parser.add_argument("--output_dir", default="experiments/results")
    parser.add_argument("--judge_model", default="gemini-2.5-pro")
    args = parser.parse_args()

    raise NotImplementedError("Implement in Week 12")


if __name__ == "__main__":
    main()
