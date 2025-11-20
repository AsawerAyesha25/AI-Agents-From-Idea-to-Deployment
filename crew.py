"""Orchestration file to build and run the Finance Focus Crew."""
from __future__ import annotations

import logging

from crewai import Crew, Process

# Import agent factories (Planner is Analyst, Researcher is Market Researcher, etc.)
from agents.planner import create_planner_agent # Analyst
from agents.researcher import create_researcher_agent # Market Researcher
from agents.writer import create_writer_agent # Report Writer
from agents.reviewer import create_reviewer_agent # Compliance Reviewer

from tasks import build_finance_tasks

_logger = logging.getLogger(__name__)


def run_workshop_pipeline(topic: str) -> str:
    """Instantiate agents and tasks and kick off the crew workflow."""
    
    # 1. Instantiate Agents (using the factories)
    researcher = create_researcher_agent()
    analyst = create_planner_agent() # Renamed to Analyst internally
    writer = create_writer_agent()
    reviewer = create_reviewer_agent()
    
    # 2. Define the sequential Tasks
    tasks = build_finance_tasks(
        researcher=researcher,
        analyst=analyst,
        writer=writer,
        reviewer=reviewer,
        topic=topic
    )
    
    # 3. Create the Crew
    finance_crew = Crew(
        agents=[researcher, analyst, writer, reviewer],
        tasks=tasks,
        process=Process.sequential, # Sequential process ensures task dependency order
        verbose=True, # High verbosity to see all tool usage and thought process
        manager_llm=None, # Use the default LLM setting or define a manager LLM if using hierarchical
    )
    
    _logger.info("Crew initialized. Kicking off workflow for topic: %s", topic)
    
    # 4. Kick off the workflow
    result = finance_crew.kickoff()
    
    return result


if __name__ == "__main__":
    # Example usage:
    TICKER = "TSLA"
    final_output = run_workshop_pipeline(TICKER)
    print("\n\n#####################################################")
    print(f"## FINAL INVESTMENT BRIEF AND REVIEW FOR {TICKER}:")
    print("#####################################################")
    print(final_output)