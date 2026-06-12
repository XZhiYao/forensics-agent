"""
Forensics-Agent LangGraph state machine.

Nodes:
    decision   — LLM decides which detector(s) to call next (cost-aware routing)
    detector   — Dispatches an MCP tool call and appends evidence to state
    reasoning  — LLM synthesises evidence into a faithfulness-grounded verdict

Edges:
    decision  → detector      (if more tools needed)
    decision  → reasoning     (if sufficient evidence or step limit reached)
    detector  → decision      (loop back for next routing decision)
    reasoning → END

Implementation schedule: Week 3–4 (see ROADMAP.md).
"""

from __future__ import annotations

# TODO (Week 3 D2): import StateGraph, END, etc.
# from langgraph.graph import StateGraph, END
# from agent.schema import AgentState
# from agent.nodes import decision_node, detector_node, reasoning_node


def build_graph():
    """Build and compile the LangGraph agent graph."""
    # TODO (Week 3–4): implement graph construction
    raise NotImplementedError("Graph — implement in Week 3")


if __name__ == "__main__":
    graph = build_graph()
    print(graph.get_graph().draw_ascii())
