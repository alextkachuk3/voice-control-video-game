import pyrebase

from app.network.configs import confs

firebase = pyrebase.initialize_app(confs)
database = firebase.database()
