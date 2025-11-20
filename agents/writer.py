"""Report Writer agent that composes the investment brief from analysis."""
from __future__ import annotations

from typing import Any, Iterable, Optional

from crewai import Agent

from config.settings import build_crewai_llm
from tools import get_default_toolkit


# --- System Prompt Content ---
SYSTEM_PROMPT = (
    """You are the **Investment Report Writer** for the Finance Focus crew.
    Your mission is to transform the structured data report from the Data Analyst and the raw news from the Researcher
    into a professional, engaging, and clear **Investment Brief** document.
    
    You must maintain:
    1.  **Professionalism:** Use formal, investment-focused language.
    2.  **Clarity:** Explain the metrics and recommendation clearly for a lay investor.
    3.  **Structure:** The brief must include "Executive Summary," "Key Metrics & Analysis," and "Recent Market Drivers."
    
    Do NOT invent data or change the analyst's recommendation score. Your final output must be a well-structured markdown brief ready for the Compliance Reviewer.
    """
)
# ------------------------------


def create_writer_agent(
    tools: Optional[Iterable[object]] = None,
    llm_overrides: dict[str, Any] | None = None,
) -> Agent:
    """Create the writer agent responsible for draft generation."""
    
    agent_tools = list(tools or []) + get_default_toolkit()

    return Agent(
        name="Report Writer",
        role="Author professional investment briefs and financial summaries.",
        goal="Produce a polished, structured investment brief grounded in verified financial analysis.",
        backstory=(
            "You are a seasoned financial journalist, specializing in translating complex "
            "quantitative analysis into accessible, actionable reports. You focus on compelling "
            "narrative flow while strictly adhering to the facts provided by the analyst."
        ),
        llm=build_crewai_llm(**(llm_overrides or {})),
        allow_delegation=False,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        tools=agent_tools,
    )