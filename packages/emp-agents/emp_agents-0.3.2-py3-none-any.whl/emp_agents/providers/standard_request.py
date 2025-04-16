from typing import Annotated, Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from emp_agents.models.shared import Message
from emp_agents.models.shared.tools import GenericTool

ModelType = TypeVar("ModelType")


class StandardRequest(BaseModel, Generic[ModelType]):
    """
    Generic request model that can be used by all platforms that mimic the OpenAI format.
    """

    model_config = ConfigDict(populate_by_name=True)

    model: ModelType
    max_tokens: Optional[int] = Field(default=None)
    temperature: Optional[float] = Field(default=None, ge=0, le=2.0)
    tool_choice: Literal["none", "required", "auto", None] = Field(default=None)

    system: str | None = None
    messages: list[Message] | None = None

    frequency_penalty: Optional[float] = Field(default=None, ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(default=None, ge=-2.0, le=2.0)
    num_responses: Optional[int] = Field(default=None, serialization_alias="n")
    top_p: Optional[int] = Field(default=None)

    def model_dump(self, *, exclude_none=True, by_alias=True, **kwargs):
        return super().model_dump(
            exclude_none=exclude_none, by_alias=by_alias, **kwargs
        )
