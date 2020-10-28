import datetime
import random
import sqlite3
import time

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import style

conn = sqlite3.connect('amazon.db')
c = conn.cursor()


def getPriceFromDb(URL: str):
    """Read the database and return the price of the url in the arguments."""
    c.execute('SELECT price FROM table1 WHERE url = ?',
              (URL,)
              )
    data = c.fetchall()
    for row in data:
        print(row)


def create_table():
    """Do creates a table."""
    c.execute(
        'CREATE TABLE IF NOT EXISTS amazon(url TEXT, price TEXT, datestamp TEXT, unix REAL, id INTEGER PRIMARY KEY AUTOINCREMENT)'
    )


def getAllData():
    c.execute('SELECT * FROM amazon ORDER BY id DESC')
    data = c.fetchall()
    for row in data:
        print(row)


def dynamic_data_entry():
    url = "asdfas.com"
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime(
        '%Y-%m-%-d %H: %M: %S'))
    for x in range(10):
        price = random.randrange(0, 10)
        c.execute("INSERT INTO amazon (url, price, datestamp, unix)"
                  "VALUES(?, ?, ?, ?)",
                  (url, price, date, unix))
    conn.commit()


def accesData(url):
    c.execute("SELECT price FROM amazon WHERE url = ? ORDER BY id DESC",
              (url,)
              )
    data = c.fetchall()
    for x in data:
        print(x)


create_table()
# dynamic_data_entry()
accesData("asdfas.com")
getAllData()
