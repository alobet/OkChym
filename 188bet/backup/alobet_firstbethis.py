#!/usr/bin/python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import sys
from datetime import datetime
import pymssql
import decimal


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


def getData(filename):
    """Do get data in file.

    :param: path to file.
    :param type: string.
    :returns: list.
    :raises: raise Error.

    """
    data = BeautifulSoup(open(filename))
    tbody = data.find('tbody')
    matches = []
    if tbody is not None:
        matches = tbody.find_all('tr')

    return matches


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
    data = re.sub('u|o', '', data)
    try:
        Over, Under = data.split('/')
        return (float(Over) + float(Under))/2
    except ValueError:
        return float(data)


for argv in sys.argv[1:]:
    filename = "/root/project/OkChym/188bet/%s" % argv
    matches = getData(filename)
    dict = {}
    chym = []
    for q in matches:
        mat = getMatch(q)
        key = '{0}, {1}'.format(mat[2], mat[3])
        if not key in dict:
            print key
            dict[key] = 'alochym'
            chym.append(mat)

    queries = []
    for match in chym:
        print match
        if match[8].find('+') == -1:
            match[8] = '0'
        else:
            match[10] = '0'
        for value in match[9::2]:
            match[match.index(value)] = doConvertNumber(value)
        for value in match[8:-1:2]:
            match[match.index(value)] = getValue(value)
        print "++++++++++++++++++++++++++++++"
        #print match.index(value), value
        query = "INSERT INTO [match-firsthalf-bet-his]([match-name], [firsthalf-asia-home-handicap], [firsthalf-asia-away-handicap], [firsthalf-asia-home-win-multiplier], [firsthalf-asia-away-win-multiplier], [firsthalf-eu-home-win-multiplier], [firsthalf-eu-away-win-multiplier], [firsthalf-eu-draw-multiplier], [firsthalf-ou-numberofgoals], [firsthalf-ou-over-win-multiplier], [firsthalf-ou-under-win-multiplier], [update-time]) VALUES('{0} vs {1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, getdate())".format(match[2], match[3], match[8], match[10], match[9], match[11], match[5], match[6], match[7], match[12], match[13], match[15])
        print query
        print "============================="
        queries.append(query)
    #for value in chym:
        #print value
    doInsertDB(queries)
