from blueprints.auth.db_login_get import dblogin
from database.operations import select
from flask import render_template, current_app, session
from database.sql_provider import SQLProvider

sql_provider = SQLProvider('blueprints/profile/sql')

def user_name():
    messege = {}
    login_dict = select(current_app.config['DB_CONFIG'], sql_provider.get('user_name.sql', {'id': session['u_id']}))
    messege['u_name'] = login_dict[0]['name']
    messege['u_surname'] = login_dict[0]['surname']
    return messege

def view(html, result, config):
    user_config = dblogin()
    u_name = user_name()
    return render_template(html, user_config=user_config, user_name=u_name, config=config, items=result)