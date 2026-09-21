"""LLM integration."""

import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
BASE_URL = os.getenv("OPENAI_BASE_URL")


def ask_ai(prompt: str) -> str:
    """Send a prompt to the LLM and return the generated text."""

    url = f"{BASE_URL}/responses"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "originator": "codex_cli_rs",
    }

    data = {
        "model": MODEL,
        "input": prompt,
        "stream": True,
        "store": False,
    }

    session = requests.Session()
    session.trust_env = False

    response = session.post(
        url,
        headers=headers,
        json=data,
        timeout=120,
        stream=True,
    )

    response.raise_for_status()

    output_text = ""

    for line in response.iter_lines(decode_unicode=False):
        if not line:
            continue

        if line.startswith(b"data: "):
            data_line = line[6:].decode("utf-8")

            if data_line == "[DONE]":
                break

            try:
                event = json.loads(data_line)

                if event.get("type") == "response.output_text.delta":
                    output_text += event.get("delta", "")

            except json.JSONDecodeError:
                continue

    return output_text

