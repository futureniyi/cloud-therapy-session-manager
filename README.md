# Overview

Cloud Therapy Session Records Manager is a Python command-line application for organizing fictional clients and therapy sessions. It stores records in Google Firebase Firestore so the information remains available after the program closes. Users can add and view clients, add and view sessions, update session statuses, and delete sessions.

My purpose for writing this software is to develop my skills with cloud databases. I wanted to practice connecting Python to a remote database, organizing documents into collections, linking related records through document IDs, and implementing Create, Read, Update, and Delete operations.

To set up the application:

1. Install Python. This project was tested with Python 3.13.1.
2. Create a Firebase project and its Firestore database.
3. Save your Firebase service account credentials locally as `serviceAccountKey.json` beside `firebase_config.py`. Do not publish this file.
4. Create a virtual environment if you do not already have one:

   ```bash
   python3 -m venv .venv
   ```

5. Install the dependency and run the application from the project folder (macOS/Linux):

   ```bash
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python main.py
   ```

An internet connection and service account access to Firestore are required. Use fictional information only.

The menu repeats until you choose **7. Exit**:

1. **Add client:** enter a fictional first name, last name, phone number, and email.
2. **View clients:** display client records and their document IDs.
3. **Add session:** select an existing client by its displayed document ID, then enter a date (`YYYY-MM-DD`), time (`HH:MM`, 24-hour), session type, status, and optional fictional notes.
4. **View sessions:** display sessions and their document IDs.
5. **Update session status:** select a displayed session ID and choose its new status.
6. **Delete session:** select a displayed session ID to delete that session.
7. **Exit:** close the application.

Session type and status choices are numbered. Press Enter at a document ID prompt to cancel that operation. The program checks required text and menu choices; date and time formats are prompted but are not validated yet.

[Software Demo Video](https://youtu.be/RlRaoNZ6eMk)

# Cloud Database

The application uses Google Firebase Firestore, a NoSQL cloud database that organizes data into documents within collections. This project uses two collections:

| Collection | Fields |
| --- | --- |
| `clients` | `first_name`, `last_name`, `phone_number`, `email`, `date_created` |
| `sessions` | `client_id`, `client_name`, `session_date`, `session_time`, `session_type`, `status`, `notes`, `date_created` |

Firestore generates a unique document ID for each new record. A session's `client_id` contains the corresponding client document ID, and `client_name` stores the name selected when the session is created. Phone numbers, session dates, and session times are stored as text. The `date_created` field is a Firestore server timestamp.

Session types are `Individual`, `Couples`, `Premarital`, and `Follow-up`. Statuses are `Scheduled`, `Completed`, and `Cancelled`.

`firebase_config.py` uses the Python `firebase-admin` library to load the local service account file, initialize or reuse the Firebase Admin app, and expose the Firestore client as `db`. Credentials are not embedded in the Python source. The service account file is stored locally and listed in `.gitignore` to exclude it from Git and GitHub when the project is published. At the final local review, this folder was not yet a Git repository, so repository history and GitHub publication could not be verified.

The CRUD operations are:

- **Create:** `add_client()` writes a client to `clients`; `add_session()` writes a session to `sessions`.
- **Read:** `get_clients()` and `get_sessions()` return lists of dictionaries containing stored fields and an `id` field for each document ID.
- **Update:** `update_session_status()` changes only an existing session's `status` field and accepts only the three supported statuses.
- **Delete:** `delete_session()` removes the selected session document. A missing document returns `False` so the menu can explain that nothing was deleted.

Client creation and retrieval are supported. Client updates and deletion are not implemented. Database operations live in `client_service.py` and `session_service.py`; `main.py` handles user input, selection, and display.

# Development Environment

- **Visual Studio Code:** editor used to work with the Python project and terminal.
- **Python 3.13.1:** programming language used for functions, dictionaries, lists, input, and the menu loop.
- **Google Firebase:** cloud project and service account management.
- **Firestore:** cloud document database used to persist client and session records.
- **firebase-admin 7.7.0:** installed Python Firebase Admin SDK, pinned in `requirements.txt`, used for authentication and Firestore access. Its dependencies provide the Google API exception classes used in error handling.
- **Git:** version-control tool available locally; the project folder still needs repository setup.
- **GitHub:** intended location for publishing the source code and README; publication was not verified during the local review.

The `.venv` virtual environment isolates installed dependencies. `.gitignore` excludes the virtual environment, Python cache directories, compiled Python files, and the private service account file.

# Useful Websites

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK Documentation](https://firebase.google.com/docs/admin/setup)
- [Python Documentation](https://docs.python.org/3/)

# Future Work

- Add a web-based interface for managing fictional client and session records.
- Add more update options for client details and session details.
- Add user authentication and appropriate access controls.
- Validate date, time, phone, and email formats more thoroughly.
