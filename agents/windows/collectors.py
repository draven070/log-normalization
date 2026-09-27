import subprocess
import xml.etree.ElementTree as ET
import requests
import time

from config import (
    SERVER_URL,
    API_KEY,
    LOG_NAME,
    POLL_INTERVAL,
    REQUEST_TIMEOUT,
    AGENT_NAME,
)


last_record_id = 0


def get_events():

    query = f"""
    <QueryList>
        <Query Id="0">
            <Select Path="{LOG_NAME}">
                *[System[
                    EventRecordID &gt; {last_record_id}
                ]]
            </Select>
        </Query>
    </QueryList>
    """

    command = [
        "wevtutil",
        "qe",
        LOG_NAME,
        "/q:" + query,
        "/f:xml"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:

        print(
            "[!] Unable to read Windows Event Log"
        )

        print(result.stderr)

        return []

    return parse_events(result.stdout)


def send_event(event):

    try:

        response = requests.post(

            f"{SERVER_URL}/api/events",

            json=event,

            headers={
                "X-API-Key": API_KEY
            },

            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 201:

            print(
                f"[+] Sent Windows Event "
                f"{event['event_id']}"
            )

        else:

            print(
                f"[!] Server returned "
                f"{response.status_code}"
            )

    except requests.RequestException as error:

        print(
            f"[!] Connection error: {error}"
        )


def main():

    global last_record_id

    print(
        f"[*] Agent: {AGENT_NAME}"
    )

    print(
        f"[*] Monitoring Windows Event Log: "
        f"{LOG_NAME}"
    )

    while True:

        events = get_events()

        for event in events:

            if event["record_id"] <= last_record_id:
                continue

            last_record_id = event["record_id"]

            normalized_input = convert_event(
                event
            )

            normalized_input["agent_id"] = AGENT_NAME

            send_event(
                normalized_input
            )

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()