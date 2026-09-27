import os
import time
import requests
from datetime import datetime

from config import (
    SERVER_URL,
    API_KEY,
    LOG_FILE,
    POLL_INTERVAL,
    MONITORED_SERVICE,
    REQUEST_TIMEOUT,
    AGENT_NAME,
)


def send_event(message):

    payload = {
        "source": "linux",
        "agent_id": AGENT_NAME,
        "timestamp": datetime.now().isoformat(),
        "host": os.uname().nodename,
        "message": message
    }

    try:

        response = requests.post(
            f"{SERVER_URL}/api/events",
            json=payload,
            headers={
                "X-API-Key": API_KEY
            },
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 201:

            print("[+] Event sent")

        else:

            print(
                f"[!] Server returned "
                f"{response.status_code}"
            )

    except requests.RequestException as error:

        print(
            f"[!] Connection error: {error}"
        )


def follow_file(path):

    print(
        f"[*] Monitoring {path}"
    )

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as file:

        file.seek(
            0,
            os.SEEK_END
        )

        while True:

            line = file.readline()

            if not line:

                time.sleep(POLL_INTERVAL)

                continue

            yield line.strip()


def main():

    print(
        f"[*] Agent: {AGENT_NAME}"
    )

    print(
        f"[*] Monitoring: {LOG_FILE}"
    )

    for line in follow_file(LOG_FILE):

        if MONITORED_SERVICE in line:

            print(
                f"[EVENT] {line}"
            )

            send_event(line)


if __name__ == "__main__":
    main()