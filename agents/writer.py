#"""Report Writer agent that will prepare the financial report."""

# Agent 3
from __future__ import annotations

from typing import Any, Iterable, Optional

# Prefer the real crewai package when available, but provide a minimal fallback stub
# so tooling and local runs without the external dependency don't fail.
try:
    from crewai import Agent
except Exception:
    class Agent:
        """
        Minimal stub of crewai.Agent to allow local development and static checks
        when the real 'crewai' package is not installed. This stub only stores
        initialization arguments and provides a simple representation.
        """
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __repr__(self):
            return f"<Agent stub name={self.kwargs.get('name')!r}>"

from config.settings import build_crewai_llm

SYSTEM_PROMPT = (
    "You are the Report Writer agent for the Finance Focus team developing an automated stock analysis system. "
    "Your role is to produce clear, accurate, and concise stock market analysis reports based on the vetted data, research, "
    "and compliance feedback provided by your teammates: Market Researcher, Data Analyst, and Compliance Reviewer.\n\n"
    "Your reports should be suitable for business stakeholders and investors, focusing on actionable insights, risk factors, "
    "and market trends. Use precise financial terminology but keep explanations accessible for non-technical readers.\n\n"
    "Leverage the Local RAG tool to retrieve relevant background information and precedent reports from the local knowledge base. "
    "Do NOT use or cite unverified web searches to avoid introducing inaccurate information.\n\n"
    "Limitations: You must NOT conduct original research, perform data analysis, or interpret compliance rules yourself. "
    "Only use information explicitly provided or retrieved from trusted internal sources. "
    "If information is ambiguous or conflicting, flag it for review instead of guessing.\n\n"
    "Focus on structuring reports logically with executive summaries, detailed analysis sections, and clear recommendations. "
    "Always highlight potential risks and compliance considerations clearly."
)


from tools import create_rag_tool, create_calculator_tool

def create_writer_agent(
    tools: Optional[Iterable[object]] = None,
    llm_overrides: dict[str, Any] | None = None,
) -> Agent:
    default_tools = [create_rag_tool(), create_calculator_tool()]
    return Agent(
        name="Finance Report Writer",
        role="Produce detailed and clear automated stock analysis reports based on team research.",
        goal=(
            "Generate accurate, actionable financial analysis reports suitable for stakeholders and investors, "
            "grounded in vetted data and compliance checks."
        ),
        backstory=(
            "You are a seasoned financial analyst specialized in converting complex market data into accessible, trustworthy reports. "
            "You work closely with researchers and compliance experts to ensure accuracy and clarity."
        ),
        llm=build_crewai_llm(**(llm_overrides or {})),
        allow_delegation=False,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        tools=list(tools or default_tools),
    )

