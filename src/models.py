import os
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from openai import OpenAI


@dataclass(frozen=True)
class Provider:
    base_url: str | None
    name: str
    env_var: str
    is_free: bool
    model: str


PROVIDERS = [
    Provider(name="Groq", env_var="GROQ_API_KEY", is_free=True,
             base_url="https://api.groq.com/openai/v1", model="openai/gpt-oss-120b"),
    Provider(name="OpenAI", env_var="OPEN_API_KEY", is_free=False, base_url=None, model="gpt-4o-mini")
]

def select_provider() -> Provider:
    for provider in PROVIDERS:
        if os.getenv(provider.env_var):
            return provider

    expected = ", ".join(p.env_var for p in PROVIDERS)
    raise RuntimeError(f"No provider key set, add one of {expected} to your environment variables")

def build_chat_model() -> tuple[ChatOpenAI, Provider]:
    provider = select_provider()
    kwargs: dict = {
        "model": provider.model,
        "api_key": os.getenv(provider.env_var),
    }
    if provider.base_url is not None:
        kwargs["base_url"] = provider.base_url
    return ChatOpenAI(**kwargs), provider