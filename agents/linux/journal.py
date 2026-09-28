import subprocess
import threading


class JournalCollector:
    """
    Collects Linux events from systemd journal.

    Works on distributions using systemd:
    Ubuntu
    Debian
    Kali
    RHEL
    Rocky
    AlmaLinux
    etc.
    """

    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.process = None

    def start(self):
        self.running = True

        self.process = subprocess.Popen(
            [
                "journalctl",
                "-f",
                "-n",
                "0",
                "-o",
                "short-iso"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        thread = threading.Thread(
            target=self._read,
            daemon=True
        )

        thread.start()

    def _read(self):
        if not self.process or not self.process.stdout:
            return

        for line in self.process.stdout:
            if not self.running:
                break

            line = line.strip()

            if not line:
                continue

            self.callback(line)

    def stop(self):
        self.running = False

        if self.process:
            self.process.terminate()