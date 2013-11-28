#!/usr/bin/env python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import time
import pymssql
from fractions import Fraction
from datetime import datetime


def getTimeZone(data):
    """Do get Information Time Zone.

    :param name: data.
    :param type: BeautifulSoup.
    :returns: always 'GMT+7'.
    :raises: raise Error.

    """
    value = data.body.find('option', {"selected": "selected"})

    return value.text


def dataNormalize(data):
    """Do Normalize Data.

    :param name: data is a row in table.
    :param type: string.
    :returns: string value.
    :raises: raise Error.

    """
    value = re.sub('<(.*)>|\\n', '', data).strip()
    if value.find('<') != -1:
        for val in value.split(','):
            if val.find(' vs ') != -1:
                return val
    return value


def doSql(data):
    """Do connect to SQL server and insert data.

    :param: data.
    :param type: list.
    :returns: successfull or failure.
    :raises: raise Error.

    """
    server = "118.69.190.26"
    db = 'tip'
    User = 'sa'
    pwd = 'abc@123'
    conn = pymssql.connect(host=server, database=db, user=User, password=pwd)
    cur = conn.cursor()
    for query in data:
        cur.execute(query)
        time.sleep(1)
        conn.commit()

    conn.close()

    return 1


def getValueMixedNumber(data):
    """Do get Information and return value.

    :param: data.
    :param type: string.
    :returns: Fraction value.
    :raises: raise Error.

    """
    value = 0
    if data.strip().find(' ') != -1:
        whole, frac = data.split()
        value = float(int(whole) + Fraction(frac))
    else:
        if data.strip().find('/') != -1:
            whole, frac = data.strip().split('/')
            value = float(whole)/float(frac)
        else:
            value = int(data)
    return value


def replaceMeansValue(data):
    """Do replace '-' ==> '-1'value.

    :param: data.
    :param type: list.
    :returns: list.
    :raises: raise Error.

    """
    for row in data:
        for value in row:
            if value == '-':
                row[row.index(value)] = '-1'

    return data


def doConvertTime(data):
    """Do convert time to the valid time.

    :param: data.
    :param type: list.
    :returns: valid time.
    :raises: raise Error.

    """
    start_time = datetime.strptime(re.sub('\xc2\xa0\xc2\xa0', ' ', data[0]), "%d/%m %H:%M")

    return start_time.replace(year=datetime.now().year)


def sqlCmdNormalize(data, table):
    """Do Normalize Data.

    :param name: data is a row in table.
    :param type: string.
    :returns: string value.
    :raises: raise Error.

    """
    queries = []
    if table == '[match-bet-his]':
        asiaValues = "[match-name], [asia-home-handicap], [asia-away-handicap], [asia-home-win-multiplier], [asia-away-win-multiplier], [eu-home-win-multiplier], [eu-away-win-multiplier], [eu-draw-multiplier], [ou-numberofgoals], [ou-over-win-multiplier], [ou-under-win-multiplier], [update-time]"
        for row in data:
            asiaDatas = '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}'.format(row[1], getValueMixedNumber(row[3].split(':')[0]), getValueMixedNumber(row[3].split(':')[-1]), row[2], row[4], row[5], row[7], row[6], getValueMixedNumber(row[9]), row[8], row[10])
            asiaCmd = "INSERT INTO {0} ({1}) VALUES ({2}, getdate())".format(table, asiaValues, asiaDatas)
            queries.append(asiaCmd)

    return queries

#we can use the argv of the system as variables for url
#url = "http://www.asianbookie.com/index.cfm?league={0}&tz={1}"\
#        .format(argv[0], argv[1])
#url = "http://www.asianbookie.com/index.cfm?league=2&tz=7"
with open('/root/project/OkChym/alobet_MATCH.txt') as f:
    for url in f:

        #Simulated a web browser
        request = urllib2.Request(url)
        request.add_header('User-agent', 'Googlebot/2.1')
        webdata = urllib2.urlopen(request)
        data = BeautifulSoup(webdata.read())

        #get table store all info
        masterdiv = data.body.find('div', {'id': 'masterdiv'})

        #get all table row
        tablerow = masterdiv.find_all('tr')

        #select rows needed in a table
        match_rows = []
        for tag in tablerow:
            if tag.td.has_attr('align') and tag.td.has_attr('nowrap'):
                if tag.find('span'):
                    match_rows.append(BeautifulSoup(tag.prettify()))

        #values insert into Database
        values = []
        OUs = []
        for row in match_rows:
            columms = row.find_all('td')
            matches = []
            for value in columms:
                matches.append(dataNormalize(str(value)))
            if len(matches) == 8:
                values.append(matches)
            else:
                OUs.append(matches)

        #Do join 2 list into 1 list
        if len(values) == len(OUs):
            joinData = []
            for i in values:
                joinData.append(i + OUs[values.index(i)][2:])
        else:
            print 'error'

        joinData = replaceMeansValue(joinData)

        #sql command insert data into [match-bet-his] table
        sqlmatchbethis = sqlCmdNormalize(joinData, '[match-bet-his]')

        for sql in sqlmatchbethis:
            print sql
        doSql(sqlmatchbethis)
