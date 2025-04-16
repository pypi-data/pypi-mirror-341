import pytest

from emp_agents.agents import AgentBase
from emp_agents.models import GenericTool, Property, Request, UserMessage
from emp_agents.providers import GrokModelType, GrokProvider


class AgentForTesting(AgentBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@pytest.mark.asyncio
async def test_grok_responds():
    from emp_agents import AgentBase

    agent = AgentBase(
        provider=GrokProvider(),
        model=GrokModelType.grok_3,
    )
    response = await agent.answer("what is the weather in san francisco?")
    assert response is not None


@pytest.mark.asyncio
async def test_grok_provider():
    agent = AgentForTesting(
        provider=GrokProvider(
            api_key="test_api_key",
            default_model=GrokModelType.grok_1_5,
        ),
    )
    assert agent.provider.default_model == GrokModelType.grok_1_5
    assert agent.provider.api_key == "test_api_key"


def test_grok_provider_init():
    """Test that GrokProvider initializes correctly"""
    provider = GrokProvider(
        api_key="test_api_key",
        default_model=GrokModelType.grok_1_5,
    )
    assert provider.default_model == GrokModelType.grok_1_5
    assert provider.api_key == "test_api_key"
    assert provider.URL == "https://api.x.ai/v1/chat/completions"


def test_grok_request_formatting():
    """Test that GrokProvider formats requests correctly"""
    provider = GrokProvider(api_key="test_api_key")

    request = Request(
        model=GrokModelType.grok_1_5,
        messages=[UserMessage(content="Hello, Grok!")],
    )

    formatted_request = provider._from_request(request)

    assert formatted_request["model"] == "grok-1.5"
    assert len(formatted_request["messages"]) == 1
    assert formatted_request["messages"][0]["role"] == "user"
    assert formatted_request["messages"][0]["content"] == "Hello, Grok!"


def test_grok_with_tools():
    """Test that GrokProvider formats requests with tools correctly"""
    provider = GrokProvider(api_key="test_api_key")

    weather_tool = GenericTool(
        name="get_weather",
        description="Get the current weather in a location",
        parameters={
            "location": Property(
                type="string",
                description="The city and state, e.g. San Francisco, CA",
            ),
            "unit": Property(
                type="string",
                description="The unit of temperature, either 'celsius' or 'fahrenheit'",
                enum=["celsius", "fahrenheit"],
            ),
        },
        required=["location"],
        func=lambda **kwargs: None,
    )

    request = Request(
        model=GrokModelType.grok_1_5,
        messages=[UserMessage(content="What's the weather in San Francisco?")],
        tools=[weather_tool],
        tool_choice="auto",
    )

    formatted_request = provider._from_request(request)

    assert formatted_request["model"] == "grok-1.5"
    assert len(formatted_request["messages"]) == 1
    assert formatted_request["messages"][0]["role"] == "user"
    assert (
        formatted_request["messages"][0]["content"]
        == "What's the weather in San Francisco?"
    )
    assert "tools" in formatted_request
    assert len(formatted_request["tools"]) == 1
    assert formatted_request["tools"][0]["function"]["name"] == "get_weather"
    assert formatted_request["tool_choice"] == "auto"
