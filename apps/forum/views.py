
from flask import Blueprint,views,render_template,make_response
from utils.captcha import xtcaptcha
from io import BytesIO
from utils import memcache_operate

bp = Blueprint('forum',__name__,url_prefix='/forum')

@bp.route('/')
def index():
    return 'forum index'


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


class SignUpView(views.MethodView):
    def get(self):
        return render_template('forum/fuser_signup.html')

    def post(self):
        pass


bp.add_url_rule('/signup/',view_func=SignUpView.as_view('signup'))