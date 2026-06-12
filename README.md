# Forensics-Agent

> A LangGraph-based agentic system for image manipulation detection.
> Detection tools (ELA, noise residual, copy-move, and a SoTA IMDL-BenCo model) are exposed as MCP tools.
> The agent performs cost-aware tool routing with evidence-grounded reasoning, and ships with full tracing,
> structured-output guardrails, and a two-tier evaluation harness covering detection accuracy and
> agent-trajectory faithfulness.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.x-green.svg)](https://github.com/langchain-ai/langgraph)

---

## Architecture

```
Image Input
    │
    ▼
┌─────────────────────────────────────┐
│         LangGraph Agent             │
│  ┌──────────────────────────────┐   │
│  │   Decision Node              │   │
│  │   (cost-aware tool routing)  │   │
│  └──────────┬───────────────────┘   │
│             │ MCP calls             │
│  ┌──────────▼───────────────────┐   │
│  │   MCP Tool Server            │   │
│  │   ├── ela_detector           │   │
│  │   ├── noise_detector         │   │
│  │   ├── copymove_detector      │   │
│  │   └── benco_model (SoTA IML) │   │
│  └──────────┬───────────────────┘   │
│             │ evidence[]            │
│  ┌──────────▼───────────────────┐   │
│  │   Reasoning Node             │   │
│  │   (faithfulness-grounded)    │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
    │
    ▼
AnalysisResult { verdict, confidence, evidence[], regions, trajectory }
```

## Quick Start

```bash
git clone https://github.com/<your-username>/forensics-agent.git
cd forensics-agent
pip install -e ".[dev]"
cp configs/.env.example configs/.env   # fill in your API keys
python scripts/hello_llm.py            # smoke test
```

## Models

| Role | Model | Where |
|---|---|---|
| Agent brain (primary) | Gemini 2.5 Pro / Flash | API |
| Local open-source VLM | Qwen3-VL-30B-A3B or Qwen2.5-VL-32B | A800 via vLLM |
| Fast iteration | Qwen2.5-VL-7B | RTX 3090 via vLLM |

See [`scripts/model_service/`](scripts/model_service/) for vLLM launch commands.

## Evaluation

This project ships a **two-tier evaluation harness**:

1. **Detection accuracy** — pixel-level F1 / AUC / image-level AUC on CASIA, NIST16, Coverage via IMDLBenCo protocol.
2. **Agent-trajectory faithfulness** — tool selection accuracy, reasoning step count, evidence grounding score (IoU between cited region and ground-truth mask), LLM-as-judge explanation quality.

```bash
python eval/detection/eval_detection.py --config configs/eval.yaml
python eval/trajectory/eval_agent.py    --config configs/eval.yaml
```

## Project Status

Built as part of a structured 14-week learning roadmap. See [ROADMAP.md](ROADMAP.md) for the weekly plan.

| Phase | Status |
|---|---|
| Phase 0 — LLM / LangChain / RAG basics | ☐ |
| Phase 1 — LangGraph multi-step reasoning | ☐ |
| Phase 2 — MCP tool server + local Qwen-VL | ☐ |
| Phase 3 — Observability + reliability | ☐ |
| Phase 4 — FastAPI + Docker deployment | ☐ |
| Phase 5 — Two-tier evaluation | ☐ |
| Phase 6 — Paper draft + public release | ☐ |

## Citation

If you use this work, please cite:

```bibtex
@misc{forensics-agent-2025,
  title   = {Forensics-Agent: Agentic Tool Orchestration for Image Manipulation Detection},
  author  = {<Your Name>},
  year    = {2025},
  url     = {https://github.com/<your-username>/forensics-agent}
}
```

## License

MIT
