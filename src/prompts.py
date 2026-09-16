from jinja2 import Environment, FileSystemLoader, select_autoescape

from config.config import AGENT_NAME, PROMPTS_DIR, get_work_dir
from tools import tool_catalog

_env = Environment(
    loader=FileSystemLoader(PROMPTS_DIR),
    autoescape=select_autoescape(enabled_extensions=()),
    trim_blocks=True,
    lstrip_blocks=True,
)


def _render_template(*, template_name, **context) -> str:
    return _env.get_template(template_name).render(**context)


def build_system_prompt(*, agent_name: str = AGENT_NAME, extra_guidance: str = "") -> str:
    return _render_template(
        template_name="system.jinja",
        agent_name=agent_name,
        extra_guidance=extra_guidance,
        work_dir=str(get_work_dir()),
        tools=tool_catalog()
    )


def build_greeting_prompt(
        *,
        agent_name: str = AGENT_NAME,
) -> str:
    return _render_template(
        template_name="greeting.jinja",
        agent_name=agent_name,
        work_dir=str(get_work_dir()),
    )
