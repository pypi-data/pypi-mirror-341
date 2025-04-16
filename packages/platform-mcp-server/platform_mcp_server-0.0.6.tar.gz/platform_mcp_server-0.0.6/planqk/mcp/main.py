import os
import signal
import sys

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

BASE_URL = "https://space-0adb49cf-05f4-4bd2-8b5d-f9d85753bc74-752661922255.europe-west1.run.app/chat"
PLATFORM_SERVICES_BASE_URL = "https://platform.planqk.de/qc-catalog/v2/apis"

mcp = FastMCP("platform")


def signal_handler(sig, frame):
    print("\nShutting down MCP server...")
    sys.exit(0)


@mcp.tool()
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


@mcp.tool()
async def describe_kipu_services() -> str:
    """
    IMPORTANT: This tool MUST be used whenever the question contains any of these keywords:
    - kipu services
    - kipu service
    - dcqo
    - bf-dcqo

    This tool helps to understand the KIPU services provided in the PLANQK Platform Marketplace.
    """
    package_path = os.path.dirname(__file__)
    file_path = os.path.join(package_path, "kipu_services.txt")
    with open(file_path, "r") as file:
        content = file.read()
        return content


class MarketplaceServiceDetails(BaseModel):
    context: str
    gateway_endpoint: str = Field(alias="gatewayEndpoint")
    description: str


class MarketplaceService(BaseModel):
    id: str
    service_id: str = Field(alias="serviceId")
    name: str
    pricing_plan_type: str = Field(alias="pricingPlanType")
    provider: str
    service_type: str = Field(alias="serviceType")
    details: MarketplaceServiceDetails


@mcp.tool()
async def describe_kipu_services_v2() -> list[MarketplaceService]:
    """
    IMPORTANT: This tool MUST be used whenever the question contains any of these keywords:
    - kipu services
    - kipu service
    - dcqo
    - bf-dcqo

    This tool helps to understand the KIPU services provided in the PLANQK Platform Marketplace.
    """
    api_key = os.getenv("PLANQK_API_KEY")
    if not api_key:
        raise ValueError("PLANQK_API_KEY environment variable is not set.")

    return get_kipu_services(api_key)


def get_kipu_services(api_key: str) -> list[MarketplaceService]:
    with httpx.Client() as client:
        response = client.get(
            PLATFORM_SERVICES_BASE_URL,
            headers={"x-auth-token": api_key},
        )
        # filter for Kipu services
        services = [
            service
            for service in response.json()
            if service["provider"] == "Kipu Quantum"
        ]

        # load details for each service
        for service in services:
            details = client.get(
                f"{PLATFORM_SERVICES_BASE_URL}/{service['id']}",
                headers={"x-auth-token": api_key},
            )
            service["details"] = details.json()

        # parse the services into a list of MarketplaceService objects
        services = [
            MarketplaceService(**service)
            for service in services
        ]

        return services


def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("MCP server started. Press Ctrl+C to exit.")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
