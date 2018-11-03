
import constants
from .models import Administrator
from flask import session,g
from .views import bp

@bp.before_request
def bef_request():
    if constants.MANAGER_ID in session:
        manager_id = session.get(constants.MANAGER_ID)
        administrator = Administrator.query.get(manager_id)
        if administrator:
            g.administrator = administrator
