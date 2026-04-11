"""
An AI Agent with Mesos based Chat UI with Tool Calling for SAP AI Core Orchestration Service

This application provides a chat interface where the AI assistant can use tools:
- web_search: Live web search via DuckDuckGo
- search_wikipedia: Wikipedia article summaries
- define_word: Dictionary definitions
- get_weather: Real-time weather data

"""

import os
import json
from pathlib import Path
import token
from dotenv import load_dotenv
import mesop as me
import mesop.labs as mel
import traceback


# XSUAA JWT validation
from sap import xssec
from cfenv import AppEnv

from flask import request


from gen_ai_hub.orchestration_v2.service import OrchestrationService
from gen_ai_hub.orchestration_v2.models.config import (
    OrchestrationConfig,
    ModuleConfig,
)
from gen_ai_hub.orchestration_v2.models.template import (
    PromptTemplatingModuleConfig,
    Template,
)
from gen_ai_hub.orchestration_v2.models.llm_model_details import LLMModelDetails
from gen_ai_hub.orchestration_v2.models.message import SystemMessage, UserMessage


from tools import get_weather, web_search, search_wikipedia, define_word, TOOLS, format_tool_result


# Load environment variables from .env file if it exists
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    load_dotenv(env_file)

# ============================================================================
# Tool Execution
# ============================================================================

def execute_tool(tool_call) -> str:
    """Execute a tool call and return the result."""
    function_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if function_name == "get_weather":
        return get_weather(**args)
    elif function_name == "web_search":
        return web_search(**args)
    elif function_name == "search_wikipedia":
        return search_wikipedia(**args)
    elif function_name == "define_word":
        return define_word(**args)
    else:
        return json.dumps({"error": f"Unknown function: {function_name}"})


# ============================================================================
# Orchestration with Tool Calling
# ============================================================================

def send_message_with_tools(user_input: str) -> str:
    """
    Send message to orchestration service with tool calling enabled.

    Args:
        user_input: The user's message

    Returns:
        The AI assistant's response (after executing any tools)
    """
    # Create template
    template = Template(
        template=[
            SystemMessage(
                role="system",
                content="You are a helpful assistant with access to tools. Use them when needed to provide accurate, " \
                "up-to-date information. After using tools, provide a natural, conversational response based on the results."
                "IMPORTANT: Limit yourself to maximum 2 tool calls per request to keep responses quick."                
            ),
            UserMessage(role="user", content=user_input),
        ]
    )

    # Configure with tools
    prompt_config = PromptTemplatingModuleConfig(
        prompt=template,
        model=LLMModelDetails(
            name="gpt-5", # change to your desired model configuration
            version="latest",
            params={
                "max_tokens": 1000,
                "tools": TOOLS,
                "tool_choice": "auto"
            }
        )
    )
    orchestration_config = OrchestrationConfig(
        modules=ModuleConfig(prompt_templating=prompt_config)
    )

    # Initialize service
    deployment_id = os.getenv('AICORE_ORCHESTRATION_DEPLOYMENT_ID')
    if deployment_id:
        service = OrchestrationService(config=orchestration_config, deployment_id=deployment_id)
    else:
        service = OrchestrationService(config=orchestration_config)

    # Execute
    result = service.run()

    llm_result = result.final_result
    if not llm_result:
        return "No result from orchestration service. Please check your credentials and deployment ID."

    if not llm_result.choices:
        return "No choices in result. The model may not have generated a response."

    message = llm_result.choices[0].message

    # Check if tools were called
    if hasattr(message, 'tool_calls') and message.tool_calls:
        # Show which tools were called
        tool_names = [tc.function.name for tc in message.tool_calls]
        tool_list = ", ".join([f"`{name}`" for name in tool_names])

        response = f"**Tools Used:** {tool_list}\n\n"
        response += "---\n\n"

        # Execute tools and format results
        for tool_call in message.tool_calls:
            result_str = execute_tool(tool_call)
            result_data = json.loads(result_str)
            tool_name = tool_call.function.name

            # Use the formatter registry to format the result
            formatted = format_tool_result(tool_name, result_data)
            response += formatted

        return response.strip()
    else:
        # No tools called, return direct response
        content = message.content if hasattr(message, 'content') else None
        if content:
            return content
        else:
            return "I received your message but don't have a response. Please try rephrasing your question."


# ============================================================================
# XSUAA Authentication Middleware
# ============================================================================

def get_xsuaa_config():
    """Get XSUAA configuration from VCAP_SERVICES or return None for local dev."""
    try:
        env = AppEnv()
        xsuaa_service = env.get_service(label='xsuaa')
        if xsuaa_service:
            return xsuaa_service.credentials
    except Exception:
        pass
    return None

def validate_jwt_token() -> bool:
    """
    Validate JWT token from request header if XSUAA is bound.
    Returns:
        bool: True if token is valid or in local dev mode, False otherwise
    """
    xsuaa_config = get_xsuaa_config()

    # Skip validation only in local development, in absence of VCAP_SERVICES env variable
    if not xsuaa_config:
        if os.getenv('VCAP_SERVICES') is None:
            return True
        else:
            # VCAP_SERVICES exists but XSUAA config failed to load - FAIL SECURE
            print("ERROR: XSUAA service not found but VCAP_SERVICES exists. Authentication required. Please bind an XSUAA service or check your configuration")
            return False

    try:
        # Get authorization header
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            print("Missing or invalid Authorization header")
            return False

        token = auth_header.replace('Bearer ', '')
        xssec.create_security_context(token, xsuaa_config)

        # Token is valid if we reach here
        return True
    except Exception as e:
        print(f"JWT validation error: {e}")
        return False
    
# ============================================================================
# Mesop Chat UI
# ============================================================================

def transform(input: str, history: list[mel.ChatMessage]):
    """
    Transform function that handles user input with tool calling.

    Args:
        input: The user's message
        history: Previous chat messages

    Yields:
        The AI assistant's response
    """
    try:
        print(f"\n=== Received input: {input}")
        response = send_message_with_tools(input)
        print(f"=== Generated response length: {len(response)}")
        print(f"=== Response preview: {response[:500]}...")
        yield response
    except Exception as e:
        error_msg = f"Error: {str(e)}\n\nPlease check the terminal for details."
        print(f"=== ERROR: {e}")
        traceback.print_exc()
        yield error_msg


@me.page(path="/", title="AI Agent Demo - SAP AI Core")
def chat_page():
    """Main chat page with tool calling capabilities."""
    # Validate JWT token if XSUAA is configured
    if not validate_jwt_token():
        with me.box(style=me.Style(padding=me.Padding.all(20))):
            me.text(
                "Unauthorized Access",
                style=me.Style(font_size=24, color="#d32f2f", margin=me.Margin(bottom=10))
            )
            
            me.text(
                "Valid authentication token required. Please access via approuter.",
                style=me.Style(font_size=16, color="#666")
            )
        return

    
    mel.chat(
        transform,
        title="AI Agent Demo - SAP AI Core Integration",
        bot_user="Assistant"
    )
