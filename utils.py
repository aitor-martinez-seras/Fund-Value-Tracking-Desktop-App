import sqlite3
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
    query = f'CREATE TABLE {fund_name} (Id INTEGER NOT NULL PRIMARY KEY, Fecha	TEXT NOT NULL, Aporte REAL NOT NULL, Participaciones REAL NOT NULL, Valor_participacion REAL NOT NULL)'
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


# Validation functions

def validate_name(name: str):
    """
    Checks that the introduced value is not only numeric, is nonzero,
has no spaces in it and that length is not superior to 30
    :param name: String
    :return: True if valid
    """
    return (len(name) != 0) and not(' ' in name) and (len(name) < 30) and not name.isnumeric()


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
