

from flask import Blueprint

bp = Blueprint('forum',__name__,url_prefix='/forum')

@bp.route('/')
def index():
    return 'forum index'