
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


class UserRights(object):
    #bitmap 11111111
    ALLOWED_ALL = 0b11111111

    VISITOR = 0b00000001

    POSTER = 0b00000010

    COMMENTER = 0b00000100

    BOARDEF = 0b00001000

    FRONTUSER = 0b00010000

    ADMINER = 0b00100000

    DEVELOPER = 0b01000000


adminer_role = db.Table(
    'adminer_role_table',
    db.Column('role_id',db.Integer,db.ForeignKey('role.id'),primary_key=True),
    db.Column('admin_id',db.Integer,db.ForeignKey('administrator.id'),primary_key=True)
)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(150), nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    rights = db.Column(db.Integer,default=UserRights.VISITOR)
    users = db.relationship('Administrator', secondary=adminer_role, backref="roles")

    def __str__(self):
        return self.name