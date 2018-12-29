
import constants
from .models import FrontUser
from .views import bp
from flask import session,g

@bp.before_request
def before_user_req():
    if constants.USER_ID in session:
        user_id = session.get(constants.USER_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.user = user

