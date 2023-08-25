from flask_bcrypt import Bcrypt
from mongoengine import Document, StringField

bcrypt = Bcrypt()

class User(Document):
    username = StringField(unique=True, required=True)
    password_hash = StringField(required=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

