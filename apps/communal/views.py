
from flask import Blueprint

bp = Blueprint('communal',__name__,url_prefix='/communal')

@bp.route('/')
def index():
    return 'communal index'


'''
blue print in views, and imported by __init__.py
'''