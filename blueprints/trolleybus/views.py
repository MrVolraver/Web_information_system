from blueprints.auth.db_login_get import dblogin
from flask import render_template

def view(html, result,  config):
    user_config = dblogin()
    return render_template(html, items=result, user_config=user_config, config=config)