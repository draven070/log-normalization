"""
Configuration for the Windows Event Log collection agent.
"""

import os


# --------------------------------------------------
# Central Normalizer Server
# --------------------------------------------------

SERVER_URL = os.getenv(
    "NORMALIZER_SERVER",
    "http://127.0.0.1:5000"
)

API_KEY = os.getenv(
    "NORMALIZER_API_KEY",
    "change-this-key"
)


# --------------------------------------------------
# Windows Event Log Configuration
# --------------------------------------------------

LOG_NAME = os.getenv(
    "WINDOWS_LOG_NAME",
    "Security"
)


# --------------------------------------------------
# Collector Configuration
# --------------------------------------------------

POLL_INTERVAL = float(
    os.getenv(
        "WINDOWS_POLL_INTERVAL",
        "1.0"
    )
)


# --------------------------------------------------
# HTTP Configuration
# --------------------------------------------------

REQUEST_TIMEOUT = int(
    os.getenv(
        "NORMALIZER_REQUEST_TIMEOUT",
        "5"
    )
)


# --------------------------------------------------
# Agent Information
# --------------------------------------------------

AGENT_NAME = os.getenv(
    "WINDOWS_AGENT_NAME",
    "windows-agent-01"
)

AGENT_VERSION = "1.0.0"