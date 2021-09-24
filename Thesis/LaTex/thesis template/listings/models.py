import pyrebase


def connect_to_firebase():
    firebase_config = {
        "apiKey": "Removed",
        "authDomain": "Removed",
        "databaseURL": "Removed",
        "projectId": "Removed",
        "storageBucket": "Removed",
        "messagingSenderId": "Removed",
        "appId": "Removed",
        "measurementId": "Removed"
    }

    firebase = pyrebase.initialize_app(firebase_config)

    return firebase


def init_db():
    firebase = connect_to_firebase()
    firebase_db = firebase.database()

    return firebase_db


def init_auth():
    firebase = connect_to_firebase()
    firebase_auth = firebase.auth()

    return firebase_auth


def init_storage():
    firebase = connect_to_firebase()
    firebase_storage = firebase.storage()

    return firebase_storage