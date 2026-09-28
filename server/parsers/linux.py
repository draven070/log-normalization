import re
from datetime import datetime

from normalization.schema import (
    NormalizedLog,
    Source,
    Event,
    User,
    Network,
    Process,
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

    FAILED_PASSWORD = re.compile(
        r"password check failed for user "
        r"\((?P<user>[^)]+)\)"
    )

    SUDO_AUTH_FAILURE = re.compile(
        r"pam_unix\(sudo:auth\): authentication failure.*?"
        r"user=(?P<user>\S+)"
    )

    def can_parse(self, log):
        """
        Determine whether the log contains a Linux
        authentication/security event that this parser supports.
        """

        keywords = (
            "sshd",
            "unix_chkpwd",
            "pam_unix",
            "authentication failure",
            "Failed password",
            "Accepted password",
            "Accepted publickey",
        )

        return any(keyword in log for keyword in keywords)

    def parse(self, log):
        """
        Parse a Linux authentication/security log.
        """

        # -----------------------------------------
        # SSH failed login
        # -----------------------------------------
        failed = self.FAILED_LOGIN.search(log)

        if failed:
            return self._create_ssh_event(
                log,
                failed,
                status="failed"
            )

        # -----------------------------------------
        # SSH successful login
        # -----------------------------------------
        success = self.SUCCESS_LOGIN.search(log)

        if success:
            return self._create_ssh_event(
                log,
                success,
                status="success"
            )

        # -----------------------------------------
        # Failed password check
        # -----------------------------------------
        password_failed = self.FAILED_PASSWORD.search(log)

        if password_failed:
            return self._create_local_auth_event(
                log,
                username=password_failed.group("user"),
                status="failed",
                process="unix_chkpwd",
                action="password_check"
            )

        # -----------------------------------------
        # Sudo authentication failure
        # -----------------------------------------
        sudo_failure = self.SUDO_AUTH_FAILURE.search(log)

        if sudo_failure:
            return self._create_local_auth_event(
                log,
                username=sudo_failure.group("user"),
                status="failed",
                process="sudo",
                action="sudo_authentication"
            )

        return None

    def _create_ssh_event(self, log, match, status):

        timestamp = self._extract_timestamp(log)

        username = match.group("user")
        source_ip = match.group("ip")
        source_port = int(match.group("port"))

        return NormalizedLog(
            timestamp=timestamp,

            source=Source(
                type="linux"
            ),

            event=Event(
                type="authentication",
                action="login",
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

    def _create_local_auth_event(
        self,
        log,
        username,
        status,
        process,
        action
    ):

        timestamp = self._extract_timestamp(log)

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
                protocol="local"
            ),

            process=Process(
                name=process
            ),

            message=log.strip(),
            raw_log=log.strip()
        )

    def _extract_timestamp(self, log):

        current_year = datetime.now().year

        try:
            timestamp_text = log[:15]

            timestamp = datetime.strptime(
                f"{current_year} {timestamp_text}",
                "%Y %b %d %H:%M:%S"
            ).isoformat()

            return timestamp

        except ValueError:
            return datetime.now().isoformat()