"""
Type definitions for agents and agent configurations.
"""

import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import List

# Forward imports to avoid circular dependencies
from mcp_agent.core.request_params import RequestParams


class AgentType(Enum):
    """Enumeration of supported agent types."""

    BASIC = "agent"
    ORCHESTRATOR = "orchestrator"
    PARALLEL = "parallel"
    EVALUATOR_OPTIMIZER = "evaluator_optimizer"
    ROUTER = "router"
    CHAIN = "chain"


@dataclass
class AgentConfig:
    """Configuration for an Agent instance"""

    name: str
    instruction: str = "You are a helpful agent."
    servers: List[str] = dataclasses.field(default_factory=list)
    model: str | None = None
    use_history: bool = True
    default_request_params: RequestParams | None = None
    human_input: bool = False
    agent_type: str = AgentType.BASIC.value

    def __post_init__(self) -> None:
        """Ensure default_request_params exists with proper history setting"""

        if self.default_request_params is None:
            self.default_request_params = RequestParams(
                use_history=self.use_history, systemPrompt=self.instruction
            )
        else:
            # Override the request params history setting if explicitly configured
            self.default_request_params.use_history = self.use_history
