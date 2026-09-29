from firebase_admin import firestore
from google.api_core.exceptions import NotFound

from firebase_config import db


def add_session(client_id, client_name, session_date, session_time,
                session_type, status, notes):
    """Save a new therapy session and return its Firestore document ID.

    Pass the existing client's document ID, a date as YYYY-MM-DD,
    and a time as HH:MM. The date and time are stored as text.
    """
    # Reject unsupported values before writing anything to Firestore.
    session_types = ["Individual", "Couples", "Premarital", "Follow-up"]
    statuses = ["Scheduled", "Completed", "Cancelled"]

    if session_type not in session_types:
        raise ValueError("Session type must be Individual, Couples, Premarital, or Follow-up.")
    if status not in statuses:
        raise ValueError("Status must be Scheduled, Completed, or Cancelled.")

    # The client ID links this session to an existing client document.
    session_data = {
        "client_id": client_id,
        "client_name": client_name,
        "session_date": session_date,
        "session_time": session_time,
        "session_type": session_type,
        "status": status,
        "notes": notes,
        # Firestore sets the creation timestamp when it saves the record.
        "date_created": firestore.SERVER_TIMESTAMP,
    }

    # Firestore generates a unique ID for each new session document.
    update_time, session_reference = db.collection("sessions").add(session_data)
    return session_reference.id


def get_sessions():
    """Return all sessions as a list of dictionaries, each including its document ID."""
    sessions = []
    for document in db.collection("sessions").stream():
        session = document.to_dict()
        # Keep the session's document ID separate from its client_id field.
        session["id"] = document.id
        sessions.append(session)
    return sessions


def update_session_status(session_id, new_status):
    """Update only a session's status; return False if the document is missing.

    Return True after a successful update. Invalid statuses raise ValueError.
    """
    statuses = ["Scheduled", "Completed", "Cancelled"]
    if new_status not in statuses:
        raise ValueError("Status must be Scheduled, Completed, or Cancelled.")

    session_reference = db.collection("sessions").document(session_id)
    try:
        # update() changes only the supplied field and never creates a document.
        session_reference.update({"status": new_status})
    except NotFound:
        return False

    return True


def delete_session(session_id):
    """Delete a session; return True if deleted or False if it does not exist."""
    session_reference = db.collection("sessions").document(session_id)

    # Check first because Firestore also allows deleting a missing document.
    if not session_reference.get().exists:
        return False

    session_reference.delete()
    return True
