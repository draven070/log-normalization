import re
from datetime import datetime

from normalization.schema import (
    NormalizedLog,
    Source,
    Event,
    User,
    Network,
    Process
)


class LinuxAuthParser:

    FAILED_LOGIN = re.compile(
        r"Failed password for (?:invalid user )?"
        r"(?P<user>\S+) from (?P<ip>\S+) "
        r"port (?P<port>\d+)"
    )

    SUCCESS_LOGIN = re.compile(
        r"Accepted (?:password|publickey) for "
        r"(?P<user>\S+) from (?P<ip>\S+) "
        r"port (?P<port>\d+)"
    )

    def can_parse(self, log):
        return "sshd" in log

    def parse(self, log):

        failed = self.FAILED_LOGIN.search(log)

        if failed:
            return self._create_event(
                log,
                failed,
                status="failed"
            )

        success = self.SUCCESS_LOGIN.search(log)

        if success:
            return self._create_event(
                log,
                success,
                status="success"
            )

        return None

    def _create_event(self, log, match, status):

        current_year = datetime.now().year

        try:
            timestamp_text = log[:15]

            timestamp = datetime.strptime(
                f"{current_year} {timestamp_text}",
                "%Y %b %d %H:%M:%S"
            ).isoformat()

        except ValueError:
            timestamp = datetime.now().isoformat()

        username = match.group("user")
        source_ip = match.group("ip")
        source_port = int(match.group("port"))

        action = "login"

        return NormalizedLog(
            timestamp=timestamp,

            source=Source(
                type="linux"
            ),

            event=Event(
                type="authentication",
                action=action,
                status=status,
                category="authentication"
            ),

            user=User(
                name=username
            ),

            network=Network(
                src_ip=source_ip,
                src_port=source_port,
                protocol="ssh"
            ),

            process=Process(
                name="sshd"
            ),

            message=log.strip(),

            raw_log=log.strip()
        )