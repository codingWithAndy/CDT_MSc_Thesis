import pyrebase


###### Firebase Connections ############

def connect_to_firebase():
    firebase_config = {
        "apiKey": "AIzaSyAjlnmPp71zTRrXhJ7kun_pzCXnZvLRt3A",
        "authDomain": "cj-app-e65ce.firebaseapp.com",
        "databaseURL": "https://cj-app-e65ce-default-rtdb.europe-west1.firebasedatabase.app/",
        "projectId": "cj-app-e65ce",
        "storageBucket": "cj-app-e65ce.appspot.com",
        "messagingSenderId": "407532536815",
        "appId": "1:407532536815:web:38c8c3ea2726122e0fac1a",
        "measurementId": "G-PTKRNCZJGB"
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