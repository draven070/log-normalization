import os
from pathlib import Path
from dotenv import load_dotenv


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


# --------------------------------------------------
# Server
# --------------------------------------------------

SERVER_URL = os.getenv(
    "NORMALIZER_SERVER",
    "http://127.0.0.1:5000"
)

API_KEY = os.getenv("NORMALIZER_API_KEY")

REQUEST_TIMEOUT = int(
    os.getenv("NORMALIZER_REQUEST_TIMEOUT", "5")
)


# --------------------------------------------------
# Agent
# --------------------------------------------------

AGENT_NAME = os.getenv(
    "LINUX_AGENT_NAME",
    "linux-agent-01"
)


# --------------------------------------------------
# Collection
# --------------------------------------------------

POLL_INTERVAL = float(
    os.getenv("LINUX_POLL_INTERVAL", "0.5")
)

ENABLE_JOURNAL = (
    os.getenv("LINUX_ENABLE_JOURNAL", "true").lower()
    == "true"
)

ENABLE_AUTH_LOG = (
    os.getenv("LINUX_ENABLE_AUTH_LOG", "true").lower()
    == "true"
)


# --------------------------------------------------
# Log locations
# --------------------------------------------------

AUTH_LOG_PATH = os.getenv(
    "LINUX_AUTH_LOG_PATH",
    "/var/log/auth.log"
)

SECURE_LOG_PATH = os.getenv(
    "LINUX_SECURE_LOG_PATH",
    "/var/log/secure"
)


# --------------------------------------------------
# Validation
# --------------------------------------------------

if not API_KEY:
    raise RuntimeError(
        "NORMALIZER_API_KEY is missing from .env"
    )