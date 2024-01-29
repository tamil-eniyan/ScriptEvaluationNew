from flask import Flask
import secrets
from firebase_admin import credentials, firestore, initialize_app, storage

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
cred = credentials.Certificate("C:/Ganglia/scriptEvalToken/credentials.json")

firebase_app = initialize_app(cred, {
    'databaseURL': 'https://scriptevaluation.firebaseio.com/',
    'storageBucket': 'scriptevaluation.appspot.com', 
})

# initialize_app(cred, {'databaseURL': 'https://scriptevaluation.firebaseio.com/'})

db = firestore.client()
storage_client = storage

from app import routes
