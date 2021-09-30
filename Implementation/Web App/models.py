import pyrebase
from firebase_details import link_to_firebase




###### Firebase Connections ############

def connect_to_firebase():
    firebase_config = link_to_firebase()

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