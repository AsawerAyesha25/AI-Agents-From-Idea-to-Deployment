"""Entrypoint for running the Finance Focus pipeline end-to-end."""
from __future__ import annotations

import argparse
import logging

from dotenv import load_dotenv

from crew import run_workshop_pipeline
from config.logging_config import configure_logging # Assuming you have a logging_config file


def run_pipeline(topic: str) -> str:
    """Run the configured crew against the provided stock topic."""
    load_dotenv()
    # Assuming configure_logging() is a separate function to set up logging
    # configure_logging() 
    logging.getLogger(__name__).info("Starting Finance Focus pipeline for stock ticker: %s", topic)
    return run_workshop_pipeline(topic)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Finance Focus stock analysis crew pipeline.")
    parser.add_argument(
        "--topic",
        default="AAPL", # Defaulting to a common stock for demonstration
        help="The stock ticker (e.g., AAPL, GOOG) to analyze.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    output = run_pipeline(args.topic)
    print(output)