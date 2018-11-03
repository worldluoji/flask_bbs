
from functools import wraps
from flask import session,redirect,url_for
import constants

def login_required(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if constants.MANAGER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('manage.login'))

    return inner