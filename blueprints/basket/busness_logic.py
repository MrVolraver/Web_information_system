from flask import request, current_app, session
from database.operations import select,  call_procedure
from database.sql_provider import SQLProvider
import redis, time

sql_provider = SQLProvider('blueprints/basket/sql')

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def flush_redis():
    r.flushdb()
    return 0

def update_redis():
    if (not('update_basket' in session)) or (session['update_basket'] == 1):
        arg_str = ' AND user_id IN (\'' + str(session['u_id']) + '\')'
        sql_code = sql_provider.get('my_basket.sql', {'args': arg_str})
        items = select(current_app.config['DB_CONFIG'], sql_code)
        print(items)
        for item in items:
            r.hset(item['ticket_id'], "R_name", item['R_name'])
            r.hset(item['ticket_id'], "price", item['price'])
            r.hset(item['ticket_id'], "count", item['count'])
            r.hset(item['ticket_id'], "Entry_date", str(item['TIME(Entry_date)']))
            r.hset(item['ticket_id'], "T_date", str(item['DATE(T_date)']))
            r.hset(item['ticket_id'], "T_ID", item['ticket_id'])
            r.expire(item['ticket_id'], 60)
    items={}
    for i in sorted(r.keys("*")):
        items[i] = (r.hgetall(i))
    session['update_basket'] = 0
    return items

def bus_logic(db_config, args):

    if args['request_type'] == '':
        config = {}
        result = update_redis()
        return result, config
    
    if args['request_type'] == 'clear':
        config = {}
        arg = str(session['u_id'])
        call_procedure(db_config, 'delete_basket', arg)
        session['update_basket'] = 1
        flush_redis()
        config['true'] = 0
        config['messege'] = 'Корзина успешно очищена'
        return 0
    
    if args['request_type'] == 'buy':
        config = {}
        
        if request.method == 'POST':
            arg_str = ' AND T_ID IN (' + str(request.form.getlist('T_ID'))[1:-1] + ')'
            sql_statement = sql_provider.get('count_tickets.sql', {'args': arg_str})
            count_tickets = select(current_app.config['DB_CONFIG'], sql_statement)
            req = dict(zip(request.form.getlist('T_ID'), request.form.getlist('count')))
            
            for item in count_tickets:
                if int(item['remain_count_ticket']) < int(req[str(item['T_ID'])]):
                    config['true'] = 1
                    config['messege'] = 'Недостаточно билетов. Заказ отменен.'
                    session['update_basket'] = 0
                    return 0, config
            
            arg = str(session['u_id']) + ', ' + str(request.form.get('total_sum'))
            
            order_id = call_procedure(db_config, 'create_order', arg)
            
            for tid, count in zip(request.form.getlist('T_ID'), request.form.getlist('count')):
                arg = str(order_id[0]['LAST_INSERT_ID()']) + ', ' + str(tid) + ', ' + str(count)
                call_procedure(db_config, 'create_order_details', arg)
                
            config['true'] = 0
            config['messege'] = 'Заказ успешно создан'
            
            session['update_basket'] = 1
            flush_redis()
            return 0, config
            
        else:
            dict1 = {}
            tid = []
            for item in args:
                if args[item] == 'ADD':
                    tid.append(item)
            for item in tid:
                dict1[str(item)] = args['count '+str(item)]
            arg_str  = ' AND user_id IN (\'' + str(session['u_id']) + '\')'
            arg_str += ' AND ticket_id IN (' + str(tid)[1:-1] + ')'
            sql_statement = sql_provider.get('my_basket.sql', {'args': arg_str})
            items = select(current_app.config['DB_CONFIG'], sql_statement)
            for item in items:
                item['count'] = dict1[str(item['ticket_id'])]
            total_sum = 0
            for item in items:
                total_sum += int(item['count']) * int(item['price'])
            items[0]['total_sum'] = total_sum
            
        return items, config
    
    return select(db_config, sql_statement)