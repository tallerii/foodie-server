import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('foodie/firebase-key.json')
firebaseApp = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://foodie-9c1e7.firebaseio.com/'
})
