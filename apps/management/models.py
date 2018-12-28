
from externs import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

'''
python manage.py db migrate
python manage.py db init
python manage.py db upgrade
'''


class UserRights(object):
    #bitmap 11111111
    ALLOWED_ALL = 0b11111111

    VISITOR = 0b00000001

    POSTER = 0b00000010

    COMMENTER = 0b00000100

    BOARDEF = 0b00001000

    FRONTUSER = 0b00010000

    ADMINER = 0b00100000

    DEVELOPER = ALLOWED_ALL

    NORIGHTS = 0b00000000


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


    @property
    def rights(self):
        if not self.roles:
            return UserRights.NORIGHTS

        all_rights = 0

        for role in self.roles:
            all_rights |= role.rights

        return all_rights


    def has_rights(self,rights):
        return (self.rights & rights) == rights

    @property
    def is_developer(self):
        return self.has_rights(UserRights.ALLOWED_ALL)

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


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    board_name = db.Column(db.String(20),nullable=False)
    #create_user = db.Column(db.String(50),nullable=False)
    create_time = db.Column(db.DATETIME,default=datetime.now)

