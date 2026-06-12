# System Architecture

## Overview

Forensics-Agent is a multi-step agentic system built on LangGraph.
Forensic detection capabilities are exposed as **MCP tools**, enabling
any MCP-compatible client to discover and call them via the Model Context Protocol.

## Component Diagram

```
┌──────────────────────────────────────────────────────┐
│                     Client                           │
│   (FastAPI /analyze  ·  curl  ·  demo page)          │
└───────────────────────┬──────────────────────────────┘
                        │ HTTP POST /analyze
┌───────────────────────▼──────────────────────────────┐
│               LangGraph Agent (agent/)               │
│                                                      │
│  ┌─────────────┐   ┌──────────────┐  ┌───────────┐  │
│  │  Decision   │──▶│   Detector   │─▶│ Reasoning │  │
│  │   Node      │◀──│    Node      │  │   Node    │  │
│  │ (routing)   │   │ (MCP calls)  │  │ (verdict) │  │
│  └─────────────┘   └──────────────┘  └───────────┘  │
│          │                │                          │
│  AgentState (Pydantic)    │                          │
│          └────────────────┘                          │
└───────────────────────┬──────────────────────────────┘
                        │ MCP (SSE / stdio)
┌───────────────────────▼──────────────────────────────┐
│            MCP Tool Server (mcp_server/)              │
│                                                      │
│  ● ela_detector      (lightweight, fast)             │
│  ● noise_detector    (lightweight, fast)             │
│  ● copymove_detector (lightweight, medium)           │
│  ● benco_model       (heavy — SoTA IML model)        │
└───────────────────────┬──────────────────────────────┘
                        │ PyTorch / OpenCV
┌───────────────────────▼──────────────────────────────┐
│             Detectors (detectors/)                   │
└──────────────────────────────────────────────────────┘
```

## Cost-Aware Tool Routing

The Decision Node routes tool calls in two tiers to balance speed and accuracy.

- **Tier 1 (lightweight)** — ELA, noise, copy-move: fast, CPU-capable.
  Called first on every image.
- **Tier 2 (heavy)** — IMDL-BenCo SoTA model: GPU-intensive, high accuracy.
  Called only when Tier-1 signals are inconclusive (confidence < threshold)
  or when the routing LLM judges them insufficient.

## Model Provider Abstraction

```
configs/settings.py  →  AGENT_MODEL_PROVIDER=gemini | local
                                │
              ┌─────────────────┴──────────────────┐
              │                                    │
   ChatGoogleGenerativeAI               ChatOpenAI (vLLM)
   (Gemini 2.5 Pro / Flash)     (Qwen3-VL-30B-A3B on A800)
```

Switching providers requires only changing one environment variable.
This design enables the Gemini vs. Qwen-VL ablation study in Week 12.

## Two-Tier Evaluation

| Tier | What is measured | Where |
|---|---|---|
| Detection accuracy | pixel-F1, AUC, robustness | `eval/detection/` |
| Agent-trajectory faithfulness | tool selection accuracy, evidence IoU, LLM-as-judge | `eval/trajectory/` |
