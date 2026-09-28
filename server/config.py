import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load shared environment file
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)

# Flask server configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "5000"))

# API authentication
API_KEY = os.getenv("NORMALIZER_API_KEY")

# Storage configuration
OUTPUT_FILE = PROJECT_ROOT / os.getenv(
    "OUTPUT_FILE",
    "output/normalized_events.json"
)

if not API_KEY:
    raise RuntimeError("NORMALIZER_API_KEY is missing from .env")