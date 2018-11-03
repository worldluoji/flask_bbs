
from externs import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

'''
python manage.py db migrate
python manage.py db init
python manage.py db upgrade
'''


class Administrator(db.Model):
    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    reg_time = db.Column(db.DATETIME, default=datetime.now)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password    # do password.setter
        self.email = email

    def __str__(self):
        return self.username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,password):
        self._password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)