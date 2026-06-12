"""
Copy-move / patch detector.

Detects copy-move forgery by finding repeated image blocks or
JPEG ghost artifacts from double compression.

Implementation: Week 4 Day 2 (see ROADMAP.md).
"""

from __future__ import annotations

from pathlib import Path

from detectors.base import BaseDetector


class PatchDetector(BaseDetector):
    name = "copymove_detector"
    description = (
        "Detects copy-move forgery and JPEG ghost artifacts indicating"
        " double-compressed spliced regions."
    )

    def detect(self, image_path: str | Path) -> dict:
        # TODO (Week 4 D2): implement copy-move / JPEG ghost detection
        raise NotImplementedError("Patch/copy-move detector — implement in Week 4 D2")
