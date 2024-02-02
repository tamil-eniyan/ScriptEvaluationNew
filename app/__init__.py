from flask import Flask
import secrets
from firebase_admin import credentials, firestore, initialize_app, storage

# GOOGLE_VISION_CREDENTIALS_PATH = "F:\Ganglia\ScriptEvaluationNeWW\ScriptEvaluationNew\google_vision_cred.json"
FIREBASE_CREDENTIALS_PATH = "C:/Ganglia/scriptEvalToken/credentials.json"

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)

firebase_app = initialize_app(cred, {
    'databaseURL': 'https://scriptevaluation.firebaseio.com/',
    'storageBucket': 'scriptevaluation.appspot.com', 
})

# initialize_app(cred, {'databaseURL': 'https://scriptevaluation.firebaseio.com/'})

db = firestore.client()
storage_client = storage

from app import routes
