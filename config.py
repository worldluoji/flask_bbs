import os

DEBUG = True

DB_USER = 'luoji'
DB_PASS = 'Password@199114'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'flask_bbs'

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


#QINIUYUN
QINIU_ACCESS_KEY = 'sT9h81_RCdaeVesZ2xhN0OYjxfzmRssQ13crpnZO'
QINIU_SECRET_KEY = '0dKrQne19F2ZK1DnLy8kBDILvc1p5qV9oIUo5tni'
QINIU_STORAGE_SPACE = 'luojivideo'


#UEditor
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "sT9h81_RCdaeVesZ2xhN0OYjxfzmRssQ13crpnZO"
UEDITOR_QINIU_SECRET_KEY = "0dKrQne19F2ZK1DnLy8kBDILvc1p5qV9oIUo5tni"
UEDITOR_QINIU_BUCKET_NAME = "luojivideo"
UEDITOR_QINIU_DOMAIN = "http://pjzlzc41u.bkt.clouddn.com/"

#flask-paginate
POSTS_PER_PAGE = 9

#CELERY
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"