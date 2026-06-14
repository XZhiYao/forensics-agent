"""
LangGraph node functions.

Each function takes AgentState and returns a partial state update dict.
Implementation schedule: Week 3–4 (see ROADMAP.md).

State: { image_path, evidence[], tools_called[], step, result }
         ↓
decision_node → 决定调哪个工具
         ↓
detector_node → 执行工具，把 Evidence 追加进 state
         ↓
         ↑（循环，最多 max_steps 次）
         ↓
reasoning_node → 综合所有 evidence 给出最终判断
"""
from __future__ import annotations

# from agent.schema import AgentState


def decision_node(state: dict) -> dict:
    """
    Cost-aware routing: decide whether to call another tool or proceed
    to reasoning. Lightweight detectors (ELA, noise, copy-move) are
    preferred first; benco_model is called only if they are inconclusive.

    TODO (Week 3 D3): implement with LLM tool-selection prompt.
    """
    raise NotImplementedError


def detector_node(state: dict) -> dict:
    """
    Execute the MCP tool chosen by decision_node.
    Append the resulting Evidence to state["evidence"].

    TODO (Week 3 D4): implement MCP tool dispatch.
    """
    raise NotImplementedError


def reasoning_node(state: dict) -> dict:
    """
    Synthesise all collected evidence into an AnalysisResult.
    The summary must cite specific evidence items (faithfulness requirement).

    TODO (Week 4 D3): implement with faithfulness-grounded prompt.
    """
    raise NotImplementedError
