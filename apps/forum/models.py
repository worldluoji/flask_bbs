
from externs import db
import shortuuid
from werkzeug.security import check_password_hash,generate_password_hash
from enum import Enum
from datetime import datetime


class GenderEnum(Enum):
    MALE = 1
    FMEAL = 2
    SECRET = 3


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)   #short uuid is efficient and unique
    telephone = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.SECRET)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,*args,**kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser,self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,new_passwd):
        self._password = generate_password_hash(new_passwd)

    def check_password(self,passwd):
        return check_password_hash(self._password,passwd)


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    board_name = db.Column(db.String(20), nullable=False)
    #create_user = db.Column(db.String(50),nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship("Board", backref="posts")

    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    author = db.relationship('FrontUser', backref='posts')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)

    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    author = db.relationship('FrontUser', backref='comments')

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='comments')


class HighLightPost(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    create_time = db.Column(db.DATETIME, default=datetime.now)
    post = db.relationship("Post", backref="highlight")
