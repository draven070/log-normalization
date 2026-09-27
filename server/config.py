import os


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

API_KEY = os.getenv(
    "NORMALIZER_API_KEY",
    "change-this-key"
)

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    "../output/normalized_events.json"
)