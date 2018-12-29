
from functools import wraps
from flask import session,redirect,url_for,g
import constants

def login_required(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if constants.USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('forum.index'))

    return inner
