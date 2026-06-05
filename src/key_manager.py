# src/key_manager.py
import os

from dotenv import load_dotenv

load_dotenv()


def get_api_key(service):
    env_map = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
    return os.getenv(env_map.get(service, ""), "fake-key")
