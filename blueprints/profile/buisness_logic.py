from flask import request, current_app, session
from database.operations import select,  call_procedure
from database.sql_provider import SQLProvider

sql_provider = SQLProvider('blueprints/profile/sql')


def bus_logic(db_config, args):
    sql_statement = ''

    arg_str = ''
    
    for item, value in list(args.items())[1:]:
        if value:
            arg_str += ' AND ' + str(item) + ' IN (\'' + str(value) + '\')'

    if args['request_type'] == 'timesheet':
        if arg_str == '':
            arg_str = ' AND idlogin_password = ' + str(session['u_id'])
            sql_statement = sql_provider.get('timesheet_search.sql', {'args': arg_str})
        else:
            arg_str += ' AND idlogin_password =' + str(session['u_id'])
            sql_statement = sql_provider.get('timesheet_search.sql', {'args': arg_str})
    
    if args['request_type'] == 'add_timesheet':
        if request.method == 'POST':
            config = {}
            
            D_ID = []
            R_ID = []

            for i in select(db_config, sql_provider.get('all_drivers.sql', {})):
                D_ID.append(i['D_ID'])
            for i in select(db_config, sql_provider.get('all_routes.sql', {})):
                R_ID.append(i['R_ID'])
            
            if str(request.form['Exit_date']) < str(request.form['Entry_date']):
                config['true'] = 1
                config['messege'] = 'Введите корректные значения дат'
                return config
            
            elif request.form['D_ID'] =='' or request.form['R_ID'] =='' or request.form['trol_num']=='' or request.form['col_bilet'] =='':
                config['true'] = 1
                config['messege'] = 'Заполните все поля'
                return config
            
            elif not(request.form['D_ID'].isdigit() and request.form['R_ID'].isdigit() and request.form['trol_num'].isdigit() and request.form['col_bilet'].isdigit()):
                config['true'] = 1
                config['messege'] = 'Введите корректные значения'
                return config
            
            elif not(int(request.form['D_ID']) in D_ID):
                config['true'] = 1
                config['messege'] = 'Нет такого водителя'
                return config
            
            elif not(int(request.form['R_ID']) in R_ID):
                config['true'] = 1
                config['messege'] = 'Нет такого маршрута'
                return config
                
                
            args =  '\'' + str(request.form['t_date'])         + '\', '
            args += '\'' + str(request.form['t_date']) + '-' + str(request.form['Entry_date'])   + '\', '
            args += '\'' + str(request.form['t_date']) + '-' + str(request.form['Exit_date'])    + '\', '
            args +=  str(request.form['D_ID'])         + ', '
            args +=  str(request.form['R_ID'])         + ', '
            args += str(request.form['trol_num'])      + ', '
            args += str(request.form['col_bilet'])
            
            print(args)
            
            a = call_procedure(current_app.config['DB_CONFIG'], 'add_timesheet', args)
            if '1' in a[0]:
                config['true'] = 0
                config['messege'] = 'Расписание успешно добавлено'
                return config
            elif '0' in a[0]:
                config['true'] = 1
                config['messege'] = 'Такое расписание уже существует'
                return config
        else:
            return 0
    
    if args['request_type'] == 'my_routes':
        if arg_str == '':
            arg_str = ' AND id_user = ' + str(session['u_id'])
            sql_statement = sql_provider.get('my_routes.sql', {'args': arg_str})
        else:
            arg_str += ' AND id_user =' + str(session['u_id'])
            sql_statement = sql_provider.get('my_routes.sql', {'args': arg_str})
    
    if args['request_type'] == 'my_drivers':
        sql_statement = sql_provider.get('my_drivers.sql', {})
        
    if args['request_type'] == 'history_routes':
        result = []
    
        arg_str = ' AND user_id1 =' + str(session['u_id'])
        
        for item, value in list(args.items())[1:]:
            if value:
                arg_str += ' AND ' + str(item) + ' IN (\'' + str(value) + '\')'
                
        sql_statement = sql_provider.get('history_orders.sql', {'args': arg_str})
        result.append(select(db_config, sql_statement))
        
        arg_str = ' AND user_id1 =' + str(session['u_id'])
        
        if 'R_name' in args:
            if args['R_name']!='':
                arg_str += ' AND R_name IN (\'' + str(args['R_name']) + '\')'
        
        sql_statement = sql_provider.get('history_order_details.sql', {'args': arg_str})
        result.append(select(db_config, sql_statement))
        return result

    return select(db_config, sql_statement)