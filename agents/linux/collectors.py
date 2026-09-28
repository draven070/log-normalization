import time
import requests

from config import (
    SERVER_URL,
    API_KEY,
    AGENT_NAME,
    REQUEST_TIMEOUT,
    POLL_INTERVAL,
    ENABLE_JOURNAL,
    ENABLE_AUTH_LOG,
    AUTH_LOG_PATH,
    SECURE_LOG_PATH,
)

from journal import JournalCollector
from file_collector import FileCollector


# --------------------------------------------------
# API
# --------------------------------------------------

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}


def send_event(message, source):
    """
    Send raw Linux event to central server.
    """

    payload = {
        "agent": AGENT_NAME,
        "source": source,
        "message": message,
    }

    try:
        response = requests.post(
            f"{SERVER_URL}/api/events",
            json=payload,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

        if response.ok:
            print(
                f"[SENT] {source}: {message}"
            )
        else:
            print(
                f"[SERVER ERROR] "
                f"{response.status_code}: "
                f"{response.text}"
            )

    except requests.RequestException as exc:
        print(
            f"[CONNECTION ERROR] {exc}"
        )


# --------------------------------------------------
# Journal handler
# --------------------------------------------------

def handle_journal(message):
    send_event(
        message,
        "systemd-journal"
    )


# --------------------------------------------------
# File handler
# --------------------------------------------------

def handle_file(message, path):
    send_event(
        message,
        path
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("Linux Security Log Collector")
    print("=" * 60)

    print(f"Agent       : {AGENT_NAME}")
    print(f"Server      : {SERVER_URL}")
    print(f"Journal     : {ENABLE_JOURNAL}")
    print(f"Auth log    : {ENABLE_AUTH_LOG}")
    print("=" * 60)

    collectors = []

    # ----------------------------------------------
    # systemd journal
    # ----------------------------------------------

    if ENABLE_JOURNAL:

        journal = JournalCollector(
            handle_journal
        )

        journal.start()

        collectors.append(journal)

        print(
            "[STARTED] systemd journal collector"
        )

    # ----------------------------------------------
    # Traditional Linux logs
    # ----------------------------------------------

    if ENABLE_AUTH_LOG:

        for path in [
            AUTH_LOG_PATH,
            SECURE_LOG_PATH,
        ]:

            collector = FileCollector(
                path,
                handle_file,
                POLL_INTERVAL
            )

            if collector.start():
                collectors.append(collector)

    # ----------------------------------------------
    # Keep running
    # ----------------------------------------------

    if not collectors:
        print(
            "[ERROR] No Linux log source available."
        )

        return

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping collectors...")

        for collector in collectors:
            collector.stop()

        print("Linux collector stopped.")


if __name__ == "__main__":
    main()