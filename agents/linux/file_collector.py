import os
import time
import threading


class FileCollector:
    """
    Generic real-time log file collector.

    Supports:
        /var/log/auth.log
        /var/log/secure
        and other text-based logs.
    """

    def __init__(self, path, callback, poll_interval=0.5):
        self.path = path
        self.callback = callback
        self.poll_interval = poll_interval

        self.running = False
        self.thread = None

    def start(self):
        if not os.path.exists(self.path):
            print(f"[FILE] Log file not found: {self.path}")
            return False

        self.running = True

        self.thread = threading.Thread(
            target=self._follow,
            daemon=True
        )

        self.thread.start()

        print(f"[FILE] Monitoring: {self.path}")

        return True

    def _follow(self):
        try:
            with open(
                self.path,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:

                file.seek(0, os.SEEK_END)

                while self.running:
                    line = file.readline()

                    if line:
                        line = line.strip()

                        if line:
                            self.callback(
                                line,
                                self.path
                            )
                    else:
                        time.sleep(self.poll_interval)

        except PermissionError:
            print(
                f"[FILE] Permission denied: {self.path}"
            )

        except Exception as exc:
            print(
                f"[FILE] Collector error: {exc}"
            )

    def stop(self):
        self.running = False