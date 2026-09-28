import os
from pathlib import Path

from dotenv import load_dotenv


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load the single root .env
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


# ==========================================
# SERVER
# ==========================================

SERVER_HOST = os.getenv(
    "SERVER_HOST",
    "0.0.0.0"
)

SERVER_PORT = int(
    os.getenv(
        "SERVER_PORT",
        "5000"
    )
)


# ==========================================
# AGENT -> SERVER
# ==========================================

NORMALIZER_SERVER = os.getenv(
    "NORMALIZER_SERVER",
    "http://127.0.0.1:5000"
)

NORMALIZER_API_KEY = os.getenv(
    "NORMALIZER_API_KEY"
)

NORMALIZER_REQUEST_TIMEOUT = int(
    os.getenv(
        "NORMALIZER_REQUEST_TIMEOUT",
        "5"
    )
)


# ==========================================
# STORAGE
# ==========================================

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    "output/normalized_events.json"
)


# ==========================================
# WINDOWS
# ==========================================

WINDOWS_LOG_NAME = os.getenv(
    "WINDOWS_LOG_NAME",
    "Security"
)

WINDOWS_POLL_INTERVAL = float(
    os.getenv(
        "WINDOWS_POLL_INTERVAL",
        "1.0"
    )
)

WINDOWS_AGENT_NAME = os.getenv(
    "WINDOWS_AGENT_NAME",
    "windows-agent-01"
)


# ==========================================
# LINUX
# ==========================================

LINUX_LOG_FILE = os.getenv(
    "LINUX_LOG_FILE",
    "/var/log/auth.log"
)

LINUX_POLL_INTERVAL = float(
    os.getenv(
        "LINUX_POLL_INTERVAL",
        "0.5"
    )
)

LINUX_MONITORED_SERVICE = os.getenv(
    "LINUX_MONITORED_SERVICE",
    "sshd"
)

LINUX_AGENT_NAME = os.getenv(
    "LINUX_AGENT_NAME",
    "linux-agent-01"
)


# ==========================================
# VALIDATION
# ==========================================

if not NORMALIZER_API_KEY:
    raise RuntimeError(
        "NORMALIZER_API_KEY is missing from .env"
    )