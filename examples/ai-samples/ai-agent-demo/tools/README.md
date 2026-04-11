# Tools Contribution Guide

This directory contains all the tool implementations for the chat UI.



## Architecture

### 1. Tool Functions
Each tool is a Python function that returns JSON strings.

### 2. Tool Schemas (`schemas.py`)
JSON Schema definitions that tell the LLM about available tools.

### 3. Formatters (`formatters.py`)
**Registry pattern** for scalable result formatting:
- Each tool has a dedicated formatter function
- `FORMATTERS` dict maps tool names to formatters
- `format_tool_result()` dispatches to the right formatter
- Unknown tools get a generic JSON fallback

**Benefits:**
- **Scalable**: Add new tools without modifying core logic
- **Maintainable**: Each formatter is independent
- **Testable**: Test formatters in isolation
- **Extensible**: Easy to add custom formatting

## Available Tools

### 1. Weather (`weather.py`)
### 2. Web Search (`web_search.py`)
### 3. Wikipedia (`wikipedia.py`)
### 4. Dictionary (`dictionary.py`)

## Adding a New Tool

### Step 1: Create Tool Function

Create `tools/calculator.py`:
```python
import json

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)  # Use safe_eval in production
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})
```

### Step 2: Add Schema

Add to `schemas.py`:
```python
TOOLS = [
    # ... existing tools
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]
```

### Step 3: Add Formatter

Add to `formatters.py`:
```python
def format_calculator(result_data: dict) -> str:
    """Format calculator results."""
    return f"🔢 **Result**: {result_data.get('result', 'N/A')}\n\n"

FORMATTERS = {
    # ... existing formatters
    'calculate': format_calculator,
}
```

### Step 4: Export

Update `__init__.py`:
```python
from .calculator import calculate

__all__ = [
    'calculate',  # Add here
    # ... other tools
]
```

### Step 5: Register Execution

Update `app.py` `execute_tool()`:
```python
elif function_name == "calculate":
    return calculate(**args)
```

**That's it!** The formatter registry will automatically use your new formatter.

## Error Handling

All tools return JSON strings with either:
- **Success**: `{"key": "value", ...}`
- **Error**: `{"error": "Error message"}`

The formatter automatically handles errors with a ❌ prefix.

## Testing Tools

Test individual tools:
```bash
python3 -c "from tools import get_weather; print(get_weather('Paris'))"
python3 -c "from tools import format_tool_result; from tools.formatters import *; print(format_weather({'location': 'Paris', 'temperature': 15}))"
```

## Dependencies

- `httpx` - HTTP requests (weather, dictionary)
- `ddgs` - DuckDuckGo search (optional)
- `Wikipedia-API` - Wikipedia access

All dependencies are listed in `requirements.txt`.
