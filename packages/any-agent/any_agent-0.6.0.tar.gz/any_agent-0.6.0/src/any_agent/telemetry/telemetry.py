from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar

from any_agent import AgentFramework
from any_agent.logging import logger

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


class TelemetryProcessor(ABC):
    """Base class for processing telemetry data from different agent types."""

    MAX_EVIDENCE_LENGTH: ClassVar[int] = 400

    @classmethod
    def create(cls, agent_framework: AgentFramework) -> TelemetryProcessor:
        """Factory method to create the appropriate telemetry processor."""
        if agent_framework == AgentFramework.LANGCHAIN:
            from any_agent.telemetry.langchain_telemetry import (
                LangchainTelemetryProcessor,
            )

            return LangchainTelemetryProcessor()
        if agent_framework == AgentFramework.SMOLAGENTS:
            from any_agent.telemetry.smolagents_telemetry import (
                SmolagentsTelemetryProcessor,
            )

            return SmolagentsTelemetryProcessor()
        if agent_framework == AgentFramework.OPENAI:
            from any_agent.telemetry.openai_telemetry import (
                OpenAITelemetryProcessor,
            )

            return OpenAITelemetryProcessor()
        if agent_framework == AgentFramework.LLAMAINDEX:
            from any_agent.telemetry.llama_index_telemetry import (
                LlamaIndexTelemetryProcessor,
            )

            return LlamaIndexTelemetryProcessor()
        msg = f"Unsupported agent type {agent_framework}"
        raise ValueError(msg)

    @staticmethod
    def determine_agent_framework(trace: Sequence[Mapping[str, Any]]) -> AgentFramework:
        """Determine the agent type based on the trace.
        These are not really stable ways to find it, because we're waiting on some
        reliable method for determining the agent type. This is a temporary solution.
        """
        for span in trace:
            if "langchain" in span.get("attributes", {}).get("input.value", ""):
                logger.info("Agent type is LANGCHAIN")
                return AgentFramework.LANGCHAIN
            if span.get("attributes", {}).get("smolagents.max_steps"):
                logger.info("Agent type is SMOLAGENTS")
                return AgentFramework.SMOLAGENTS
            # This is extremely fragile but there currently isn't
            # any specific key to indicate the agent type
            if span.get("name") == "response":
                logger.info("Agent type is OPENAI")
                return AgentFramework.OPENAI
        msg = "Could not determine agent type from trace, or agent type not supported"
        raise ValueError(msg)

    @abstractmethod
    def extract_hypothesis_answer(self, trace: Sequence[Mapping[str, Any]]) -> str:
        """Extract the hypothesis agent final answer from the trace."""

    @abstractmethod
    def _extract_telemetry_data(
        self,
        telemetry: Sequence[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        """Extract the agent-specific data from telemetry."""

    @abstractmethod
    def extract_interaction(
        self,
        span: Mapping[str, Any],
    ) -> tuple[str, dict[str, Any]]:
        """Extract interaction details from a span."""

    def extract_evidence(self, telemetry: Sequence[Mapping[str, Any]]) -> str:
        """Extract relevant telemetry evidence."""
        calls = self._extract_telemetry_data(telemetry)
        return self._format_evidence(calls)

    def _format_evidence(self, calls: Sequence[Mapping[str, Any]]) -> str:
        """Format extracted data into a standardized output format."""
        evidence = f"## {self._get_agent_framework().name} Agent Execution\n\n"

        for idx, call in enumerate(calls, start=1):
            evidence += f"### Call {idx}\n"

            # Truncate any values that are too long
            call = {
                k: (
                    v[: self.MAX_EVIDENCE_LENGTH] + "..."
                    if isinstance(v, str) and len(v) > self.MAX_EVIDENCE_LENGTH
                    else v
                )
                for k, v in call.items()
            }

            # Use ensure_ascii=False to prevent escaping Unicode characters
            evidence += json.dumps(call, indent=2, ensure_ascii=False) + "\n\n"

        return evidence

    @abstractmethod
    def _get_agent_framework(self) -> AgentFramework:
        """Get the agent type associated with this processor."""

    @staticmethod
    def parse_generic_key_value_string(text: str) -> dict[str, str]:
        """
        Parse a string that has items of a dict with key-value pairs separated by '='.
        Only splits on '=' signs, handling quoted strings properly.
        """
        pattern = r"(\w+)=('.*?'|\".*?\"|[^'\"=]*?)(?=\s+\w+=|\s*$)"
        result = {}

        matches = re.findall(pattern, text)
        for key, value in matches:
            # Clean up the key
            key = key.strip()

            # Clean up the value - remove surrounding quotes if present
            if (value.startswith("'") and value.endswith("'")) or (
                value.startswith('"') and value.endswith('"')
            ):
                value = value[1:-1]

            # Store in result dictionary
            result[key] = value

        return result
