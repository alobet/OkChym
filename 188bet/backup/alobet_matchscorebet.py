#!/usr/bin/python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pymssql
import sys
from time import sleep


def dataNormalize(data):
    """Do get the Name of match.

    :param: data.
    :param type: BeautifuSoup.
    :returns: name of match.
    :raises: raise Error.

    """
    text = []
    for value in data.find_all('span'):
        text.append(value.getText())
    return text


def getQuery(data, match, typeOfhalf):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    for i in range(0, len(data), 2):
        if data[i].find('Any') == -1:
            home, away = data[i].split(' - ')
            return "INSERT INTO {0} ([home-numberofgoals], [away-numberofgoals], [win-multiplier], [match-name], [update-time]) VALUES ({1}, {2}, {3}, '{4}', getdate())".format(typeOfhalf, home, away, data[i+1], match)


def doInsertDB(data):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
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
    soup = BeautifulSoup(open(filename))
    tbody = soup.find_all('tbody')
    temp = {}
    queries = []
    for data in tbody:
        trs = data.find_all('tr')
        match = dataNormalize(trs[0])
        match = '{0} vs {1}'.format(match[0], match[2])
        if not match in temp:
            temp[match] = '[match-scorebet-his]'
            typeOfhalf = '[match-scorebet-his]'
        else:
            typeOfhalf = '[match-firsthalf-scorebet-his]'
        for i in trs[1:]:
            queries.append(getQuery(dataNormalize(i), match, typeOfhalf))
    doInsertDB(queries)
