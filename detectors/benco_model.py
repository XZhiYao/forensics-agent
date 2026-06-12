"""
IMDL-BenCo SoTA model wrapper.

Wraps a pre-trained Image Manipulation Detection & Localisation model
from the IMDL-BenCo benchmark as a detector tool. Used as the
"heavy weapon" called only when lightweight detectors are inconclusive.

Reference: https://github.com/scu-zjz/IMDLBenCo  (NeurIPS 2024 Spotlight)

Implementation: Week 6 Day 2 (see ROADMAP.md).
"""

from __future__ import annotations

from pathlib import Path

from detectors.base import BaseDetector


class BenCoModelDetector(BaseDetector):
    name = "benco_model"
    description = (
        "SoTA image manipulation localisation model from IMDL-BenCo. "
        "Produces a pixel-level manipulation mask. Used as a heavy-weight "
        "detector when lightweight signals are inconclusive."
    )

    def __init__(self, weights_path: str | None = None):
        self.weights_path = weights_path

    def detect(self, image_path: str | Path) -> dict:
        # TODO (Week 6 D2): load IMDLBenCo model, run inference, return mask
        raise NotImplementedError("BenCo model detector — implement in Week 6 D2")
