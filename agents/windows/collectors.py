import subprocess
import time
import xml.etree.ElementTree as ET
import requests

from config import (
    SERVER_URL,
    API_KEY,
    LOG_NAME,
    POLL_INTERVAL,
    REQUEST_TIMEOUT,
    AGENT_NAME,
)


NS = {
    "e": "http://schemas.microsoft.com/win/2004/08/events/event"
}


def get_events(last_record_id=0):

    query = (
        "*[System["
        f"EventRecordID > {last_record_id}"
        "]]"
    )

    command = [
        "wevtutil",
        "qe",
        LOG_NAME,
        f"/q:{query}",
        "/f:xml",
        "/c:10",
        "/rd:true",
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )

    except Exception as error:

        print(f"[ERROR] Failed to execute wevtutil: {error}")

        return []

    if result.returncode != 0:

        print(
            f"[ERROR] wevtutil failed: "
            f"{result.stderr.strip()}"
        )

        return []

    if not result.stdout.strip():

        return []

    try:

        root = ET.fromstring(
            f"<Events>{result.stdout}</Events>"
        )

    except ET.ParseError as error:

        print(f"[ERROR] XML parsing failed: {error}")

        return []

    events = []

    for event in root.findall("e:Event", NS):

        system = event.find(
            "e:System",
            NS
        )

        if system is None:
            continue

        event_id_element = system.find(
            "e:EventID",
            NS
        )

        record_id_element = system.find(
            "e:EventRecordID",
            NS
        )

        time_created = system.find(
            "e:TimeCreated",
            NS
        )

        computer = system.find(
            "e:Computer",
            NS
        )

        if event_id_element is None:
            continue

        event_id = int(
            event_id_element.text
        )

        record_id = (
            int(record_id_element.text)
            if record_id_element is not None
            else 0
        )

        timestamp = ""

        if time_created is not None:
            timestamp = time_created.attrib.get(
                "SystemTime",
                ""
            )

        host = ""

        if computer is not None:
            host = computer.text or ""

        event_data = {}

        event_data_element = event.find(
            "e:EventData",
            NS
        )

        if event_data_element is not None:

            for data in event_data_element.findall(
                "e:Data",
                NS
            ):

                name = data.attrib.get(
                    "Name"
                )

                value = data.text or ""

                if name:
                    event_data[name] = value

        raw_xml = ET.tostring(
            event,
            encoding="unicode"
        )

        events.append({
            "event_id": event_id,
            "record_id": record_id,
            "timestamp": timestamp,
            "host": host,
            "data": event_data,
            "raw_log": raw_xml,
        })

    return events


def convert_event(event):

    data = event["data"]

    def first_value(*names):

        for name in names:

            value = data.get(name)

            if value:
                return value

        return None

    payload = {
        "source": "windows",

        "agent_id": AGENT_NAME,

        "timestamp": event["timestamp"],

        "event_id": event["event_id"],

        "host": event["host"],

        "username": first_value(
            "TargetUserName",
            "SubjectUserName",
            "AccountName",
            "UserName",
        ),

        "domain": first_value(
            "TargetDomainName",
            "SubjectDomainName",
            "AccountDomain",
        ),

        "src_ip": first_value(
            "IpAddress",
            "SourceAddress",
            "SourceIP",
        ),

        "src_port": first_value(
            "IpPort",
            "SourcePort",
        ),

        "dst_ip": first_value(
            "DestinationAddress",
            "DestAddress",
            "DestinationIP",
        ),

        "dst_port": first_value(
            "DestinationPort",
            "DestPort",
        ),

        "protocol": first_value(
            "Protocol"
        ),

        "process_name": first_value(
            "NewProcessName",
            "ProcessName",
            "ApplicationName",
        ),

        "process_id": first_value(
            "NewProcessId",
            "ProcessId",
        ),

        "command_line": first_value(
            "CommandLine"
        ),

        "message": (
            f"Windows Event ID "
            f"{event['event_id']}"
        ),

        "raw_log": event["raw_log"],
    }

    return payload


def send_event(event):

    payload = convert_event(event)

    try:

        response = requests.post(
            f"{SERVER_URL}/api/events",
            json=payload,
            headers={
                "X-API-Key": API_KEY
            },
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 201:

            print(
                f"[+] Event {event['event_id']} "
                f"sent successfully"
            )

        elif response.status_code == 200:

            print(
                f"[*] Event {event['event_id']} "
                f"ignored by server"
            )

        else:

            print(
                f"[!] Server returned "
                f"{response.status_code}: "
                f"{response.text}"
            )

    except requests.RequestException as error:

        print(
            f"[!] Connection error: {error}"
        )


def main():

    print(
        f"[*] Agent: {AGENT_NAME}"
    )

    print(
        f"[*] Monitoring Windows Event Log: "
        f"{LOG_NAME}"
    )

    print(
        f"[*] Server: {SERVER_URL}"
    )

    last_record_id = 0

    while True:

        events = get_events(
            last_record_id
        )

        if events:

            print(
                f"[DEBUG] Received "
                f"{len(events)} event(s)"
            )

        for event in events:

            print(
                f"[EVENT] "
                f"ID={event['event_id']} "
                f"RecordID={event['record_id']}"
            )

            send_event(event)

            last_record_id = max(
                last_record_id,
                event["record_id"]
            )

        time.sleep(
            POLL_INTERVAL
        )


if __name__ == "__main__":
    main()