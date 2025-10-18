from flask import request, session
from database.operations import select, call_procedure
from database.sql_provider import SQLProvider

sql_provider = SQLProvider('blueprints/trolleybus/sql')


def bus_logic(db_config, args):
    sql_statement = ''

    arg_str = ''
    
    for item, value in list(args.items())[1:]:
        if value:
            arg_str += ' AND ' + str(item) + ' IN (\'' + str(value) + '\')'
    
    if args['request_type'] == 'timesheet':
        if request.method == 'POST':
            if arg_str == '':
                sql_statement = sql_provider.get('timesheet.sql', {})
            else:
                sql_statement = sql_provider.get('timesheet_search.sql', {'args': arg_str})
            result = select(db_config, sql_statement)
            
            config = {}
            if not('u_id' in session):
                config['true'] = 1
                config['messege'] = 'Вы не вошли в аккаунт'
                return result, config
            
            if request.form['count'] == '':
                config['true'] = 1
                config['messege'] = 'Вы не указали количество билетов!'
                return result, config
            
            elif int(request.form['count']) < 0:
                config['true'] = 1
                config['messege'] = 'Введите корректное количетсво билетов!'
                return result, config
            
            arg =  str(request.form['T_ID'])         + ', '
            arg += str(request.form['count'])        + ', '
            arg += str(session['u_id'])
            
            a =  call_procedure(db_config, 'add_ticket', arg)
            
            if '1' in a[0]:
                config['true'] = 1
                config['messege'] = 'Билетов нет'
                return result, config
            elif '0' in a[0]:
                config['true'] = 0
                config['messege'] = 'Билет добавлен в корзину'
                session['update_basket'] = 1
                return result, config
            
        else:
            if arg_str == '':
                sql_statement = sql_provider.get('timesheet.sql', {})
            else:
                sql_statement = sql_provider.get('timesheet_search.sql', {'args': arg_str})
    
    return select(db_config, sql_statement), 0