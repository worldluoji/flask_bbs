
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
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)   #short uuid is efficient and unique
    telephone = db.Column(db.String(50),nullable=False,unique=True)
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum),default=GenderEnum.SECRET)
    join_time = db.Column(db.DateTime,default=datetime.now)

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