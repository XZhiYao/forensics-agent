"""
Forensics-Agent MCP Tool Server.

Exposes forensic detectors as MCP tools so any MCP-compatible client
(including the LangGraph agent) can discover and call them via the
standard Model Context Protocol.

Start the server:
    python -m mcp_server.server

Or via the MCP CLI:
    mcp dev mcp_server/server.py

Implementation schedule: Week 5 (see ROADMAP.md).
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

# Initialise the MCP server
mcp = FastMCP(
    "forensics-agent-tools",
    dependencies=["Pillow", "opencv-python-headless", "numpy", "scipy"],
)


# ── Tool registrations (filled in Week 5) ─────────────────────────────────────

@mcp.tool()
def ela_detector(image_path: str) -> dict:
    """
    Run Error Level Analysis on an image.

    Returns a confidence score and path to the ELA visualisation map.
    High confidence indicates potential manipulation.
    """
    # TODO (Week 5 D2): call ELADetector().detect(image_path)
    raise NotImplementedError("Implement in Week 5 D2")


@mcp.tool()
def noise_detector(image_path: str) -> dict:
    """
    Analyse noise residual patterns for local inconsistencies.

    Returns confidence and a visualisation of noise variance per block.
    Inconsistent noise is a strong splicing indicator.
    """
    # TODO (Week 5 D3): call NoiseDetector().detect(image_path)
    raise NotImplementedError("Implement in Week 5 D3")


@mcp.tool()
def copymove_detector(image_path: str) -> dict:
    """
    Detect copy-move forgery and JPEG ghost artifacts.

    Returns matched region pairs and a double-compression heatmap.
    """
    # TODO (Week 5 D3): call PatchDetector().detect(image_path)
    raise NotImplementedError("Implement in Week 5 D3")


@mcp.tool()
def benco_model(image_path: str) -> dict:
    """
    Run a SoTA IMDL-BenCo model for pixel-level manipulation localisation.

    Heavy-weight tool — call only when lightweight detectors are inconclusive.
    Returns a pixel-level mask path and image-level confidence.
    """
    # TODO (Week 6 D2): call BenCoModelDetector().detect(image_path)
    raise NotImplementedError("Implement in Week 6 D2")


if __name__ == "__main__":
    mcp.run()
