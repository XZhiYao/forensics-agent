"""
Forensics-Agent REST API.

Endpoints:
    POST /analyze          — analyse an uploaded image
    GET  /health           — liveness probe

Run locally:
    uvicorn api.app:app --reload --port 8080

Implementation schedule: Week 9 (see ROADMAP.md).
"""

from __future__ import annotations

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from agent.schema import AnalysisResult

app = FastAPI(
    title="Forensics-Agent API",
    description="LangGraph-based image manipulation detection with evidence-grounded reasoning.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(file: UploadFile = File(...)):
    """
    Upload an image and receive a structured manipulation analysis.

    Returns:
        AnalysisResult with verdict, confidence, evidence list,
        and full agent trajectory.
    """
    # TODO (Week 9 D2): save upload → call agent → return result
    raise HTTPException(status_code=501, detail="Not implemented yet — see Week 9")
