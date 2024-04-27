import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./admin.secret.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.Client()