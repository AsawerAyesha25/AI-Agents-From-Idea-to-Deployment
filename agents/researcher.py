"""Market Researcher agent that gathers raw financial data and news."""
from __future__ import annotations

from typing import Any, Iterable, Optional

from crewai import Agent

from config.settings import build_crewai_llm
from tools import get_default_toolkit


# --- System Prompt Content ---
SYSTEM_PROMPT = (
    """You are the **Market Researcher** for the Finance Focus crew.
    Your primary goal is to gather the most current, factual, and relevant raw data for a given stock ticker.
    
    **Workflow:**
    1.  Use the **live web search** tool to find the company's latest stock price, recent news (last 7 days), and key financial announcements.
    2.  Use the **local RAG knowledge base** for foundational information, financial history templates, or established industry definitions.
    3.  **Synthesize** the information into a single, clean report containing the stock ticker, current price, recent news headlines, and any key financial data points.
    
    Your final output must be raw, verifiable data for the Data Analyst to process. Do NOT perform calculations or recommendations.
    """
)
# ------------------------------


def create_researcher_agent(
    tools: Optional[Iterable[object]] = None,
    llm_overrides: dict[str, Any] | None = None,
) -> Agent:
    """Create the researcher agent that fuses structured and unstructured sources for financial data."""
    
    agent_tools = list(tools or []) + get_default_toolkit()
    
    return Agent(
        name="Market Researcher",
        role="Curate authoritative, current financial data and news for a specific stock ticker.",
        goal="Produce a raw, factual report containing current stock data, key financial figures, and recent market drivers.",
        backstory=(
            "You are a meticulous investigator, specializing in extracting and combining knowledge "
            "from diverse sources—historical documentation and the open web. Your reports are the "
            "foundation of the investment brief, known for their timeliness and accuracy."
        ),
        llm=build_crewai_llm(**(llm_overrides or {})),
        allow_delegation=False,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        tools=agent_tools,
    )