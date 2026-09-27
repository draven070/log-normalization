from parsers.linux import LinuxAuthParser
from parsers.windows import WindowsEventParser


class LogNormalizer:

    def __init__(self):

        self.linux_parser = LinuxAuthParser()

        self.windows_parser = WindowsEventParser()

    def normalize_linux(
        self,
        log: str
    ):

        if self.linux_parser.can_parse(log):

            return self.linux_parser.parse(
                log
            )

        return None

    def normalize_windows(
        self,
        event: dict
    ):

        if self.windows_parser.can_parse(
            event
        ):

            return self.windows_parser.parse(
                event
            )

        return None