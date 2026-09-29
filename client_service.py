from firebase_admin import firestore

from firebase_config import db


def add_client(first_name, last_name, phone_number, email):
    """Save a new client in Firestore and return the new document's ID."""
    # Each dictionary key becomes a field in the Firestore document.
    client_data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "email": email,
        # Firestore sets this timestamp when it saves the record.
        "date_created": firestore.SERVER_TIMESTAMP,
    }

    # add() generates a unique document ID and returns the write time
    # followed by a reference to the new document.
    update_time, client_reference = db.collection("clients").add(client_data)
    return client_reference.id


def get_clients():
    """Return all clients as a list of dictionaries, each including its document ID."""
    clients = []
    for document in db.collection("clients").stream():
        client = document.to_dict()
        # The document ID is separate from its stored fields in Firestore.
        client["id"] = document.id
        clients.append(client)
    return clients
