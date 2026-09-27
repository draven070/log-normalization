import json
import os
from threading import Lock


class JSONEventStore:

    def __init__(self, path):

        self.path = path

        self.lock = Lock()

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        if not os.path.exists(path):

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump([], file)

    def save(self, event):

        with self.lock:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                events = json.load(file)

            events.append(event)

            with open(
                self.path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    events,
                    file,
                    indent=2
                )