"""
Tool schemas for SAP AI Core Orchestration Service
JSON Schema definitions for all available tools
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get real-time weather for any location using Open-Meteo API (no API key needed). Returns current temperature, condition, and wind speed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country, e.g. London, UK"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information using DuckDuckGo. Use this when you need up-to-date information, news, or facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 3)",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Search Wikipedia and retrieve article summary. Use for factual information, historical data, or general knowledge.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The topic or article title to search for"
                    },
                    "sentences": {
                        "type": "integer",
                        "description": "Number of sentences in summary (default: 3)",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "define_word",
            "description": "Get dictionary definition, pronunciation, and usage examples. Use for vocabulary queries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The word to define"
                    }
                },
                "required": ["word"]
            }
        }
    }
]
