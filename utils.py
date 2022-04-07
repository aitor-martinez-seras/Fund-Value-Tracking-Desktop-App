import sqlite3
from constants import *
import datetime
import requests
import random
from bs4 import BeautifulSoup
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
    else:
        assert isinstance(params, (list, tuple))
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


def edit_deposit(db, entries):
    query = f"""UPDATE {entries['fund']}
                SET Fecha = ?,
                    Aporte = ?, 
                    Participaciones = ?, 
                    Valor_participacion = ? 
                WHERE Id = ?"""
    query_db(db, query, params=(entries['date'], entries['deposit'],
                                entries['participations'], entries['value'], entries['id']))


def delete_record_from_db(db, fund, id_string):
    query = f"""DELETE FROM {fund} WHERE Id = {id_string}"""
    try:
        query_db(db, query)
        return True
    except Exception as e:
        print(f'Ha ocurrido la excepcion {e}')
        return False


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


def get_available_funds(db) -> list:
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
        query = f"""
        SELECT * FROM {fund_name} 
        ORDER BY Id DESC LIMIT ?
        """
        params = 15
    elif dates == 'All':
        query = f"SELECT * FROM {fund_name}"
        params = None
    else:
        query = f"""
        SELECT * FROM {fund_name}
        WHERE Fecha BETWEEN ? AND ?"""
        params = (dates['from'], dates['to'])
    query = query_db(db, query, params=params)
    deposits = parse_deposits(query)
    return deposits


def parse_deposits(query_object: sqlite3.Cursor) -> list:
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


def list_to_string(list_of_str: list) -> str:
    strng = ''
    for index, item in enumerate(list_of_str):
        strng += item
        if index == len(list_of_str)-1:
            strng += '.'
        else:
            strng += ', '
    return strng

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


def validate_date(date: datetime.date):
    try:
        return (1950 < date.year < 2100) and (0 <= date.month <= 12) and (0 <= date.day <= 31)
    except (ValueError, AttributeError) :
        return False


def parse_date_to_datetime(date):
    try:
        items_list = date.split('-')
        date = datetime.date(int(items_list[0]), int(items_list[1]), int(items_list[2]))
        return date
    except ValueError:
        return False


def parse_dates_to_linspace(dates):
    new_dates = [datetime.strptime(item, '%Y-%m-%d') for item in dates]
    oldest_date = new_dates[0].timestamp()
    dates_linspace = [round((item.timestamp() - oldest_date)/(60*60*24*7*2), 3) for item in new_dates]
    return dates_linspace


def parse_num_with_commas_for_decimals(num: str):
    num = num.replace('.','')
    num = num[::-1].replace(',','.',1)
    return num[::-1]

# Scrapping functions

def get_fund_value(fund_name):
    """
    Obtains the value of the fund calling the web scrapping functions
    :param fund_name: String with the name of the fund, must match one on the dictionary on the constants.py
    :return: value of one participation of the fund
    """
    if fund_name in FUNDS_WEB_PAGES.keys():
        web_page = FUNDS_WEB_PAGES[fund_name]
        fund_value = scrape_investing_dot_com(web_page)
    else:
        return False

    return fund_value


def scrape_investing_dot_com(fund_web_page):
    """
    Scrapes investing.com to get the fund value at the moment
    :param fund_name:
    :return:
    """
    # Future headers may need to be added
    # This function needs a lot of exception preventing code
    page = requests.get(
        fund_web_page,
        headers={'User-Agent': random.choice(USER_AGENTS)})
    soup = BeautifulSoup(page.text, 'html.parser')
    fund_value = soup.find(id="last_last").text
    try:
        fund_value = float(parse_num_with_commas_for_decimals(fund_value))
    except Exception as e:
        print(e)
    return fund_value
