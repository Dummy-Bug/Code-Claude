from memory import make_checkpointer
from schema import TurnSummary
from langchain.agents.structured_output import ProviderStrategy
from prompts import build_system_prompt
from tools import ALL_TOOLS
from langchain.agents import create_agent
from models import build_chat_model
from langgraph.checkpoint.base import BaseCheckpointSaver

from middlewares.hitl import build_hitl_middleware
from middlewares.audit import AuditMiddleware
from config.config import MAX_MODEL_CALLS_PER_RUN, hitl_enabled
from langchain.agents.middleware import ModelCallLimitMiddleware

from middlewares.protection import ProtectionMiddleware


def build_middleware(enable_hitl: bool) -> list:
    layers: list = [
        ModelCallLimitMiddleware(
            run_limit=MAX_MODEL_CALLS_PER_RUN,
            exit_behavior="end"
        ),
        AuditMiddleware(),
        ProtectionMiddleware(),
    ]

    if enable_hitl:
        layers.append(build_hitl_middleware())

    return layers


def build_agent(
        *,
        checkpointer: BaseCheckpointSaver | None = None,
        enable_hitl: bool | None = None,
        extra_guidance: str = "",
):
    model, _provider = build_chat_model()
    use_hitl = hitl_enabled() if enable_hitl is None else enable_hitl

    return create_agent(
        model=model,
        tools=ALL_TOOLS,
        system_prompt=build_system_prompt(extra_guidance=extra_guidance),
        middleware=build_middleware(use_hitl),
        response_format=ProviderStrategy(TurnSummary),
        checkpointer=checkpointer or make_checkpointer(),
        name="Claudia"
    )
