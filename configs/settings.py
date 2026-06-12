"""
Central configuration loaded from environment variables (.env or shell).

Usage:
    from configs.settings import settings

    llm = settings.build_llm()   # returns Gemini or local-vLLM client
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="configs/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Provider switch ───────────────────────────────────────
    agent_model_provider: str = "gemini"  # "gemini" | "local"

    # ── Gemini ────────────────────────────────────────────────
    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # ── Local vLLM (Qwen-VL, OpenAI-compatible) ──────────────
    local_vlm_base_url: str = "http://localhost:8000/v1"
    local_vlm_model: str = "Qwen/Qwen2.5-VL-7B-Instruct"
    local_vlm_api_key: str = "EMPTY"

    # ── Observability ─────────────────────────────────────────
    langsmith_api_key: str = ""
    langsmith_project: str = "forensics-agent"
    langchain_tracing_v2: bool = True

    # ── MCP ───────────────────────────────────────────────────
    mcp_server_host: str = "localhost"
    mcp_server_port: int = 9000

    # ── Dataset paths ─────────────────────────────────────────
    casia_root: str = "/data/datasets/CASIA"
    nist16_root: str = "/data/datasets/NIST16"
    coverage_root: str = "/data/datasets/Coverage"
    imdl_benco_weights: str = "/data/weights/imdlbenco"

    @property
    def mcp_server_url(self) -> str:
        return f"http://{self.mcp_server_host}:{self.mcp_server_port}/sse"

    def build_llm(self):
        """Return a LangChain chat model according to the active provider."""
        if self.agent_model_provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model=self.gemini_model,
                google_api_key=self.google_api_key,
                temperature=0.0,
            )
        elif self.agent_model_provider == "local":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                base_url=self.local_vlm_base_url,
                model=self.local_vlm_model,
                api_key=self.local_vlm_api_key,
                temperature=0.0,
            )
        else:
            raise ValueError(f"Unknown provider: {self.agent_model_provider}")


settings = Settings()
