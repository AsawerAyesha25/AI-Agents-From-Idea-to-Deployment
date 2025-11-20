"""Task definitions for the Finance Focus crew."""
from __future__ import annotations

from typing import List

from crewai import Task
from tools import create_calculator_tool, create_rag_tool, create_web_search_tool # Unused imports removed


def create_research_task(agent, topic: str) -> Task:
    """Task 1: Market Research to gather raw data and news."""
    return Task(
        description=(
            f"Conduct comprehensive research on the stock ticker **{topic}**. "
            "Gather the current stock price, recent news drivers (last 7 days), and key financial figures "
            "from the latest earnings report (Revenue, EPS, and forward guidance)."
        ),
        expected_output=(
            "A raw data report containing the ticker, current price, a list of 3-5 key news headlines/summaries, "
            "and all relevant financial data points for the analyst to use."
        ),
        agent=agent,
        name="Market Research",
    )


def create_analysis_task(agent) -> Task:
    """Task 2: Data Analysis to calculate metrics and provide a score."""
    return Task(
        description=(
            "Analyze the raw data provided. Use the calculator tool to compute derived metrics like "
            "P/E ratio (if data is available), Year-over-Year (YoY) change from the 52-week high, and a "
            "formal investment recommendation score (1-10) with justification."
        ),
        expected_output=(
            "A structured report containing all calculated metrics, a clear Bullish/Bearish/Neutral stance, "
            "and the final, numerical Recommendation Score (e.g., Score: 8/10, Stance: Bullish)."
        ),
        agent=agent,
        name="Financial Data Analysis",
    )


def create_writing_task(agent) -> Task:
    """Task 3: Report Writing to author the investment brief."""
    return Task(
        description=(
            "Draft a professional Investment Brief based on the Data Analyst's structured report. "
            "The brief must include sections for 'Executive Summary', 'Key Metrics & Analysis' (using the calculated metrics), "
            "and 'Recent Market Drivers' (incorporating the researcher's news). "
            "Maintain a formal, professional tone."
        ),
        expected_output=(
            "A complete, professional Markdown-formatted Investment Brief ready for compliance review."
        ),
        agent=agent,
        name="Investment Brief Drafting",
    )


def create_review_task(agent) -> Task:
    """Task 4: Compliance Review for accuracy and adherence."""
    return Task(
        description=(
            "Review the drafted Investment Brief for accuracy, compliance risk, and quality. "
            "You MUST use the calculator tool to double-check all presented financial metrics against the initial raw data. "
            "Identify any non-compliant language (e.g., guarantees, speculation) and factual errors."
        ),
        expected_output=(
            "A review report with sections for Summary, Major Findings, Minor Suggestions, and a Final Recommendation: "
            "either 'SIGN-OFF: Approved' or an 'Actionable Critique' listing required revisions."
        ),
        agent=agent,
        name="Compliance Review",
        
    )


def build_finance_tasks(researcher, analyst, writer, reviewer, topic: str) -> List[Task]:
    """Convenience helper to create the full sequential task list for the finance crew."""
    
    # Define tasks
    t1 = create_research_task(researcher, topic)
    t2 = create_analysis_task(analyst)
    t3 = create_writing_task(writer)
    t4 = create_review_task(reviewer)
    
    # Set context (dependencies)
    t2.context = [t1]
    t3.context = [t2]
    t4.context = [t3]
    
    return [t1, t2, t3, t4]