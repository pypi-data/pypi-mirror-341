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

from __future__ import annotations

import os
import logging
from typing import Any, Iterable

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic


class LLMFactory:
  """
  Light‑weight, provider‑agnostic LLM factory.

  Parameters
  ----------
  model_name : str
      The model identifier you want to use (e.g. ``gpt-4o-mini`` or
      ``claude-3-sonnet-20240229``).
  provider : str | None, default ``None``
      One of ``'azure'``, ``'openai'``, or ``'anthropic'``.
      When *None*, the ``LLM_PROVIDER`` env‑var is consulted
      (default ``'azure'``).
  """

  SUPPORTED_PROVIDERS = {"azure", "openai", "anthropic"}

  def __init__(self, model_name: str, provider: str | None = None) -> None:
    self.model_name = model_name
    self.provider = (provider or os.getenv("LLM_PROVIDER", "azure")).lower()

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
    """Return a LangChain chat model, optionally bound to tools."""
    builder = getattr(self, f"_build_{self.provider}_llm")
    llm = builder(response_format, temperature, **kwargs)
    return llm.bind_tools(tools, strict=strict_tools) if tools else llm

  # ------------------------------------------------------------------ #
  # Internal builders
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
        "Missing one or more Azure OpenAI env‑vars "
        f"for model '{self.model_name}'."
      )

    logging.info(
      f"[LLM] AzureOpenAI  model={self.model_name} "
      f"deployment={deployment} api_version={api_version}"
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
      model_kwargs=model_kwargs
    )

  def _build_openai_llm(
    self,
    response_format: str | dict | None,
    temperature: float | None,
    **kwargs,
  ):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1")

    if not api_key:
      raise EnvironmentError("OPENAI_API_KEY env‑var is required for OpenAI provider")

    logging.info(f"[LLM] OpenAI model={self.model_name} endpoint={base_url}")

    model_kwargs = {"response_format": response_format} if response_format else {}
    return ChatOpenAI(
      model_name=self.model_name,
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
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY env‑var is required for Anthropic provider")

    logging.info(f"[LLM] Anthropic model={self.model_name}")

    model_kwargs = {"response_format": response_format} if response_format else {}
    return ChatAnthropic(
      model_name=self.model_name,
      anthropic_api_key=api_key,
      temperature=temperature if temperature is not None else 0,
      max_tokens=None,
      timeout=None,
      model_kwargs=model_kwargs,
      **kwargs,
    )
