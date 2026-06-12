"""
Error Level Analysis (ELA) detector.

ELA re-saves the image at a fixed JPEG quality and measures
per-pixel difference. Bright regions indicate possible manipulation.

Implementation: Week 1 Day 5 (see ROADMAP.md).
"""

from __future__ import annotations

from pathlib import Path

from detectors.base import BaseDetector


class ELADetector(BaseDetector):
    name = "ela_detector"
    description = (
        "Detects image manipulation using Error Level Analysis (ELA). "
        "Returns a confidence score and path to the ELA visualisation map."
    )

    def __init__(self, quality: int = 75, scale: float = 10.0):
        self.quality = quality
        self.scale = scale

    def detect(self, image_path: str | Path) -> dict:
        # TODO (Week 1 D5): implement ELA using Pillow
        # 1. Re-save at self.quality
        # 2. Compute absolute difference
        # 3. Scale for visualisation
        # 4. Compute mean error as confidence proxy
        # 5. Save ELA map and return path
        raise NotImplementedError("ELA detector — implement in Week 1 D5")
