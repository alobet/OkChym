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
from datetime import date
import pymssql


def getMatch(data):
    """Do get Information of the Match.

    <div class="rt-1 ">
       <div class="rt-cc-time" id="e-609711">
           <span>
               19:00
           </span>
       </div>
       <div class="rt-event" title="Independiente Rivadavia - Union Santa Fe ">
           <span class="pt">
               Independiente Rivadavia
           </span>
           <span class="vs">
               v
           </span>
           <span class="pt">
               Union Santa Fe
           </span>
       </div>
       <div class="rt-ht ">
           0-0
       </div>
       <div class="rt-ft ">
           2-0
       </div>
    </div>

    ==>
    '19:00;Independiente Rivadavia;v;Union Santa Fe;0-0;2-0'

    :param: data.
    :param type: BeautifulSoup.
    :returns: a string.
    :raises: raise Error.

    """
    chym = re.sub('<(.*)>|\\n', '', data.prettify())
    alo = re.sub('  +', ',', chym.strip())
    return alo


def getData(filename):
    """Do get data in file.

    element in a list
    <div class="rt-1 ">
       <div class="rt-cc-time" id="e-609711">
           <span>
               19:00
           </span>
       </div>
       <div class="rt-event" title="Independiente Rivadavia - Union Santa Fe ">
           <span class="pt">
               Independiente Rivadavia
           </span>
           <span class="vs">
               v
           </span>
           <span class="pt">
               Union Santa Fe
           </span>
       </div>
       <div class="rt-ht ">
           0-0
       </div>
       <div class="rt-ft ">
           2-0
       </div>
    </div>

    :param: file.
    :param type: string.
    :returns: list.
    :raises: raise Error.

    """
    data = BeautifulSoup(open(filename))
    div = data.find_all('div', {'class': 'rt-1 '})
    b = data.find_all('div', {'class': 'rt-0 '})

    return div + b


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


filename = "/root/project/OkChym/188bet/result.txt"
div = getData(filename)
queries = []
test = re.compile('\d-\d')
for q in div:
    #query = 'INSERT INTO [TranDau](%s) VALUES(' % columms
    temp = getMatch(q).split(',')
    if test.search(temp[-2]):
        home1, away1 = temp[-2].split('-')
        home, away = temp[-1].split('-')
        temptime = '{0} {1}:00'.format(str(date.today()), temp[0])
        query = "INSERT INTO match_result(home_team_name, away_team_name, home_numberofgoals, away_numberofgoals, firsthalf_home_numberofgoals, firsthalf_away_numberofgoals, start_datetime, create_datetime) VALUES('{0}','{1}', {2}, {3}, {4}, {5}, '{6}', getdate())".format(temp[1], temp[3], home, away, home1, away1, temptime)
        queries.append(query)
doInsertDB(queries)
