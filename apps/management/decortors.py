
from functools import wraps
from flask import session,redirect,url_for,g
import constants

def login_required(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if constants.MANAGER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('manage.login'))

    return inner

def rights_check(rights):

    def outer(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.administrator
            if user.has_rights(rights):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('manage.index'))
        return inner
    return outer
