import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
print("Project Root", PROJECT_ROOT)
PROMPTS_DIR = PROJECT_ROOT / "prompts"

DEFAULT_WORKING_DIR = PROJECT_ROOT / "workspace"

AGENT_NAME = "Claudia"

MAX_MODEL_CALLS_PER_RUN = int(os.getenv("MAX_MODEL_CALLS_PER_RUN", 10))
MAX_READ_BYTES = int(os.getenv("MAX_READ_BYTES", 1024 * 1024))


def get_working_directory() -> Path:
    override = os.getenv("WORKING_DIRECTORY",DEFAULT_WORKING_DIR).strip()
    if override:
        return Path(override).expanduser().resolve()
    return DEFAULT_WORKING_DIR.resolve()

def is_hitl_enabled() -> bool:
    return os.getenv("HITL_ENABLED" , "true").lower() in ("true", "1", "yes", "y")

