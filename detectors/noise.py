"""
Noise residual detector.

Uses SRM (Steganalysis Rich Model) or Gaussian noise residual to
detect local inconsistencies in noise patterns indicative of splicing.

Implementation: Week 2 Day 5 (see ROADMAP.md).
"""

from __future__ import annotations

from pathlib import Path

from detectors.base import BaseDetector


class NoiseDetector(BaseDetector):
    name = "noise_detector"
    description = (
        "Detects manipulation by analysing noise residual inconsistencies across image regions."
    )

    def detect(self, image_path: str | Path) -> dict:
        # TODO (Week 2 D5): implement noise residual analysis
        raise NotImplementedError("Noise detector — implement in Week 2 D5")
