
from flask import Blueprint,render_template,views,request,redirect,url_for,session,flash,g
from .forms import LoginForm
from .models import Administrator
from .decortors import login_required
import constants

bp = Blueprint('manage',__name__,url_prefix='/manage')

@bp.route('/')
@login_required
def index():
    return render_template("management/index.html")

@bp.route('/')
@login_required
def logout():
    session.pop(key=constants.MANAGER_ID)
    return redirect(url_for('manage.login'))

'''
@bp.route('/login')
def login():
    return render_template("management/login.html")
'''

class LoginView(views.MethodView):

    def get(self,message=None):
        form = LoginForm()
        return render_template("management/login.html",form=form,message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            manager = Administrator.query.filter_by(email=email).first()

            if manager:
                if manager.check_password(password):
                    session[constants.MANAGER_ID] = manager.id
                    if remember:
                        session.permanent = True
                    return redirect(url_for('manage.index'))
                else:
                    #flash('Password error', 'err')
                    return render_template("management/login.html", message='User password error', form=form)
            else:
                #flash('User is not exist','err')
                return render_template("management/login.html",message='User is not exist', form=form)

        else:
            print(form.errors)
            message = form.errors.popitem()[1][0]
            return self.get(message)


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))