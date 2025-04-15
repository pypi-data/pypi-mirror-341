from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://space-0adb49cf-05f4-4bd2-8b5d-f9d85753bc74-752661922255.europe-west1.run.app/chat"


mcp = FastMCP("platform")


@mcp.tool()
async def find_platform_documentation(question: str) -> str:
    """
    Fetch relevant information from the PLANQK Platform documentation based on the user's question.
    The documentation includes:
        - Quick Start Guide
        - Documentation about the PLANQK Quantum SDK, PLANQK Service SDK, and PLANQK CLI
        - How to manage organizations and projects
        - About PLANQK Services, Managed Services, PLANQK Marketplace, How to use Services, Automations, Use Cases
        - It also contains tutorials, FAQs, and more.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            BASE_URL, json={"question": question, "history": []}, timeout=30.0
        )
        response.raise_for_status()
        return response.json()["message"]["content"]


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
