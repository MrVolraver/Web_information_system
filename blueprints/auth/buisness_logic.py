from database.operations import select, call_procedure
from database.sql_provider import SQLProvider
from flask import request, current_app, session

sql_provider = SQLProvider('blueprints/auth/sql')

def registr():
    config = {}
    if request.method == 'POST':
        if len(request.form['password']) < 8:
            config['true'] = 1
            config['messege'] = 'Пароль должен содержать не менее 8 символов!'
            return config
        args = '\'' + str(request.form['login']) + '\', \'' + str(request.form['password']) + '\', \'' + str(request.form['name']) + '\', \'' + str(request.form['surname']) + '\''
        a = call_procedure(current_app.config['DB_CONFIG'], 'registration', args)
        if '1' in a[0]:
            config['true'] = 0
            config['messege'] = 'Аккаунт успешно  создан'
            return config
        else:
            config['true'] = 1
            config['messege'] = 'Имя пользователя уже используется'
            return config
    return config

def login():
    login_dict = select(current_app.config['DB_CONFIG'], sql_provider.get('login.sql', {}))
    if request.method == 'POST':
        for i in login_dict:
            if (i['u_login'] == request.form.get('u_login')) and (i['u_password'] == request.form.get('u_password')):
                session['u_id'] = i['idlogin_password']
                session['u_role'] = i['u_role']
                return '200'
        return '401'
    else:
        if 'u_role' in session:
            return '200'
        else:
            return '4011'
    return '200'