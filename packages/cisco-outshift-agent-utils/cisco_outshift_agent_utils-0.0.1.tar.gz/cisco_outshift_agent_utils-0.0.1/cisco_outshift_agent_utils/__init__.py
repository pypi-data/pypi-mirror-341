"""Light‑weight, provider‑agnostic LLM factory.

Usage
-----
from llm_factory import LLMFactory

llm = LLMFactory("gpt-4o-mini").get_llm_connection()
"""

from .factory import LLMFactory, get_llm_connection_with_tools

__all__ = ["LLMFactory", "get_llm_connection_with_tools"]
