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

        Args:
            source (str): 'linux' or 'windows'
            data: Raw event data.

        Returns:
            NormalizedLog | None
        """

        source = source.lower()

        if source == "linux":
            return self.normalize_linux(data)

        if source == "windows":
            return self.normalize_windows(data)

        raise ValueError(
            f"Unsupported log source: {source}"
        )