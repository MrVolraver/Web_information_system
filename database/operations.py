from database import connection


def select(db_config, _sql):
    with connection.DBContextManager(db_config) as cursor:
        if cursor:
            cursor.execute(_sql)
            schema = [column[0] for column in cursor.description]
            result = [dict(zip(schema, row)) for row in cursor.fetchall()]
            return result
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
        
def call_procedure(db_config, procedure, p_arg):
    with connection.DBContextManager(db_config) as cursor:
        if cursor:
            proc_sql = "CALL " + procedure + "(" + p_arg + ")"
            cursor.execute(proc_sql)
            schema = [column[0] for column in cursor.description]
            result = [dict(zip(schema, row)) for row in cursor.fetchall()]
            return result
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
