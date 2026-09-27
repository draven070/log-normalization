"""
Configuration for the Linux log collection agent.
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
# Linux Log Configuration
# --------------------------------------------------

LOG_FILE = os.getenv(
    "LINUX_LOG_FILE",
    "/var/log/auth.log"
)


# --------------------------------------------------
# Collector Configuration
# --------------------------------------------------

POLL_INTERVAL = float(
    os.getenv(
        "LINUX_POLL_INTERVAL",
        "0.5"
    )
)


# Only collect SSH-related authentication events
MONITORED_SERVICE = os.getenv(
    "LINUX_MONITORED_SERVICE",
    "sshd"
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
    "LINUX_AGENT_NAME",
    "linux-agent-01"
)

AGENT_VERSION = "1.0.0"