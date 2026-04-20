"""
Dictionary tool using Free Dictionary API (no API key required)
"""

import json


def define_word(word: str) -> str:
    """
    Get dictionary definition, pronunciation, and examples.

    Args:
        word: The word to define

    Returns:
        JSON string with word definition
    """
    try:
        import httpx

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()

        data = response.json()
        if not data:
            return json.dumps({"error": f"No definition found for '{word}'"})

        entry = data[0]
        meanings = entry.get("meanings", [])

        definitions = []
        for meaning in meanings[:2]:
            part_of_speech = meaning.get("partOfSpeech", "")
            defs = meaning.get("definitions", [])
            for d in defs[:2]:
                definitions.append({
                    "part_of_speech": part_of_speech,
                    "definition": d.get("definition", ""),
                    "example": d.get("example", "")
                })

        return json.dumps({
            "word": word,
            "phonetic": entry.get("phonetic", ""),
            "definitions": definitions
        })
    except Exception as e:
        return json.dumps({"error": f"Dictionary lookup failed: {str(e)}"})
