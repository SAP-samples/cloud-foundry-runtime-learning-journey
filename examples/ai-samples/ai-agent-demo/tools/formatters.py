"""
Tool result formatters
Each tool has a formatter function that formats its results for display
"""


def format_weather(result_data: dict) -> str:
    """Format weather tool results."""
    response = f"🌤️ **Weather: {result_data.get('location', '')}**\n\n"
    response += f"Temperature: {result_data.get('temperature', '')}°{result_data.get('unit', '')[0].upper()}\n"
    response += f"Condition: {result_data.get('condition', '').title()}\n"
    if 'wind_speed' in result_data:
        response += f"Wind Speed: {result_data.get('wind_speed', '')} km/h\n"
    return response


def format_web_search(result_data: dict) -> str:
    """Format web search results."""
    response = "🔍 **Web Search Results**\n\n"
    for idx, res in enumerate(result_data.get('results', []), 1):
        response += f"**{idx}. {res['title']}**\n"
        response += f"   {res['snippet'][:150]}...\n"
        response += f"   🔗 {res['url']}\n\n"
    return response


def format_wikipedia(result_data: dict) -> str:
    """Format Wikipedia results."""
    response = f"📚 **Wikipedia: {result_data.get('title', '')}**\n\n"
    response += f"{result_data.get('summary', '')}\n\n"
    response += f"🔗 Read more: {result_data.get('url', '')}\n"
    return response


def format_dictionary(result_data: dict) -> str:
    """Format dictionary results."""
    response = f"📖 **Definition: {result_data.get('word', '')}**\n"
    if result_data.get('phonetic'):
        response += f"*{result_data.get('phonetic')}*\n\n"
    for defn in result_data.get('definitions', [])[:3]:
        response += f"**{defn['part_of_speech']}**: {defn['definition']}\n"
        if defn.get('example'):
            response += f"   *Example: {defn['example']}*\n"
        response += "\n"
    return response


# Registry mapping tool names to their formatters
FORMATTERS = {
    'get_weather': format_weather,
    'web_search': format_web_search,
    'search_wikipedia': format_wikipedia,
    'define_word': format_dictionary,
}


def format_tool_result(tool_name: str, result_data: dict) -> str:
    """
    Format a tool result for display.

    Args:
        tool_name: Name of the tool that was called
        result_data: JSON result from the tool

    Returns:
        Formatted string for display
    """
    # Check for errors first
    if "error" in result_data:
        return f"**{tool_name}**: {result_data['error']}\n\n"

    # Get the appropriate formatter
    formatter = FORMATTERS.get(tool_name)

    if formatter:
        return formatter(result_data)
    else:
        # Fallback for unknown tools - just show the JSON
        import json
        return f"**{tool_name}**:\n```json\n{json.dumps(result_data, indent=2)}\n```\n\n"
