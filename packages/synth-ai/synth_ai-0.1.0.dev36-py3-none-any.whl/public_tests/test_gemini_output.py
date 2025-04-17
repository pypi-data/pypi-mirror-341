import json
import logging
from typing import List

import pytest
from pydantic import BaseModel, Field

from synth_ai.zyk import LM
from synth_ai.zyk.lms.tools.base import BaseTool

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# 1. Define the Tool Input Schema using BaseModel and Field
class CraftaxToolArgs(BaseModel):
    instance_id: str = Field(
        description="The ID of the Craftax instance to interact with"
    )
    actions_list: List[str] = Field(
        description="A sequence of actions to execute in the environment (e.g., ['up', 'left', 'do'])"
    )
    service_url: str = Field(description="The URL of the Craftax environment service")


# 2. Define the Tool class by extending BaseTool
class CraftaxTool(BaseTool):
    name: str = "interact_with_craftax"
    description: str = "Interacts with the Craftax environment by sending a sequence of actions to the service."
    arguments = CraftaxToolArgs

    async def execute(self, args: dict):
        """Mock execution function for testing"""
        logger.info(
            f"Would execute actions: {args['actions_list']} for instance {args['instance_id']}"
        )
        return {
            "observation": f"Executed actions: {args['actions_list']}",
            "reward": 1.0,
            "done": False,
            "info": {"achievements": {"collect_wood": True}},
        }


# Helper function to create a simple tool dict (without RepeatedComposite)
def create_simplified_tool():
    return {
        "name": "interact_with_craftax",
        "description": "Interacts with the Craftax environment by sending a sequence of actions to the service.",
        "parameters": {
            "type": "object",
            "properties": {
                "instance_id": {
                    "type": "string",
                    "description": "The ID of the Craftax instance to interact with",
                },
                "actions_list": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "A sequence of actions to execute in the environment",
                },
                "service_url": {
                    "type": "string",
                    "description": "The URL of the Craftax environment service",
                },
            },
            "required": ["instance_id", "actions_list", "service_url"],
        },
    }


# Define test constants
SYSTEM_MESSAGE = """You are an agent playing Craftax. Your goal is to collect resources.
You have access to a tool called `interact_with_craftax` to control the agent."""

USER_MESSAGE = """# Map
## Terrain_underneath_you
grass
## Surroundings
- Tree is 1 steps up

# Inventory
## Resources
- wood: 0

Instructions: Collect 1 wood.
Instance ID: test-instance-123
Service URL: http://localhost:8002

Make a tool call to execute actions. Do not explain what you're doing."""


@pytest.mark.asyncio
async def test_base_tool_to_json():
    """Test that a BaseTool can be serialized to JSON in OpenAI and Gemini formats"""
    tool = CraftaxTool()

    # Test that the tool can be converted to OpenAI format
    openai_format = tool.to_openai_tool()
    openai_json = json.dumps(openai_format, indent=2)
    assert "function" in openai_json
    assert "interact_with_craftax" in openai_json

    # Test that the tool can be converted to Gemini format
    gemini_format = tool.to_gemini_tool()
    gemini_json = json.dumps(gemini_format, indent=2)
    assert "parameters" in gemini_json
    assert "interact_with_craftax" in gemini_json


@pytest.mark.asyncio
async def test_simplified_gemini_tool():
    """Test that a simplified Gemini tool can be serialized to JSON"""
    simplified_tool = create_simplified_tool()
    tool_json = json.dumps(simplified_tool, indent=2)
    assert "parameters" in tool_json
    assert "interact_with_craftax" in tool_json


@pytest.mark.asyncio
async def test_direct_gemini_tool_call():
    """Test that calling Gemini with a directly formatted tool works"""
    lm = LM(
        model_name="gemini-2-flash",
        formatting_model_name="gpt-4o-mini",
        temperature=0,
        max_retries="Few",
        synth_logging=True,
    )

    # Create a direct function-only tool format
    direct_tool = [create_simplified_tool()]

    # We're expecting this to complete without errors
    response = await lm.respond_async(
        system_message=SYSTEM_MESSAGE,
        user_message=USER_MESSAGE,
        tools=direct_tool,
    )

    # Just check we got a response
    assert response is not None
    logger.info(f"Response with direct tool format: {response.raw_response}")

    # If there are tool calls, validate basic structure
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
        # Verify at least one tool call has the right structure
        assert any("function" in tc for tc in response.tool_calls)


@pytest.mark.asyncio
async def test_base_tool_gemini_call():
    """Test that calling Gemini with a BaseTool works"""
    lm = LM(
        model_name="gemini-2-flash",
        formatting_model_name="gpt-4o-mini",
        temperature=0,
        max_retries="Few",
        synth_logging=True,
    )

    # Use our properly defined BaseTool
    tool = CraftaxTool()

    # We're expecting this to complete without errors
    response = await lm.respond_async(
        system_message=SYSTEM_MESSAGE,
        user_message=USER_MESSAGE,
        tools=[tool],
    )

    # Just check we got a response
    assert response is not None
    logger.info(f"Response with BaseTool: {response.raw_response}")

    # If there are tool calls, validate basic structure
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
        # Verify at least one tool call has the right structure
        assert any("function" in tc for tc in response.tool_calls)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
