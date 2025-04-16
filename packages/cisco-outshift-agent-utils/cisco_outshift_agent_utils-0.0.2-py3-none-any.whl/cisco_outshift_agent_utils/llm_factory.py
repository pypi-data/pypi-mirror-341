# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""Light‑weight, provider‑agnostic Large‑Language‑Model (LLM) factory.

The factory hides the provider‑specific details required to instantiate a
LangChain‑compatible chat model. It supports Azure OpenAI, OpenAI public
cloud, and Anthropic Claude models. All configuration is driven via
environment variables so the same code can be re‑used across local
workstations, CI pipelines, or containerised runtimes without code
changes.

Environment variables
---------------------
Azure OpenAI
^^^^^^^^^^^^
* ``AZURE_OPENAI_ENDPOINT`` – Endpoint URL of your Azure OpenAI resource.
* ``AZURE_OPENAI_DEPLOYMENT`` – Name of the model deployment to invoke.
* ``AZURE_OPENAI_API_KEY`` – API key for the resource.
* ``AZURE_OPENAI_API_VERSION`` – REST API version to use.

OpenAI public cloud
^^^^^^^^^^^^^^^^^^^
* ``OPENAI_API_KEY`` – Your OpenAI API key.
* ``OPENAI_ENDPOINT`` – Optional custom base URL (defaults to
  ``https://api.openai.com/v1``).
* ``OPENAI_MODEL_NAME`` – Optional model name (defaults to
  ``gpt-4o-mini``).

Anthropic Claude
^^^^^^^^^^^^^^^^
* ``ANTHROPIC_API_KEY`` – Your Anthropic API key.
* ``ANTHROPIC_MODEL_NAME`` – Optional model name (defaults to
  ``claude-3-sonnet-20240229``).
"""

from __future__ import annotations

import logging
import os
from typing import Any, Iterable

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic


class LLMFactory:
  """Factory that returns a *ready‑to‑use* LangChain chat model.

  Parameters
  ----------
  provider : {"azure", "openai", "anthropic"}
      Which LLM backend to use.
  """

  SUPPORTED_PROVIDERS = {"azure", "openai", "anthropic"}

  # ------------------------------------------------------------------ #
  # Construction helpers
  # ------------------------------------------------------------------ #

  def __init__(self, provider: str | None = None) -> None:
    if not provider:
      raise ValueError("Provider must be specified (azure | openai | anthropic)")

    self.provider = provider.lower()
    if self.provider not in self.SUPPORTED_PROVIDERS:
      raise ValueError(f"Unsupported provider: {self.provider}")

  # ------------------------------------------------------------------ #
  # Public helpers
  # ------------------------------------------------------------------ #

  def get_llm(
    self,
    response_format: str | dict | None = None,
    tools: Iterable[Any] | None = None,
    strict_tools: bool = True,
    temperature: float | None = None,
    **kwargs,
  ):
    """Return a LangChain chat model, optionally bound to *tools*.

    The returned object is an instance of ``ChatOpenAI``,
    ``AzureChatOpenAI`` or ``ChatAnthropic`` depending on the selected
    *provider*.
    """

    builder = getattr(self, f"_build_{self.provider}_llm")
    llm = builder(response_format, temperature, **kwargs)
    return llm.bind_tools(tools, strict=strict_tools) if tools else llm

  # ------------------------------------------------------------------ #
  # Internal builders (one per provider)
  # ------------------------------------------------------------------ #

  def _build_azure_llm(
    self,
    response_format: str | dict | None,
    temperature: float | None,
    **kwargs,
  ):
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if not all([deployment, api_version, endpoint, api_key]):
      raise EnvironmentError(
        "Missing one or more Azure OpenAI environment variables "
        "(AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, "
        "AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION)."
      )

    logging.info(
      f"[LLM] AzureOpenAI deployment={deployment} api_version={api_version}"
    )

    model_kwargs = {"response_format": response_format} if response_format else {}
    return AzureChatOpenAI(
      azure_endpoint=endpoint,
      azure_deployment=deployment,
      openai_api_key=api_key,
      api_version=api_version,
      temperature=temperature if temperature is not None else 0,
      max_tokens=None,
      timeout=None,
      max_retries=5,
      model_kwargs=model_kwargs,
      **kwargs,
    )

  def _build_openai_llm(
    self,
    response_format: str | dict | None,
    temperature: float | None,
    **kwargs,
  ):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1")
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

    if not api_key:
      raise EnvironmentError("OPENAI_API_KEY environment variable is required")

    logging.info(f"[LLM] OpenAI model={model_name} endpoint={base_url}")

    model_kwargs = {"response_format": response_format} if response_format else {}
    return ChatOpenAI(
      model_name=model_name,
      api_key=api_key,
      base_url=base_url,
      temperature=temperature if temperature is not None else 0,
      model_kwargs=model_kwargs,
      **kwargs,
    )

  def _build_anthropic_llm(
    self,
    response_format: str | dict | None,
    temperature: float | None,
    **kwargs,
  ):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model_name = os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-sonnet-20240229")

    if not api_key:
      raise EnvironmentError("ANTHROPIC_API_KEY environment variable is required")

    logging.info(f"[LLM] Anthropic model={model_name}")

    model_kwargs = {"response_format": response_format} if response_format else {}
    return ChatAnthropic(
      model_name=model_name,
      anthropic_api_key=api_key,
      temperature=temperature if temperature is not None else 0,
      max_tokens=None,
      timeout=None,
      model_kwargs=model_kwargs,
      **kwargs,
    )