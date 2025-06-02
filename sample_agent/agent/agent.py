import random

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types


root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='restaurant_agent',
    description=(
        'Agent that can find nearby restaurants'
    ),
    instruction="""
      You are a helpful agent that can help users find nearby restaurants.
      When user asks you to find reservation, ask user's address.
      If the user provides the address directly, then use that address directly.
      Then use address_to_geocode to convert the address to a geo code which contains longtitude and latitude.
      Then call get_nearby_restaurants with the longtitude and latitude provided by the user.
      Read the result and give user a bullet point list in markdown.
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='uv',
                args=[
                    "--directory",
                    "../mcp_server",
                    "run",
                    "nearby_restaurants.py"
                ],
            ),
        )
    ],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
