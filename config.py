import os

DEBUG = True

DB_USER = 'luoji'
DB_PASS = 'Password@199114'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'bbs'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USER,DB_PASS,DB_HOST,DB_PORT,DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

#if you don't set this parameter, the default value is 31 days
#PERMANENT_SESSION_LIFETIME = 31

SECRET_KEY = os.urandom(24)


#FLASK MAIL
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
#MAIL_USE_SSL: default
MAIL_USERNAME = "1132416@qq.com"
MAIL_PASSWORD = "pomozgmjpktpbjgj"
MAIL_DEFAULT_SENDER = "1132416@qq.com"




#MEMCACHE
MEMCACHE_HOST = '127.0.0.1:11211'


