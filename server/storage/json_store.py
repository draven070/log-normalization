import json
import os
from threading import Lock


class JSONEventStore:

    def __init__(self, path):

        self.path = path
        self.lock = Lock()

        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        self._initialize_file()

    def _initialize_file(self):

        if not os.path.exists(self.path):

            self._write_events([])

            return

        try:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read().strip()

                if not content:
                    raise ValueError("Empty JSON file")

                json.loads(content)

        except (json.JSONDecodeError, ValueError):

            print(
                f"[!] Invalid JSON store detected: "
                f"{self.path}"
            )

            print(
                "[*] Resetting JSON event store..."
            )

            self._write_events([])

    def _read_events(self):

        try:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read().strip()

                if not content:
                    return []

                data = json.loads(content)

                if not isinstance(data, list):
                    print(
                        "[!] JSON store root is not a list. "
                        "Resetting."
                    )
                    return []

                return data

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            return []

    def _write_events(self, events):

        temp_path = f"{self.path}.tmp"

        with open(
            temp_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                events,
                file,
                indent=2
            )

        os.replace(
            temp_path,
            self.path
        )

    def save(self, event):

        with self.lock:

            events = self._read_events()

            events.append(event)

            self._write_events(events)

            print(
                f"[+] Stored event "
                f"(total={len(events)})"
            )