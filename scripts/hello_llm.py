"""
Week 1 Day 1 — Hello LLM smoke test.

Verifies that the configured LLM provider (Gemini or local vLLM) responds.
Run this first after setting up configs/.env.

Usage:
    python scripts/hello_llm.py
    python scripts/hello_llm.py --provider local   # test local Qwen endpoint
"""

from __future__ import annotations

import argparse
import os
import sys

# Make sure project root is on path when running as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=["gemini", "local"], default=None)
    args = parser.parse_args()

    if args.provider:
        os.environ["AGENT_MODEL_PROVIDER"] = args.provider

    from configs.settings import settings

    print(f"Provider : {settings.agent_model_provider}")
    print(f"Model    : {settings.gemini_model if settings.agent_model_provider == 'gemini' else settings.local_vlm_model}")

    llm = settings.build_llm()
    response = llm.invoke("Reply with exactly one sentence: what is your name and version?")
    print(f"\nLLM response:\n{response.content}")


if __name__ == "__main__":
    main()
