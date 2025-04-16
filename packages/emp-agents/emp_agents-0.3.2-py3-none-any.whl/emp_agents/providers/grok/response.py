from emp_agents.providers.openai.response import Response as OpenAIResponse

from .types import GrokModelType


class Response(OpenAIResponse):
    model: GrokModelType | str
