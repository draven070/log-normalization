import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load shared environment file
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)

# Server connection
SERVER_URL = os.getenv(
    "NORMALIZER_SERVER",
    "http://127.0.0.1:5000"
)

API_KEY = os.getenv("NORMALIZER_API_KEY")

# Windows Event Log settings
LOG_NAME = os.getenv("WINDOWS_LOG_NAME", "Security")
POLL_INTERVAL = float(
    os.getenv("WINDOWS_POLL_INTERVAL", "1.0")
)

# Agent settings
AGENT_NAME = os.getenv(
    "WINDOWS_AGENT_NAME",
    "windows-agent-01"
)

REQUEST_TIMEOUT = int(
    os.getenv("NORMALIZER_REQUEST_TIMEOUT", "5")
)

if not API_KEY:
    raise RuntimeError("NORMALIZER_API_KEY is missing from .env")