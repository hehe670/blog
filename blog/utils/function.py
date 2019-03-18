from functools import wraps
from flask import session, redirect, url_for


def ff(func):
    @wraps(func)
    def hh():

        user_id = session.get('user_id')
        if user_id:
            return func()
        else:
            return redirect(url_for('back.login'))

    return hh
