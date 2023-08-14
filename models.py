from flask_login import UserMixin
from db import db

class User(UserMixin, db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
