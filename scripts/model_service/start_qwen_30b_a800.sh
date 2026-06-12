#!/usr/bin/env bash
# Week 5 附加轨道 A2 — 在 A800 (80 GB) 上启动 Qwen3-VL-30B-A3B (vLLM)
#
# Qwen3-VL-30B-A3B is a MoE model: 30 B total params, only ~3 B active per token.
# Very memory-efficient on a single A800.
# Alternatively swap MODEL for Qwen/Qwen2.5-VL-32B-Instruct (dense, ~64 GB fp16).
#
# Usage:
#   bash scripts/model_service/start_qwen_30b_a800.sh

set -euo pipefail

# Switch to Qwen/Qwen2.5-VL-32B-Instruct for the dense alternative
MODEL="Qwen/Qwen3-VL-30B-A3B-Instruct"
PORT=8001               # different port to run alongside the 7B service
GPU_MEM_UTIL=0.90
MAX_MODEL_LEN=8192

echo "Starting vLLM server: $MODEL on port $PORT"

python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --port "$PORT" \
    --gpu-memory-utilization "$GPU_MEM_UTIL" \
    --max-model-len "$MAX_MODEL_LEN" \
    --trust-remote-code \
    --limit-mm-per-prompt image=8 \
    --served-model-name "$MODEL"

# To use FP8 (official Qwen FP8 checkpoint, further reduces memory):
#   add: --quantization fp8
#   and use the FP8 variant model name from HuggingFace
