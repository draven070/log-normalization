from parsers.linux import LinuxAuthParser
from parsers.windows import WindowsEventParser


class LogNormalizer:
    """
    Central normalization engine.

    Receives platform-specific events and converts
    them into the common NormalizedLog schema.
    """

    def __init__(self):
        self.linux_parser = LinuxAuthParser()
        self.windows_parser = WindowsEventParser()

    def normalize_linux(self, log):
        """
        Normalize a Linux log line.

        Args:
            log (str): Raw Linux log line.

        Returns:
            NormalizedLog | None
        """
        if not self.linux_parser.can_parse(log):
            return None

        return self.linux_parser.parse(log)

    def normalize_windows(self, event):
        """
        Normalize a Windows event.

        Args:
            event (dict): Windows event data.

        Returns:
            NormalizedLog
        """
        return self.windows_parser.parse(event)

    def normalize(self, source, data):
        """
        Generic normalization method.

        Supported Linux sources:
            - linux
            - systemd-journal
            - /var/log/auth.log
            - /var/log/secure

        Supported Windows source:
            - windows
        """

        source = source.lower().strip()

        # Linux sources
        linux_sources = {
            "linux",
            "systemd-journal",
            "/var/log/auth.log",
            "/var/log/secure",
        }

        if source in linux_sources:
            return self.normalize_linux(data)

        # Windows source
        if source == "windows":
            return self.normalize_windows(data)

        raise ValueError(
            f"Unsupported log source: {source}"
        )