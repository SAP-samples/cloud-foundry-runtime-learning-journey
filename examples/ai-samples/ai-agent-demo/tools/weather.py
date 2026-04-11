"""
Weather tool using Open-Meteo API (no API key required)
"""

import json


def get_weather(location: str, unit: str = "celsius") -> str:
    """Get real weather for a location using Open-Meteo API (no API key needed)."""
    try:
        import httpx

        # Step 1: Geocode location to get coordinates
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_response = httpx.get(geocoding_url, timeout=10.0)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return json.dumps({"error": f"Location '{location}' not found"})

        result = geo_data["results"][0]
        lat = result["latitude"]
        lon = result["longitude"]
        location_name = result["name"]
        country = result.get("country", "")

        # Step 2: Get current weather
        temp_unit = "celsius" if unit == "celsius" else "fahrenheit"
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit={temp_unit}"

        weather_response = httpx.get(weather_url, timeout=10.0)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current_weather"]

        # Step 3: Map WMO weather code to readable condition
        weather_code = current["weathercode"]
        condition = map_weather_code(weather_code)

        return json.dumps({
            "location": f"{location_name}, {country}",
            "temperature": round(current["temperature"], 1),
            "unit": unit,
            "condition": condition,
            "wind_speed": round(current["windspeed"], 1)
        })

    except httpx.HTTPError as e:
        return json.dumps({"error": f"Weather API error: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Weather fetch failed: {str(e)}"})


def map_weather_code(code: int) -> str:
    """Map WMO weather code to human-readable condition."""
    if code == 0:
        return "Clear sky"
    elif code in [1, 2, 3]:
        return "Partly cloudy"
    elif code in [45, 48]:
        return "Foggy"
    elif code in [51, 53, 55]:
        return "Drizzle"
    elif code in [56, 57]:
        return "Freezing drizzle"
    elif code in [61, 63, 65]:
        return "Rain"
    elif code in [66, 67]:
        return "Freezing rain"
    elif code in [71, 73, 75]:
        return "Snow"
    elif code == 77:
        return "Snow grains"
    elif code in [80, 81, 82]:
        return "Rain showers"
    elif code in [85, 86]:
        return "Snow showers"
    elif code == 95:
        return "Thunderstorm"
    elif code in [96, 99]:
        return "Thunderstorm with hail"
    else:
        return "Unknown"
