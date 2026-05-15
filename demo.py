"""OpenRouter quickstart demo using the OpenAI SDK.

Showcases three things:
  1) A simple chat completion via OpenRouter
  2) Swapping models with a single string change
  3) A streaming response
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    sys.exit("OPENROUTER_API_KEY not set. Add it to .env or export it.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Optional OpenRouter headers for app attribution / leaderboards.
extra_headers = {
    "HTTP-Referer": "https://example.local/openrouter-demo",
    "X-Title": "OpenRouter Quickstart Demo",
}

PROMPT = "In one sentence, why is OpenRouter useful for developers?"


def basic_completion(model: str) -> None:
    print(f"\n--- Basic completion ({model}) ---")
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT}],
        extra_headers=extra_headers,
    )
    print(resp.choices[0].message.content.strip())


def streaming_completion(model: str) -> None:
    print(f"\n--- Streaming ({model}) ---")
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Count from 1 to 5, one number per line."}],
        stream=True,
        extra_headers=extra_headers,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()


if __name__ == "__main__":
    # Two different providers, same API — that's the OpenRouter pitch.
    basic_completion("openai/gpt-4o-mini")
    basic_completion("anthropic/claude-3.5-haiku")
    streaming_completion("openai/gpt-4o-mini")
