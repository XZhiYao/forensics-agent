"""
Shared Pydantic schemas used across the agent, MCP server, and API.
All inter-module data exchange passes through these models.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Verdict(str, Enum):
    AUTHENTIC = "authentic"
    MANIPULATED = "manipulated"
    UNCERTAIN = "uncertain"


class Region(BaseModel):
    """Bounding box or pixel-mask reference for a detected anomaly."""

    x: int = Field(..., description="Left pixel coordinate")
    y: int = Field(..., description="Top pixel coordinate")
    w: int = Field(..., description="Width in pixels")
    h: int = Field(..., description="Height in pixels")
    mask_path: str | None = Field(None, description="Path to pixel-level mask file")


class Evidence(BaseModel):
    """One piece of forensic evidence produced by a single detector tool."""

    tool_name: str = Field(..., description="Name of the MCP tool that produced this evidence")
    signal: str = Field(..., description="Human-readable description of the detected signal")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detector confidence [0, 1]")
    region: Region | None = Field(None, description="Spatial location of the anomaly")
    artifact_path: str | None = Field(None, description="Path to saved visualisation (ELA map, etc.)")
    raw_output: dict[str, Any] = Field(default_factory=dict, description="Full raw detector output")


class TrajectoryStep(BaseModel):
    """One step in the agent's reasoning trajectory (for faithfulness eval)."""

    step: int
    node: str = Field(..., description="LangGraph node name")
    action: str = Field(..., description="What the agent decided to do")
    tool_called: str | None = None
    reasoning: str | None = None


class AnalysisResult(BaseModel):
    """Final output returned by the agent and the API."""

    verdict: Verdict
    confidence: float = Field(..., ge=0.0, le=1.0)
    summary: str = Field(..., description="Evidence-grounded natural language explanation")
    evidence: list[Evidence] = Field(default_factory=list)
    trajectory: list[TrajectoryStep] = Field(default_factory=list)
    model_provider: str = Field("", description="LLM provider used (gemini / local)")
    vlm_model: str = Field("", description="Exact VLM model name used")


class AgentState(BaseModel):
    """LangGraph state object passed between nodes."""

    image_path: str
    evidence: list[Evidence] = Field(default_factory=list)
    trajectory: list[TrajectoryStep] = Field(default_factory=list)
    tools_called: list[str] = Field(default_factory=list)
    result: AnalysisResult | None = None
    step: int = 0
    max_steps: int = 5
