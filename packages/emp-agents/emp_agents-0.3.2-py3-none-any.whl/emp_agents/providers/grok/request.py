from typing import Optional

from pydantic import Field

from emp_agents.models.shared.tools import GenericTool
from emp_agents.providers.standard_request import StandardRequest

from .types import GrokModelType


class Request(StandardRequest[GrokModelType]):
    """
    Request model for Grok API, which follows the OpenAI API format.
    """

    tools: Optional[list[GenericTool]] = Field(default=None)
