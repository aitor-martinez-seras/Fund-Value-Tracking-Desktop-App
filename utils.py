import sqlite3
from constants import *
from tkinter import *


# Functions related to the database

def query_db(db, query, params=None):
    '''
    Makes a query to the database
    :param db: string with the route to the database
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


def create_deposit(db, entries):
    query = f'''INSERT INTO {entries['fund']} 
                VALUES (NULL, ?, ?, ?, ?)'''
    # The value of each participation at the time of the deposit
    participation_value = entries['deposit'] / entries['participations']
    parameters = (entries['date'], entries['deposit'], entries['participations'], participation_value)
    query_db(db, query, parameters)
    return


def create_fund_db(db, fund_name):
    '''
    Function to create the table of a fund in the database
    :param db: string with the route to the database
    :param fund_name: string with the desired name for the table in the database
    '''
    query = f'CREATE TABLE {fund_name} ({DB_COLUMNS[0]} INTEGER NOT NULL PRIMARY KEY, {DB_COLUMNS[1]}	TEXT NOT NULL, ' \
            f'{DB_COLUMNS[2]} REAL NOT NULL, {DB_COLUMNS[3]} REAL NOT NULL, {DB_COLUMNS[4]} REAL NOT NULL)'
    query_db(db, query)


def edit_fund(db, old_name: str, new_name: str):
    '''
    Edits the name of a table of the database
    :param db:
    :param new_name:
    :return:
    '''
    query = f'ALTER TABLE {old_name} RENAME TO {new_name}'
    query_db(db, query)


def delete_fund_from_db(db, name):
    query = f'DROP TABLE {name}'
    query_db(db, query)


def get_available_funds(db):
    '''
    Gets the table names that represent each fund
    :return: List of strings
    '''
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    query = query_db(db, query)
    funds = []
    for element in query:
        if element[0] != 'sqlite_sequence':
            funds.append(element[0])
    return funds


def get_deposits_of_a_fund(db, fund_name, dates=None):
    """
    Creates a dict with the deposits that correspond to the fund and that happened between the indicated dates. If
    no dates are passed, last 15 deposits are retrieved, if 'All' is passed, all the deposits are retrieved
    :param db:
    :param fund_name:
    :param dates:
    :return:
    """
    if dates is None:
        # FALTA DE AÑADIR QUE EN LA QUERY SOLO COJA LOS ULTIMOS 15
        query = f"SELECT * FROM {fund_name}"
    elif dates == 'All':
        query = f"SELECT * FROM {fund_name}"
    else:
        query = f"SELECT * FROM {fund_name} WHERE ____"
    query = query_db(db, query)
    deposits = parse_deposits(query)
    print(deposits)
    return deposits


def parse_deposits(query_object: sqlite3.Cursor) -> dict:
    """
    Creates a dict of list where each key is a column of the list is one row of the table
    :param query_object:
    :return:
    """
    '''
    deposits = {
        'Id': [],
        'Fecha': [],
        'Aporte': [],
        'Participaciones': [],
        'Valor_participacion': []
    }
    for element in query_object:
        deposits['Id'].append(element[0])
        deposits['Fecha'].append(element[1])
        deposits['Aporte'].append(element[2])
        deposits['Participaciones'].append(element[3])
        deposits['Valor_participacion'].append(element[4])
    '''
    deposits = []
    for element in query_object:
        deposits.append(element)
    return deposits


# Validation functions

def validate_name(name: str):
    """
    Checks that the introduced value is not only numeric, is nonzero,
has no spaces in it and that length is not superior to 30
    :param name: String
    :return: True if valid
    """
    return (len(name) != 0) and not (' ' in name) and (len(name) < 30) and not name.isnumeric()


def validate_number(number):
    return (100000000 > number > 0.0)


def validate_date(date):
    try:
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
    except ValueError:
        return False
    return (1950 < year < 2100) and (0 <= month <= 12) and (0 <= day <= 31)
