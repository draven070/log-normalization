from flask import Flask, request, jsonify

from normalization.normalizer import LogNormalizer
from storage.json_store import JSONEventStore
from config import (
    SERVER_HOST,
    SERVER_PORT,
    API_KEY,
    OUTPUT_FILE,
)


app = Flask(__name__)

normalizer = LogNormalizer()

store = JSONEventStore(
    OUTPUT_FILE
)


@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "online",
        "service": "cross-platform-log-normalizer"
    })


@app.route("/api/events", methods=["POST"])
def receive_event():
    provided_key = request.headers.get(
        "X-API-Key"
    )

    if provided_key != API_KEY:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    data = request.get_json(
        silent=True
    )

    if not data:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    source = data.get("source")

    try:
        linux_sources = {
            "linux",
            "systemd-journal",
            "/var/log/auth.log",
            "/var/log/secure",
        }

        normalized = normalizer.normalize(
            source,
            data.get("message")
            if source in linux_sources
            else data
        )

        if normalized is None:
            return jsonify({
                "status": "ignored"
            }), 200

        normalized_dict = normalized.model_dump()

        store.save(
            normalized_dict
        )

        print(
            f"[+] {source.upper()} | "
            f"{normalized.event.type} | "
            f"{normalized.event.action} | "
            f"{normalized.event.status}"
        )

        return jsonify({
            "status": "success",
            "event": normalized_dict
        }), 201

    except Exception as error:
        print(
            f"[ERROR] {error}"
        )

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":

    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=False
    )