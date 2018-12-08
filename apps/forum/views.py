
from flask import Blueprint,views,render_template,request,url_for
from .forms import SignupForm
from utils import restful
from .models import FrontUser
from externs import db
from utils.safeutils import is_safe_url


bp = Blueprint('forum',__name__,url_prefix='/forum')

@bp.route('/')
def index():
    return render_template('forum/index.html')

class SignUpView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if all([return_to, return_to != url_for('forum.signup'), is_safe_url(return_to)]):
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
        return render_template('forum/fuser_signin.html')

    def post(self):
        pass

bp.add_url_rule('/signup/',view_func=SignUpView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SignInView.as_view('signin'))