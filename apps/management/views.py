
from flask import Blueprint,render_template,views,request,redirect,url_for,session,flash,g,jsonify
from .forms import LoginForm,Resetpwdform,ResetEmailForm,AddBannerForm,EditBannerForm,AddBoardForm,EditBoardForm
from .models import Administrator,UserRights
from .decortors import login_required,rights_check
from externs import db
import constants
from utils import restful
from flask_mail import Message
from externs import mail
from constants import CAPTCHA_SOURCE
import random
from utils import memcache_operate
from apps.communal.models import BannerModel
from apps.forum.models import Board

bp = Blueprint('manage',__name__,url_prefix='/manage')

@bp.route('/')
@login_required
def index():
    return render_template("management/index.html")

@bp.route('/logout')
@login_required
def logout():
    session.pop(key=constants.MANAGER_ID)
    return redirect(url_for('manage.login'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('management/profile.html')
'''
@bp.route('/login')
def login():
    return render_template("management/login.html")
'''
@bp.route('/email/')
def send_email():
    msg = Message('email send',recipients=['wolong_haha@163.com'],body='test')
    mail.send(msg)
    return 'success'


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if email:
        captcha = ''.join(random.sample(CAPTCHA_SOURCE,6))
        msg = Message('FLASK BBS CAPTCHA',recipients=[email],body=captcha)
        try:
            mail.send(msg)
        except:
            return restful.server_error()

        memcache_operate.set(email,captcha)
        return restful.success('send captcha to {} successfully'.format(email))
    else:
        return restful.param_error('please input email')




@bp.route('/adminusers/')
@login_required
@rights_check(UserRights.ADMINER)
def adminusers():
    return render_template('management/adminusers.html')


@bp.route('/comments/')
@login_required
@rights_check(UserRights.COMMENTER)
def comments():
    return render_template('management/comments.html')

@bp.route('/frontusers/')
@login_required
@rights_check(UserRights.FRONTUSER)
def frontusers():
    return render_template('management/frontusers.html')

@bp.route('/posts/')
@login_required
@rights_check(UserRights.POSTER)
def posts():
    return render_template('management/posts.html')

@bp.route('/roles/')
@login_required
@rights_check(UserRights.ALLOWED_ALL)
def roles():
    return render_template('management/roles.html')

@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('management/banners.html', banners=banners)

@bp.route('/add_banner/', methods=['POST'])
@login_required
def add_banner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.param_error(form.get_error())

@bp.route('/edit_banner/', methods=['POST'])
@login_required
def edit_banner():
    form = EditBannerForm(request.form)
    if form.validate():
        id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.add(banner)
            db.session.commit()
            return restful.success()
        return restful.param_error(message='There is no this banner')
    else:
        return restful.param_error(form.get_error())

@bp.route('/del_banner/',methods=['POST'])
@login_required
def del_banner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.param_error(message='banner id missing')

    banner = BannerModel.query.get(banner_id)

    if banner:
        db.session.delete(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.param_error(message='There is no this banner')

@bp.route('/add_board/', methods=['POST'])
@login_required
@rights_check(UserRights.BOARDEF)
def add_board():
    form = AddBoardForm(request.form)
    if form.validate():
        board_name = form.board_name.data
        board = Board(board_name=board_name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.param_error(form.get_error())

@bp.route('/edit_board/', methods=['POST'])
@login_required
@rights_check(UserRights.BOARDEF)
def edit_board():
    form = EditBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        board = Board.query.get(board_id)
        if board:
            board.board_name = form.board_name.data
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(form.get_error(message='There is no this board'))
    else:
        return restful.param_error(form.get_error())

@bp.route('/del_board/', methods=['POST'])
@login_required
@rights_check(UserRights.BOARDEF)
def del_board():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.param_error(message='Please input board id')

    board = Board.query.get(board_id)
    if board:
        db.session.delete(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.param_error(message='There is no this board')

@bp.route('/boards/')
@login_required
@rights_check(UserRights.BOARDEF)
def boards():
    total_boards = Board.query.all()
    return render_template('management/boards.html',boards=total_boards)

class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template("management/login.html",message=message)

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
                    return render_template("management/login.html", message='User password error')
            else:
                #flash('User is not exist','err')
                return render_template("management/login.html",message='User is not exist')

        else:
            print(form.errors)
            message = form.errors.popitem()[1][0]
            return self.get(message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("management/resetpwd.html")

    def post(self):
        form = Resetpwdform(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data

            if oldpwd == newpwd:
                return restful.param_error('New password can`t be the same with old password')

            adminer = g.administrator
            print(adminer)
            print(adminer.password)
            print(oldpwd)
            print(adminer.check_password(oldpwd))
            if adminer.check_password(oldpwd):
                adminer.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.param_error('previous password error')
        else:
            return restful.param_error(form.get_error())

class ResetEmailView(views.MethodView):

    decorators = [login_required]

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.administrator.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(message=form.get_error())

    def get(self):
        return render_template("management/resetemail.html")



bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))

