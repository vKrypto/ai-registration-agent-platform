from datetime import UTC, datetime
from uuid import uuid4

AUDIT_EVENTS: list[dict] = []


def record_audit_event(
    *,
    application_id: str,
    actor_type: str,
    action: str,
    previous_state: str | None = None,
    new_state: str | None = None,
    payload: dict | None = None,
) -> dict:
    event = {
        "event_id": f"evt_{uuid4().hex[:12]}",
        "application_id": application_id,
        "actor_type": actor_type,
        "action": action,
        "previous_state": previous_state,
        "new_state": new_state,
        "payload": payload or {},
        "created_at": datetime.now(UTC).isoformat(),
    }
    AUDIT_EVENTS.append(event)
    return event


def get_audit_events(application_id: str) -> list[dict]:
    return [event for event in AUDIT_EVENTS if event["application_id"] == application_id]
