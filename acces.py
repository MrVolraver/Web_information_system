import typing as t
from functools import wraps
from blueprints.auth.db_login_get import dblogin
from flask import request, session, current_app, render_template

def group_validation(config: dict):
    endpoint_app = request.endpoint.split('.')
    flag = 0
    if 'u_role' in session:
        group = session['u_role']
        if group in config:
            for item in endpoint_app:
                if ('!' + item) in config[group]:
                    return False
                elif item in config[group]:
                    flag = 1
    if flag:
        return True
    else:
        return False


def login_required():
    def login_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            is_login = session.get("u_id", False)
            if is_login:
                if group_validation(current_app.config['access_config']):
                    result = func(*args, **kwargs)
                    return result
                else:
                    message = "Вы не имеете прав доступа"
                    user_config = dblogin()
                    return render_template('Error_form.html', message = message, user_config=user_config)
            else:
                message = "Вы не вошли в аккаунт"
                user_config = dblogin()
                return render_template('Error_form.html', message = message, user_config=user_config)
        return wrapper
    return login_wrapper