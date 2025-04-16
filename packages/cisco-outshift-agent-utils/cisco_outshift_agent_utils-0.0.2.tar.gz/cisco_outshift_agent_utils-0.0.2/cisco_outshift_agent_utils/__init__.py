"""
Utilities for managing connections to Large Language Models (LLMs).

Includes a factory class for creating LLM connections, utility functions,
and logging configuration.

Classes:
- LLMFactory: Creates LLM connections.

Functions:
- get_llm: Retrieves an LLM connection with tools.
- configure_logging: Sets up application logging.
- get_logger: Retrieves a logger instance.

Usage:
from llm_factory import LLMFactory
llm = LLMFactory("azure").get_llm()
"""
from .llm_factory import LLMFactory
from .logging_config import configure_logging, get_logger

__all__ = ["LLMFactory", "configure_logging", "get_logger"]
