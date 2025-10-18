from database.sql_provider import SQLProvider
from database.operations import select
from flask import current_app, session


sql_provider = SQLProvider('blueprints/auth/sql')

def dblogin():
    messege = {}
    if 'u_id' in session:
        id = session['u_id']
        login_dict = select(current_app.config['DB_CONFIG'], sql_provider.get('login_get.sql', {'id': id}))
        messege['u_role'] = login_dict[0]['u_role']
        messege['u_login'] = login_dict[0]['u_login']
    return messege