
from flask import Blueprint, views, render_template, request, url_for, session, g, abort
from .forms import SignupForm, SignInForm, PubPostForm, AddCommentForm
from utils import restful
from .models import FrontUser, Board, Post, Comment, HighLightPost
from externs import db
from utils.safeutils import is_safe_url
import constants
from apps.communal.models import BannerModel
from .decortors import login_required
from flask_paginate import Pagination, get_page_parameter
import config
from sqlalchemy.sql import func

bp = Blueprint('forum', __name__, url_prefix='/forum')

@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = Board.query.all()

    #/?page=xxx
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.POSTS_PER_PAGE
    end = start + config.POSTS_PER_PAGE

    query = None
    classification = request.args.get("classification", type=int, default=0)
    if classification == 0:
        #按照创建时间新的帖子在前面
        query = Post.query.order_by(Post.create_time.desc())
    elif classification == 1:
        #按照精华帖子创建时间排序，如果不是精华帖子，则按照帖子创建时间排序, outerjoin默认是left join
        query = db.session.query(Post).outerjoin(HighLightPost).order_by(HighLightPost.create_time.desc(),
                                                                         Post.create_time.desc())
    elif classification == 2:
        #TODO 按照点赞数
        query = Post.query.order_by(Post.create_time.desc())
    else:
        #按照评论数排序
        query = db.session.query(Post).outerjoin(Comment).group_by(Post.id).order_by(func.count(Comment.id).desc(),
                                                                                     Post.create_time.desc())

    board_id = request.args.get("board_id", type=int, default=None)
    if board_id:
        query_base = query.filter(Post.board_id == board_id)
        pagination = Pagination(page=page, total=query_base.count(), bs_version=3)
        posts = query_base.slice(start, end)
    else:
        pagination = Pagination(page=page, total=query.count(), bs_version=3)
        posts = query.slice(start, end)

    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_classification': classification
    }
    return render_template('forum/index.html', **context)

@bp.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)

    if not post:
        abort(404)

    return render_template('forum/post_detail.html', post=post)


@bp.route('/ppost/', methods=['GET', 'POST'])
@login_required
def publish_post():
    if request.method == 'GET':
        boards = Board.query.all()
        return render_template('forum/publish_post.html',boards=boards)
    else:
        form = PubPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = Board.query.get(board_id)
            if not board:
                return restful.param_error(message='There is no this board')

            post = Post(title=title,content=content,board_id=board_id)
            post.author_id = g.user.id
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error(message=form.get_error())


@bp.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = Post.query.get(post_id)
        if not post:
            return restful.param_error(message='This post is not exist')
        author = g.user
        comment = Comment(content=content, post=post, author=author)
        db.session.add(comment)
        db.session.commit()
        return restful.success()
    else:
        return restful.param_error(form.get_error())

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