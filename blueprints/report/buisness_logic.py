from flask import request
from database.operations import select, call_procedure
from database.sql_provider import SQLProvider
from datetime import datetime

sql_provider = SQLProvider('blueprints/report/sql')

def bus_logic_create(db_config, args):
    
    if args['request_type'] == 'create_report/about_date':
        if request.method == 'POST':
            config = {}
            
            if str(request.form['Entry_date']) > str(request.form['Exit_date']):
                config['true'] = 1
                config['messege'] = 'Введите корректные даты'
                return config
            elif str(request.form['Entry_date']) < '1000-01-01' or str(request.form['Exit_date']) > str(datetime.now().date()):
                config['true'] = 1
                config['messege'] = 'Можно указать даты от 1000-01-01 до ' +  str(datetime.now().date())
                return config
            
            arg =  '\'' + str(request.form['Entry_date'])         + '\', '
            arg += '\'' + str(request.form['Exit_date'])         + '\''
            if 'col_drivers' in request.form:
                arg += ', ' + '1'
            else:
                arg += ', ' + '0'
            if 'col_bilet' in request.form:
                arg += ', ' + '1'
            else:
                arg += ', ' + '0'
            if 'total_sum' in request.form:
                arg += ', ' + '1'
            else:
                arg += ', ' + '0'
            if 'total_people' in request.form:
                arg += ', ' + '1'
            else:
                arg += ', ' + '0'
            
            a = call_procedure(db_config, 'otchet_date', arg)
            
            if '0' in a[0]:
                config['true'] = 0
                config['messege'] = 'Отчет успешно добавлен'
                return config
            elif '1' in a[0]:
                config['true'] = 0
                config['messege'] = 'Запись обновлена'
                return config
        
    elif args['request_type'] == 'create_report/about_drivers':
        if request.method == 'POST':
            config = {}
            
            if  str(request.form['years'])=='' or str(request.form['months'])=='':
                config['true'] = 1
                config['messege'] = 'Заполните все поля'
                return config
            elif not(request.form['years'].isdigit() and request.form['months'].isdigit()):
                config['true'] = 1
                config['messege'] = 'Введите корректные значения'
                return config
            elif int(request.form['years']) > datetime.now().year or int(request.form['years']) < 2000:
                config['true'] = 1
                config['messege'] = 'Неверно указан год'
                return config
            elif int(request.form['months']) < 0 or int(request.form['months']) > 12:
                config['true'] = 1
                config['messege'] = 'Неверно указан месяц'
                return config
            
            arg =  str(request.form['years'])         + ', '
            arg += str(request.form['months'])
                
            a = call_procedure(db_config, 'otchet_driver', arg)
            
            if '1' in a[0]:
                config['true'] = 0
                config['messege'] = 'Отчет успешно добавлен'
                return config
            elif '0' in a[0]:
                config['true'] = 1
                config['messege'] = 'Такой отчет уже существует'
                return config
    else:
        return 0
    
    return 0

def bus_logic_read(db_config, args):
    
    if args['request_type'] == 'read_report':
        total = {}
        
        sql_statement = sql_provider.get('driver_report.sql', {})
        total['report_driver'] = select(db_config, sql_statement)

        sql_statement = sql_provider.get('date_report.sql', {})
        total['report_date'] = select(db_config, sql_statement)
        
        #sql_statement = sql_provider.get('driver_report_all.sql', {})
        #total['report_all_drivers'] = select(db_config, sql_statement)
        
        return total
        
    return 0