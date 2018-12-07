
from flask import Blueprint,make_response
from utils.captcha import xtcaptcha
from io import BytesIO
from utils import memcache_operate

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
