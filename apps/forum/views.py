
from flask import Blueprint,views,render_template,request,url_for,session
from .forms import SignupForm, SignInForm
from utils import restful
from .models import FrontUser
from externs import db
from utils.safeutils import is_safe_url
import constants
from apps.communal.models import BannerModel
from apps.management.models import Board

bp = Blueprint('forum',__name__,url_prefix='/forum')

@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = Board.query.all()
    context = {
        'banners': banners,
        'boards': boards
    }
    return render_template('forum/index.html', **context)

class SignUpView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if all([return_to, return_to != request.url, is_safe_url(return_to)]):
            return render_template('forum/fuser_signup.html', return_to=return_to)
        else:
            return render_template('forum/fuser_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate_on_submit():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success(message="You have registered to BSS successfully")
        else:
            return restful.param_error(message=form.get_error())

class SignInView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and is_safe_url(return_to):
            return render_template('forum/fuser_signin.html',return_to=return_to)
        else:
            return render_template('forum/fuser_signin.html')

    def post(self):
        form = SignInForm(request.form)
        if form.validate_on_submit():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[constants.USER_ID] = user.id
                print('view user id {}'.format(user.id))
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.param_error(message='telephone or password error')
        else:
            return restful.param_error(message=form.get_error())

bp.add_url_rule('/signup/',view_func=SignUpView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SignInView.as_view('signin'))