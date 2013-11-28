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


def getData(filename):
    """Do get data in file.

    :param: path to file.
    :param type: string.
    :returns: list.
    :raises: raise Error.

    """
    data = BeautifulSoup(open(filename))
    matches = data.find_all('tbody')
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
#    conn = pymssql.connect(host=server, database=db, user=User, password=pwd)
#    cur = conn.cursor()
    for query in data:
        print query
 #       cur.execute(query)
 #       conn.commit()
 #   conn.close()


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
    data = re.sub('u|o|\+', '', data)
    try:
        Over, Under = data.split('/')
        return (float(Over) + float(Under))/2
    except ValueError:
        return float(data)


def getValueMatch(data, string):
    if data.find(string) != -1:
        result = re.sub('<(.*)>|\\n', '', data)
        if result == '' or result.strip() == '':
            return '{0}, NULL'.format(string)
        else:
            result = re.sub('  +', ',', result)
            return '{0}{1}'.format(string, result)


def getInfo(data, string):
    col = ['col-info', 'col-selection', 'col-1x2', 'col-hdp', 'col-hdp-odds', 'col-ou', 'col-ou-odds', 'col-1x2 half divider', 'col-hdp half', 'col-hdp-odds half', 'col-ou half', 'col-ou-odds half', 'col-oe', 'col-oe-odds', 'col-option']
    draw_col = ['col-selection', 'col-1x2', 'colspan-4', 'colspan-6', 'col-1x2 half divider', 'col-hdp half']
    list = []
    count = 0
    if string == 'draw':
        for td in draw.find_all('td'):
            #print getInfo(td.prettify(), draw_col[count])
            #print td.getText()
            list.append(getValueMatch(td.prettify(), draw_col[count]))
            count += 1
    elif string == 'away':
        count = 1
        for td in away.find_all('td'):
            #print getInfo(td.prettify(), col[count])
            #print td.getText()
            list.append(getValueMatch(td.prettify(), col[count]))
            count += 1
    else:
        for td in home.find_all('td'):
            #print getInfo(td.prettify(), col[count])
            #print td.getText()
            list.append(getValueMatch(td.prettify(), col[count]))
            count += 1
    return list

dict = {}
filename = "/root/project/OkChym/188bet/inplay.txt"
tbodies = getData(filename)
for tbody in tbodies:
    draw_list = []
    home_list = []
    away_list = []
    if len(tbody.find_all('tr')) > 2:
        home, away, draw = tbody.find_all('tr')
        home_list = getInfo(home, 'home')
        away_list = (getInfo(away, 'away'))
        draw_list = (getInfo(draw, 'draw'))
        print draw_list
        print "*************************"
    else:
        home, away = tbody.find_all('tr')
        home_list = (getInfo(home, 'home'))
        away_list = (getInfo(away, 'away'))
    print "home_list"
    print home_list
    print "========================="
    print "away_list"
    print away_list
    print "+++++++++++++++++++++++++"
    temp = home_list[0].split(',')
    if temp[-1] != ' NULL':
        key = '{0} {1}{2}{3}'.format(temp[-2], temp[1], temp[2], temp[3])
        print key
