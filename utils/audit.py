import json
from datetime import datetime
from pathlib import Path


AUDIT_FILE = Path("audit_log.json")


def log_event(event_type, details):
    """
    Record an important action in the system.
    """

    event = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "event": event_type,
        "details": details
    }

    # Read existing logs
    if AUDIT_FILE.exists():

        with open(AUDIT_FILE, "r", encoding="utf-8") as file:
            logs = json.load(file)

    else:

        logs = []

    # Add new event
    logs.append(event)

    # Save updated logs
    with open(AUDIT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            logs,
            file,
            indent=4
        )

    return event


def get_audit_logs():
    """
    Return all recorded audit events.
    """

    if not AUDIT_FILE.exists():
        return []

    with open(AUDIT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)