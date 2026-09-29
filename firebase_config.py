from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore


# Find the key beside this file, even when Python runs from another folder.
key_path = Path(__file__).resolve().parent / "serviceAccountKey.json"

# Reuse the default Firebase app if it has already been initialized.
try:
    app = firebase_admin.get_app()
except ValueError:
    # Credentials stay in the private key file, not in our Python code.
    credential = credentials.Certificate(str(key_path))
    app = firebase_admin.initialize_app(credential)

# Other Python files can use: from firebase_config import db
db = firestore.client(app=app)
