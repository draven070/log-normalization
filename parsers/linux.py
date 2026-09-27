import re
from datetime import datetime

from schema.event import (
    NormalizedLog,
    Source,
    Event,
    User,
    Network,
    Process
)


class LinuxAuthParser:

    FAILED_LOGIN = re.compile(
        r"(?P<month>\w{3})\s+"
        r"(?P<day>\d+)\s+"
        r"(?P<time>\d+:\d+:\d+)\s+"
        r"(?P<host>\S+)\s+"
        r"sshd\[(?P<pid>\d+)\]:\s+"
        r"Failed password for "
        r"(?:invalid user )?"
        r"(?P<user>\S+)\s+"
        r"from\s+"
        r"(?P<ip>[\d.]+)\s+"
        r"port\s+"
        r"(?P<port>\d+)"
    )

    SUCCESS_LOGIN = re.compile(
        r"(?P<month>\w{3})\s+"
        r"(?P<day>\d+)\s+"
        r"(?P<time>\d+:\d+:\d+)\s+"
        r"(?P<host>\S+)\s+"
        r"sshd\[(?P<pid>\d+)\]:\s+"
        r"Accepted password for "
        r"(?P<user>\S+)\s+"
        r"from\s+"
        r"(?P<ip>[\d.]+)\s+"
        r"port\s+"
        r"(?P<port>\d+)"
    )

    def can_parse(self, log: str) -> bool:
        return "sshd" in log

    def parse(self, log: str):

        match = self.FAILED_LOGIN.search(log)

        if match:
            data = match.groupdict()

            return self.create_event(
                data,
                log,
                status="failed"
            )

        match = self.SUCCESS_LOGIN.search(log)

        if match:
            data = match.groupdict()

            return self.create_event(
                data,
                log,
                status="success"
            )

        return None

    def create_event(
        self,
        data,
        raw_log,
        status
    ):

        timestamp = self.build_timestamp(
            data["month"],
            data["day"],
            data["time"]
        )

        return NormalizedLog(

            timestamp=timestamp,

            source=Source(
                type="linux",
                host=data["host"]
            ),

            event=Event(
                type="authentication",
                action="login",
                status=status,
                category="authentication"
            ),

            user=User(
                name=data["user"]
            ),

            network=Network(
                src_ip=data["ip"],
                src_port=int(data["port"]),
                protocol="ssh"
            ),

            process=Process(
                name="sshd",
                pid=int(data["pid"])
            ),

            message=raw_log,

            raw_log=raw_log
        )

    def build_timestamp(
        self,
        month,
        day,
        time
    ):

        year = datetime.now().year

        date_string = (
            f"{year} "
            f"{month} "
            f"{day} "
            f"{time}"
        )

        dt = datetime.strptime(
            date_string,
            "%Y %b %d %H:%M:%S"
        )

        return dt.isoformat()