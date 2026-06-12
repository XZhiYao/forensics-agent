#!/usr/bin/env bash
# Week 5 附加轨道 A1 — 在 RTX 3090 (24 GB) 上启动 Qwen2.5-VL-7B (vLLM)
#
# Prerequisites:
#   pip install vllm
#   # model downloaded to $HF_HOME or HF cache automatically
#
# Usage:
#   bash scripts/model_service/start_qwen_7b.sh

set -euo pipefail

MODEL="Qwen/Qwen2.5-VL-7B-Instruct"
PORT=8000
GPU_MEM_UTIL=0.88      # leave ~3 GB headroom on a 24 GB card
MAX_MODEL_LEN=4096     # reduce if OOM; increase carefully

echo "Starting vLLM server: $MODEL on port $PORT"

python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --port "$PORT" \
    --gpu-memory-utilization "$GPU_MEM_UTIL" \
    --max-model-len "$MAX_MODEL_LEN" \
    --trust-remote-code \
    --limit-mm-per-prompt image=4 \
    --served-model-name "$MODEL"

# Test after startup:
#   curl http://localhost:8000/v1/models
