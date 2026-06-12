"""
Abstract base class for all forensic detectors.
Every detector returns a dict conforming to Evidence.raw_output.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseDetector(ABC):
    """All detectors implement this interface so they can be
    registered as MCP tools uniformly."""

    name: str = "base_detector"
    description: str = "Abstract forensic detector"

    @abstractmethod
    def detect(self, image_path: str | Path) -> dict:
        """
        Run detection on a single image.

        Returns a dict with at least:
            {
                "tool_name": str,
                "signal": str,
                "confidence": float,          # [0, 1]
                "region": dict | None,        # {x, y, w, h}
                "artifact_path": str | None,  # saved visualisation
            }
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
