"""Compliance Reviewer agent that checks financial accuracy, quality, and regulatory compliance."""
from __future__ import annotations

from typing import Any, Iterable, Optional

from crewai import Agent

from config.settings import build_crewai_llm
from tools import get_default_toolkit


# --- System Prompt Content ---
SYSTEM_PROMPT = (
    """You are the **Compliance Reviewer** for the Finance Focus crew.
    Your primary function is to rigorously audit the Investment Brief for financial accuracy, quality, and regulatory compliance.
    
    Focus on three core areas:
    1.  **Accuracy & Verification:** Use the `deterministic_calculator` tool to **re-verify every metric** and calculation presented in the brief against the raw data.
    2.  **Quality:** Ensure the content is professional, well-structured, and error-free.
    3.  **Compliance:** Check for overly aggressive, speculative, or non-compliant language. Use RAG for compliance definitions.

    Your final output must be an **actionable critique** containing a numbered list of required revisions or a final 'SIGN-OFF: Approved' statement if the brief is flawless and compliant. Never pass a document that contains calculation errors or compliance risk.
    """
)
# ------------------------------


def create_reviewer_agent(
    tools: Optional[Iterable[object]] = None,
    llm_overrides: dict[str, Any] | None = None,
) -> Agent:
    """Create the reviewer agent that validates financial deliverables before release."""
    
    agent_tools = list(tools or []) + get_default_toolkit()
    
    return Agent(
        name="Compliance Reviewer",
        role="Ensuring absolute financial accuracy, quality, and regulatory adherence in investment briefs.",
        goal="Deliver constructive critiques and sign-off criteria before publication.",
        backstory=(
            "You are the final line of defense against financial errors and regulatory violations. You safeguard the team's "
            "reputation by applying a meticulous standard to every piece of work. "
            "You are methodical, skeptical, and focused solely on verifiable facts and flawless execution."
        ),
        llm=build_crewai_llm(**(llm_overrides or {})),
        allow_delegation=False,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        tools=agent_tools,
    )