from typing import Annotated, Optional

from pydantic import Field, PlainSerializer

from emp_agents.models.shared.tools import GenericTool
from emp_agents.providers.standard_request import StandardRequest

from .tool import Tool
from .types import OpenAIModelType


class Request(StandardRequest[OpenAIModelType]):
    """
    https://platform.openai.com/docs/api-reference/chat/create
    """

    tools: Annotated[
        Optional[list[GenericTool]],
        PlainSerializer(
            lambda tools_list: (
                [tool.to_openai() for tool in tools_list]
                if tools_list is not None
                else None
            ),
            return_type=Optional[list[Tool]],
        ),
    ] = Field(default=None)
