from normalization.schema import (
    NormalizedLog,
    Source,
    Event,
    User,
    Network,
    Process
)


EVENT_MAP = {

    4624: {
        "type": "authentication",
        "action": "login",
        "status": "success",
        "category": "authentication"
    },

    4625: {
        "type": "authentication",
        "action": "login",
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
        "action": "explicit_credentials",
        "status": "success",
        "category": "authentication"
    },

    4672: {
        "type": "privilege",
        "action": "special_privileges_assigned",
        "status": "success",
        "category": "privilege"
    },

    4688: {
        "type": "process",
        "action": "process_creation",
        "status": "success",
        "category": "process"
    },

    4720: {
        "type": "account",
        "action": "user_created",
        "status": "success",
        "category": "account_management"
    },

    4726: {
        "type": "account",
        "action": "user_deleted",
        "status": "success",
        "category": "account_management"
    },

    4740: {
        "type": "account",
        "action": "account_locked",
        "status": "success",
        "category": "account_management"
    }
}


class WindowsEventParser:

    def parse(self, event):

        event_id = int(event.get("event_id", 0))

        mapping = EVENT_MAP.get(
            event_id,
            {
                "type": "unknown",
                "action": "unknown",
                "status": None,
                "category": "windows"
            }
        )

        return NormalizedLog(

            timestamp=event.get(
                "timestamp",
                ""
            ),

            source=Source(
                type="windows",
                host=event.get("host")
            ),

            event=Event(
                id=event_id,
                type=mapping["type"],
                action=mapping["action"],
                status=mapping["status"],
                category=mapping["category"]
            ),

            user=User(
                name=event.get("username"),
                domain=event.get("domain")
            ),

            network=Network(
                src_ip=event.get("src_ip"),
                src_port=self._int(
                    event.get("src_port")
                ),
                dst_ip=event.get("dst_ip"),
                dst_port=self._int(
                    event.get("dst_port")
                ),
                protocol=event.get("protocol")
            ),

            process=Process(
                name=event.get("process_name"),
                pid=self._int(
                    event.get("process_id")
                ),
                command_line=event.get(
                    "command_line"
                )
            ),

            message=event.get("message"),

            raw_log=event.get("raw_log")
        )

    @staticmethod
    def _int(value):

        if value is None:
            return None

        try:
            return int(value)

        except (ValueError, TypeError):
            return None