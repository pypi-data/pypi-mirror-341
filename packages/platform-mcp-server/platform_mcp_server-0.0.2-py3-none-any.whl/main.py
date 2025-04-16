from typing import Any
import signal
import sys

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://space-0adb49cf-05f4-4bd2-8b5d-f9d85753bc74-752661922255.europe-west1.run.app/chat"


mcp = FastMCP("platform")


def signal_handler(sig, frame):
    print("\nShutting down MCP server...")
    sys.exit(0)


@mcp.tool(name="PLANQK Platform Copilot")
async def ask_platform_copilot(question: str) -> str:
    """
    IMPORTANT: This tool MUST be used whenever the question contains any of these keywords:
    - planqk
    - planqk cli
    - planqk sdk
    - planqk service sdk
    - planqk quantum sdk
    - planqk marketplace
    - planqk services
    
    This tool fetches relevant information from the PLANQK Platform documentation based on the user's question.
    The documentation includes:
        - Quick start guide
        - Documentation about the PLANQK Quantum SDK, PLANQK Service SDK, and PLANQK CLI
        - How to manage organizations and projects
        - How to create and use PLANQK Services and the PLANQK Marketplace
        - Tutorials, FAQs, and more.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            BASE_URL, json={"question": question, "history": []}, timeout=30.0
        )
        response.raise_for_status()
        return response.json()["message"]["content"]


def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("MCP server started. Press Ctrl+C to exit.")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
