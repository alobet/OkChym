#!/usr/bin/python
#-*- coding: utf-8 -*-
"""Copyright (c) 2013 aloBet Group.

This file is used to get information for website http://www.asianbookie.com.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation aloBet Group.

"""
from bs4 import BeautifulSoup
import re
import sys
from datetime import datetime
import pymssql

'''
def getMatch(data):
    """Do get Information of the Match.

    :param: data.
    :param type: BeautifulSoup.
    :returns: list.
    :raises: raise Error.

    """
    chym = re.sub('<(.*)>|\\n', '', data.prettify())
    alo = re.sub('  +', ';', chym.strip())

    return alo.split(';')
'''


def getMatch(data):
    """Data is the tbody.

    :param: data.append    :param type: type variable.
    :returns: value is match(home and away name).
    :raises: raise Error.

    """
    count = 0
    match = ''
    date = ''
    for td in data.find_all('td'):
        if td['class'][0] == 'col-selection' and count == 1:
            match += ';' + td.getText().strip()
            return '{0};{1}'.format(match, date)
        if td['class'][0] == 'col-selection':
            match += td.getText().strip()
            count += 1
        if td['class'][0] == 'col-info':
            date += td.getText().strip()


def getData(filename):
    """Do get data in file.

    :param: path to file.
    :param type: string.
    :returns: list.
    :raises: raise Error.

    """
    data = BeautifulSoup(open(filename))
    tbody = data.find_all('tbody')

    return tbody


def convertTime(date, time):
    """Do convert time to valid format time.

    :param: date, time.
    :param type: string.
    :returns: valid datetime.
    :raises: raise Error.

    """
    begin = datetime.strptime(date + time, "%d/%m %H:%M")

    return begin.replace(year=datetime.now().year)


def doInsertDB(data):
    """Do Insert data into database.

    :param: data query.
    :param type: list.
    :returns: type value.
    :raises: raise Error.

    """
    server = "210.245.126.141"
    db = 'tip'
    User = 'sa'
    pwd = 'abc@123'
    conn = pymssql.connect(host=server, database=db, user=User, password=pwd)
    cur = conn.cursor()
    for query in data:
        print query
        cur.execute(query)
        conn.commit()
    conn.close()


for argv in sys.argv[1:]:
    filename = "/root/project/OkChym/188bet/%s" % argv
    matches = getData(filename)
    dict = {}
    columms = '[DoiChu], [DoiKhach], [NgayGioBatDau], [NgayTao]'
    queries = []
    for q in matches:
        query = 'INSERT INTO [TranDau](%s) VALUES(' % columms
        home, away, date = getMatch(q).split(';')
        key = home + away
        time = date.split()
        if not key in dict:
            dict[key] = date
            begin = convertTime(time[0] + time[1] + time[2] + ' ', time[3])
            #sample query
            #INSERT INTO [TranDau]
            #([DoiChu], [DoiKhach], [NgayGioBatDau], [NgayTao])
            #VALUES
            #('Elche', 'Atletico Madrid', '2013-11-30 22:00:00', getdate())']
            query = "{0}'{1}', '{2}', '{3}', getdate())".\
                    format(query, home, away, begin)
            queries.append(query)
    print argv
    doInsertDB(queries)
