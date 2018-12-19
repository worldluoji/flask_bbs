
from flask import Blueprint,make_response,jsonify
from utils.captcha import xtcaptcha
from io import BytesIO
from utils import memcache_operate
import qiniu
import config

bp = Blueprint('communal',__name__,url_prefix='/communal')

@bp.route('/')
def index():
    return 'communal index'


'''
blue print in views, and imported by __init__.py
'''


@bp.route('/image_captcha/')
def image_captcha():
    text,image = xtcaptcha.Captcha.gene_code()
    out = BytesIO();
    image.save(out,'png')
    out.seek(0)

    resp = make_response(out.read())
    resp.content_type = 'image/png'
    memcache_operate.set(text.lower(),text.lower(),timeout=2*68)

    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = config.QINIU_ACCESS_KEY
    secret_key = config.QINIU_SECRET_KEY
    auth = qiniu.Auth(access_key,secret_key)
    storage_space_name = config.QINIU_STORAGE_SPACE
    token = auth.upload_token(storage_space_name)
    return jsonify({"uptoken":token})
