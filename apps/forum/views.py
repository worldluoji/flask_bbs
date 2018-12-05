

from flask import Blueprint,views,render_template

bp = Blueprint('forum',__name__,url_prefix='/forum')

@bp.route('/')
def index():
    return 'forum index'


class SignUpView(views.MethodView):
    def get(self):
        return render_template('forum/fuser_signup.html')

    def post(self):
        pass


bp.add_url_rule('/signup/',view_func=SignUpView.as_view('signup'))