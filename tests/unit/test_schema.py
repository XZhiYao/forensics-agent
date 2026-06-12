"""
Unit tests for agent.schema — run these from Day 1 to verify the environment.

    pytest tests/unit/test_schema.py -v
"""

from __future__ import annotations

import pytest
from agent.schema import AnalysisResult, Evidence, Verdict, AgentState


def test_verdict_values():
    assert Verdict.MANIPULATED == "manipulated"
    assert Verdict.AUTHENTIC == "authentic"
    assert Verdict.UNCERTAIN == "uncertain"


def test_evidence_confidence_range():
    with pytest.raises(Exception):
        Evidence(tool_name="ela", signal="test", confidence=1.5)


def test_analysis_result_defaults():
    result = AnalysisResult(
        verdict=Verdict.UNCERTAIN,
        confidence=0.5,
        summary="Test summary.",
    )
    assert result.evidence == []
    assert result.trajectory == []


def test_agent_state_initial():
    state = AgentState(image_path="/tmp/test.jpg")
    assert state.step == 0
    assert state.result is None
    assert len(state.tools_called) == 0
