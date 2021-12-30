import sqlite3


def query_db(db, query, params=None):
    '''

    :param db: route to the db directory
    :param query: query in SQL
    :param params: parameters of the SQL query
    :return: result of the query
    '''
    if params is None:
        params = ()

    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        result = cursor.execute(query, params)
        connection.commit()
    return result


def create_fund_db(db, fund_name):
    if fund_name == '':
        return
    query = f'CREATE TABLE {fund_name} (Id INTEGER NOT NULL PRIMARY KEY, Fecha	TEXT NOT NULL, Aporte REAL NOT NULL, Participaciones REAL NOT NULL, Valor_participacion REAL NOT NULL)'
    # parameters = (fund_name)
    query_db(db, query)
