"""The one place we call Gemma. Python looks up the numbers; Gemma only writes."""

import json
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.prompts import FACTS, SYSTEM_PROMPT

MODEL = "gemma-4-26b-a4b-it"
LOCAL_MODEL = "gemma4"
LOCAL_URL = "http://localhost:11434/v1/chat/completions"
BUSY_MESSAGE = "First Call is busy right now. Please wait a moment and try again."
LOCAL_DOWN_MESSAGE = "Offline mode needs Ollama running on this computer with the gemma4 model."

REGIONS_CSV = Path(__file__).resolve().parent.parent / "data" / "sa_regions.csv"

load_dotenv()                      # reads GEMINI_API_KEY from .env
_client = None
_cache = {}


def load_regions():
    return pd.read_csv(REGIONS_CSV)


def build_content(description, region_row):
    """Instructions + facts + one region's numbers + the family's words, as one string.

    Gemma on the Gemini API may reject system_instruction, so we prepend instead.
    """
    regions = load_regions()
    region = {k: (v.item() if hasattr(v, "item") else v) for k, v in dict(region_row).items()}
    region["sa_min_pct_lives_alone"] = float(regions["pct_lives_alone"].min())
    region["sa_max_pct_lives_alone"] = float(regions["pct_lives_alone"].max())
    return (
        f"{SYSTEM_PROMPT}\n{FACTS}\n"
        f"REGION_DATA: {json.dumps(region)}\n\n"
        f"DESCRIPTION: {description.strip()}"
    )


def ask(description, region_row):
    """Return Gemma's Markdown plan, or a friendly busy message if the API fails."""
    global _client
    key = (dict(region_row)["code"], description.strip())
    if key in _cache:
        return _cache[key]
    try:
        if _client is None:
            _client = genai.Client()   # picks the key up from the environment
        response = _client.models.generate_content(
            model=MODEL,
            contents=build_content(description, region_row),
            config=types.GenerateContentConfig(
                temperature=0.2,
                thinking_config=types.ThinkingConfig(thinking_level="minimal"),
            ),
        )
        answer = response.text
    except Exception:
        return BUSY_MESSAGE
    if not answer:
        return BUSY_MESSAGE
    _cache[key] = answer
    return answer


def ask_local(description, region_row):
    """Same as ask(), but uses a local Gemma through Ollama. Only works if Ollama is running."""
    try:
        response = requests.post(
            LOCAL_URL,
            json={
                "model": LOCAL_MODEL,
                "messages": [{"role": "user", "content": build_content(description, region_row)}],
                "temperature": 0.2,
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception:
        return LOCAL_DOWN_MESSAGE
