from schema.event import (
    NormalizedLog,
    Source,
    Event,
    User,
    Network,
    Process
)


class WindowsEventParser:

    EVENT_MAP = {

        4624: {
            "type": "authentication",
            "action": "logon",
            "status": "success",
            "category": "authentication"
        },

        4625: {
            "type": "authentication",
            "action": "logon",
            "status": "failed",
            "category": "authentication"
        },

        4634: {
            "type": "authentication",
            "action": "logoff",
            "status": "success",
            "category": "authentication"
        },

        4648: {
            "type": "authentication",
            "action": "explicit_credential_logon",
            "category": "authentication"
        },

        4672: {
            "type": "privilege",
            "action": "special_privileges_assigned",
            "category": "privilege"
        },

        4688: {
            "type": "process",
            "action": "process_creation",
            "category": "process"
        },

        4720: {
            "type": "account",
            "action": "user_created",
            "category": "account_management"
        },

        4726: {
            "type": "account",
            "action": "user_deleted",
            "category": "account_management"
        },

        4740: {
            "type": "account",
            "action": "account_locked",
            "category": "account_management"
        }
    }

    def can_parse(self, event: dict) -> bool:

        return (
            event.get("source") == "windows"
            or "event_id" in event
        )

    def parse(self, event: dict):

        event_id = int(
            event.get("event_id", 0)
        )

        mapping = self.EVENT_MAP.get(
            event_id
        )

        if not mapping:
            return self.parse_unknown(
                event,
                event_id
            )

        return self.create_normalized_event(
            event,
            event_id,
            mapping
        )

    def create_normalized_event(
        self,
        event,
        event_id,
        mapping
    ):

        return NormalizedLog(

            timestamp=event.get(
                "timestamp",
                ""
            ),

            source=Source(
                type="windows",
                host=event.get(
                    "host"
                )
            ),

            event=Event(
                id=event_id,
                type=mapping["type"],
                action=mapping.get("action"),
                status=mapping.get("status"),
                category=mapping.get("category")
            ),

            user=User(
                name=event.get("username"),
                domain=event.get("domain")
            ),

            network=Network(
                src_ip=event.get("src_ip"),
                src_port=self.safe_int(
                    event.get("src_port")
                ),
                dst_ip=event.get("dst_ip"),
                dst_port=self.safe_int(
                    event.get("dst_port")
                ),
                protocol=event.get(
                    "protocol"
                )
            ),

            process=Process(
                name=event.get("process_name"),
                pid=self.safe_int(
                    event.get("process_id")
                ),
                command_line=event.get(
                    "command_line"
                )
            ),

            message=event.get(
                "message"
            ),

            raw_log=str(event)
        )

    def parse_unknown(
        self,
        event,
        event_id
    ):

        return NormalizedLog(

            timestamp=event.get(
                "timestamp",
                ""
            ),

            source=Source(
                type="windows",
                host=event.get(
                    "host"
                )
            ),

            event=Event(
                id=event_id,
                type="unknown",
                category="windows"
            ),

            user=User(
                name=event.get(
                    "username"
                )
            ),

            message=event.get(
                "message"
            ),

            raw_log=str(event)
        )

    @staticmethod
    def safe_int(value):

        if value is None:
            return None

        try:
            return int(value)

        except (
            ValueError,
            TypeError
        ):
            return None