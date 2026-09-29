from google.api_core.exceptions import GoogleAPICallError

from client_service import add_client, get_clients
from session_service import (
    add_session,
    get_sessions,
    update_session_status,
    delete_session,
)


SESSION_TYPES = ["Individual", "Couples", "Premarital", "Follow-up"]
STATUSES = ["Scheduled", "Completed", "Cancelled"]


def ask_required(prompt):
    """Keep asking until the user enters a nonempty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def choose_option(label, options):
    """Let the user select one of the allowed values by number."""
    print(f"\n{label}")
    for number, option in enumerate(options, start=1):
        print(f"{number}. {option}")
    while True:
        choice = input("Choose a number: ").strip()
        if choice in [str(number) for number in range(1, len(options) + 1)]:
            return options[int(choice) - 1]
        print(f"Please choose a number from 1 to {len(options)}.")


def view_clients():
    """Display existing clients and return the list for client selection."""
    clients = get_clients()
    print("\nCLIENTS")
    if not clients:
        print("No clients found.")
    for client in clients:
        print(f"Document ID: {client['id']}")
        print(f"First name: {client.get('first_name', '')}")
        print(f"Last name: {client.get('last_name', '')}")
        print(f"Phone number: {client.get('phone_number', '')}")
        print(f"Email: {client.get('email', '')}\n")
    return clients


def view_sessions():
    """Display existing sessions and return the list for session selection."""
    sessions = get_sessions()
    print("\nSESSIONS")
    if not sessions:
        print("No sessions found.")
    for session in sessions:
        print(f"Document ID: {session['id']}")
        print(f"Client name: {session.get('client_name', '')}")
        print(f"Session date: {session.get('session_date', '')}")
        print(f"Session time: {session.get('session_time', '')}")
        print(f"Session type: {session.get('session_type', '')}")
        print(f"Status: {session.get('status', '')}")
        print(f"Notes: {session.get('notes', '')}\n")
    return sessions


def choose_record(records, label):
    """Find a record by its displayed document ID, or cancel with a blank input."""
    while True:
        record_id = input(f"Enter {label} document ID (Enter to cancel): ").strip()
        if not record_id:
            return None
        for record in records:
            if record["id"] == record_id:
                return record
        print("That ID is not in the displayed list. Please try again.")


def add_client_prompt():
    """Collect fictional client details and save them using the client service."""
    first_name = ask_required("First name: ")
    last_name = ask_required("Last name: ")
    phone_number = ask_required("Phone number: ")
    email = ask_required("Email: ")
    client_id = add_client(first_name, last_name, phone_number, email)
    print(f"Client added successfully! Document ID: {client_id}")


def add_session_prompt():
    """Choose an existing client and collect the fictional session details."""
    clients = view_clients()
    if not clients:
        print("Add a fictional client before adding a session.")
        return
    client = choose_record(clients, "client")
    if client is None:
        return

    # Use the selected client's name so it matches the chosen document ID.
    client_name = f"{client['first_name']} {client['last_name']}"
    session_date = ask_required("Session date (YYYY-MM-DD): ")
    session_time = ask_required("Session time (HH:MM, 24-hour): ")
    session_type = choose_option("Session type", SESSION_TYPES)
    status = choose_option("Session status", STATUSES)
    notes = input("Fictional notes (optional): ").strip()
    session_id = add_session(
        client["id"], client_name, session_date, session_time,
        session_type, status, notes,
    )
    print(f"Session added successfully! Document ID: {session_id}")


def update_session_prompt():
    """Display sessions, choose one, and update its status through the service."""
    sessions = view_sessions()
    if not sessions:
        return
    session = choose_record(sessions, "session")
    if session is None:
        return
    status = choose_option("New session status", STATUSES)
    if update_session_status(session["id"], status):
        print(f"Session status updated to {status}.")
    else:
        print("Session not found. It may have already been deleted.")


def delete_session_prompt():
    """Display sessions and delete the session selected by document ID."""
    sessions = view_sessions()
    if not sessions:
        return
    session = choose_record(sessions, "session")
    if session is None:
        return
    if delete_session(session["id"]):
        print("Session deleted successfully!")
    else:
        print("Session not found. Nothing was deleted.")


def main():
    """Repeat the menu until the user chooses Exit."""
    print("Cloud Therapy Session Records Manager")
    print("Use fictional client details and session information only.")
    while True:
        print("\n1. Add client\n2. View clients\n3. Add session\n4. View sessions")
        print("5. Update session status\n6. Delete session\n7. Exit")
        choice = input("Choose an option (1-7): ").strip()
        try:
            if choice == "1":
                add_client_prompt()
            elif choice == "2":
                view_clients()
            elif choice == "3":
                add_session_prompt()
            elif choice == "4":
                view_sessions()
            elif choice == "5":
                update_session_prompt()
            elif choice == "6":
                delete_session_prompt()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")
        except (ValueError, GoogleAPICallError) as error:
            # Report validation or database errors, then return to the menu.
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    main()
