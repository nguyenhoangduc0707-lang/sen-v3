"""Minimal xAI SDK smoke test.

Requires XAI_API_KEY in the environment or .env. Do not paste keys into this
file.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user


load_dotenv()


def main() -> None:
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise SystemExit("XAI_API_KEY is not set")

    client = Client(api_key=api_key, timeout=3600)
    chat = client.chat.create(model=os.getenv("XAI_MODEL", "grok-3-mini"))
    chat.append(user("Hello, are you working?"))
    response = chat.sample()
    print(response)


if __name__ == "__main__":
    main()
