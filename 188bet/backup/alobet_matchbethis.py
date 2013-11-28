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
import decimal


def getMatch(data):
    """Data is tbody.

    :param: data.
    :param type: BeautifulSoup.
    :returns: list.
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


def getDetails(data):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    a = re.sub('<(.*)>|\\n', '', data.prettify())
    return re.sub('  +', ',', a).split(',')


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


def doConvertNumber(data):
    """Do change from string '-0.92' to number and return value = 2 + (-0.92) .

    :param: data.
    :param type: string.
    :returns: float value.
    :raises: raise Error.

    """
    try:
        if decimal.Decimal(data).is_signed():
            return str(2 + decimal.Decimal(data))
    except decimal.InvalidOperation:
        pass

    return data


def getValue(data):
    """Do convert data into valid data 0/0.5 or o2/2.5 or u2/2.5
    return value = (2+2.5)/2.

    :param: data.
    :param type: string.
    :returns: float.
    :raises: raise Error.

    """
    data = re.sub('u|o|\+', '', str(data))
    try:
        Over, Under = data.split('/')
        return (float(Over) + float(Under))/2
    except ValueError:
        return float(data)


for argv in sys.argv[1:]:
    filename = "/root/project/OkChym/188bet/%s" % argv
    matches = getData(filename)
    dict = {}
    for q in matches:
        home, away, date = getMatch(q).split(';')
        key = home + ' vs ' + away
        if not key in dict:
            dict[key] = q
    print '============================================'
    queries = []
    for key, match in dict.items():
        home, away, draw = match.find_all('tr')
        draw = getDetails(draw)
        home01 = getDetails(home)[3:16]
        away01 = getDetails(away)[1:-3]
        if home01[2].find('+') == -1:
            home01[2] = 0
        else:
            away01[2] = 0
        if home01[8].find('+') == -1:
            home01[8] = 0
        else:
            away01[8] = 0
        i = 3
        for j in range(i, len(home01), 3):
            home01[j-1] = getValue(home01[j-1])
            away01[j-1] = getValue(away01[j-1])
            home01[j] = doConvertNumber(home01[j])
            away01[j] = doConvertNumber(away01[j])
        query =  "INSERT INTO[match-bet-his]([match-name], [asia-home-handicap], [asia-away-handicap], [asia-home-win-multiplier], [asia-away-win-multiplier], [eu-home-win-multiplier], [eu-away-win-multiplier], [eu-draw-multiplier], [ou-numberofgoals], [ou-over-win-multiplier], [ou-under-win-multiplier], [update-time]) VALUES('{0} vs {1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, getdate())".format(home01[0], away01[0], home01[2], away01[2], home01[3], away01[3], home01[1], away01[1], draw[2], home01[5], home01[6], away01[6])
        queries.append(query)
        query = "INSERT INTO [match-firsthalf-bet-his]([match-name], [firsthalf-asia-home-handicap], [firsthalf-asia-away-handicap], [firsthalf-asia-home-win-multiplier], [firsthalf-asia-away-win-multiplier], [firsthalf-eu-home-win-multiplier], [firsthalf-eu-away-win-multiplier], [firsthalf-eu-draw-multiplier], [firsthalf-ou-numberofgoals], [firsthalf-ou-over-win-multiplier], [firsthalf-ou-under-win-multiplier], [update-time]) VALUES('{0} vs {1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, getdate())".format(home01[0], away01[0], home01[8], away01[8], home01[9], away01[9], home01[7], away01[7], draw[3], home01[11], home01[12], away01[12])
        queries.append(query)
    doInsertDB(queries)
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    for i in queries:
        print i
