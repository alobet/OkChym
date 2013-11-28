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
    return data.find_all('tbody')


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


def getInfo(data, string, columms, count=0):
    """Do convert all string into a list.

    <tr>
        <td class="col-info" rowspan="3">
            <div class="score">
                <label id="sh609733">
                    0
                </label>
                    -
                <label id="sa609733">
                    0
                </label>
            </div>
            <div class="timer" id="tm609733">
            58:38
            </div>
            <div class="period" ttp="">
            2nd Half
            </div>
            <div class="event-detail">
            </div>
        </td>
        <td class="col-selection">
            <div class="selection clearfix">
                <span class="selection-txt fav" id="ht609733">
                FC St Pauli U19
                </span>
                <span class="rc rc0" ttp="No. of Red Cards">
                </span>
            </div>
        </td>
        <td class="col-1x2">
            <span class="odds" id="o356452330" ttp="Home">
            1.94
            </span>
        </td>
        <td class="col-hdp">
            <div class="hdp" hdp="-0.5" id="h356452349">
            0.5
            </div>
            </td>
            <td class="col-hdp-odds">
            <span class="odds" id="o356452349" ttp="Home">
            0.87
            </span>
        </td>
        <td class="col-ou">
            <div class="ou">
                <span class="ou-txt">
                O
                </span>
                <span hdp="1/1.5" id="h356452341">
                1/1.5
                </span>
            </div>
        </td>
        <td class="col-ou-odds">
            <span class="odds" id="o356452341" ttp="Over">
            0.93
            </span>
        </td>
        <td class="col-1x2 half divider">
        </td>
        <td class="col-hdp half">
            <div class="hdp">
            </div>
        </td>
        <td class="col-hdp-odds half">
        </td>
        <td class="col-ou half">
            <div class="ou">
            </div>
        </td>
        <td class="col-ou-odds half">
        </td>
        <td class="col-oe">
            <div class="oe">
            </div>
        </td>
        <td class="col-oe-odds">
        </td>
        <td class="col-option" rowspan="3">
            <a cc-info="true|609733|FC St Pauli U19|Holstein Kiel U19|1|" class="btn-mb ccajax" id="mb609733" ttp="View All Markets" url="/en-gb/sports/609733/in-play">
            3
            </a>
            <a class="btn-stats" target="_blank" ttp="Statistics" url="/en-gb/info-centre/sportsbook-info/statistics/609733">
            </a>
        </td>
    </tr>

    ===>
    [
        'col-1x2,3.20 ',
        'col-hdp,+0/0.5 ',
        'col-hdp-odds,0.70 ',
        'col-ou,U,1.5,',
        'col-ou-odds,0.76 ',
        'col-1x2 half divider,4.85 ',
        'col-hdp half,0 ',
        'col-hdp-odds half,-0.87 ',
        'col-ou half,U,0.5,',
        'col-ou-odds half,0.66 '
    ]

    """
    list = []
    temp = count
    for td in data.find_all('td'):
        list.append(getValueMatch(td.prettify(), columms[temp]))
        temp += 1
    return list


def getDataPerRow(data):
    """Do convert a list into dictionary.
    [
        'col-1x2,3.20 ',
        'col-hdp,+0/0.5 ',
        'col-hdp-odds,0.70 ',
        'col-ou,U,1.5,',
        'col-ou-odds,0.76 ',
        'col-1x2 half divider,4.85 ',
        'col-hdp half,0 ',
        'col-hdp-odds half,-0.87 ',
        'col-ou half,U,0.5,',
        'col-ou-odds half,0.66 '
    ]

    ===>
    {
        'col-hdp-odds': '0.72 ',
        'col-ou half': ' NULL',
        'col-1x2 half divider': ' NULL',
        'col-hdp half': ' NULL',
        'col-ou': 'O1/1.5',
        'col-hdp-odds half': ' NULL',
        'col-ou-odds': '0.95 ',
        'col-1x2': '2.03 ',
        'col-hdp': '0/0.5 '
    }

    """
    dict = {}
    for val in data:
        value = val.split(',')
        key = value[0]
        dict[key] = ''.join(value[1:]).strip()
    return dict


def doNormalData(home, away, draw):
    """Do get Information and return value.

    home                          |  away                              |  draw
    col-selection,CA Rentistas,', |  col-selection,Defensor Sporting,' |  col-selection,Draw,
    col-1x2,30.00                 |  col-1x2,1.04                      |  col-1x2,3.50
    col-hdp,+0/0.58               |  col-hdp,0/0.50                    |  colspan-4, NULL
    col-hdp-odds,0.77             |  col-hdp-odds,-0.93                |  colspan-6, NULL
    col-ou,O,7.5,ou               |  col-ou,U,7.5,                     |  col-1x2 half divider, NULL
    col-ou-odds,0.89              |  col-ou-odds,0.93                  |  col-hdp half, NULL
    col-1x2 half divider, NULL    |  col-1x2 half divider, NULL
    col-hdp half, NULL            |  col-hdp half, NULL
    col-hdp-odds half, NULL       |  col-hdp-odds half, NULL
    col-ou half, NULL             |  col-ou half, NULL
    col-ou-odds half, NULL        |  col-ou-odds half, NULL

    ===>
    {
        "CA Rentistas vs Defensor Sporting": [
            {
                "col-ou-odds half": " NULL",
                "col-hdp-odds": "0.77 ",
                "col-ou half": " NULL",
                "col-1x2 half divider": " NULL",
                "col-hdp half": " NULL",
                "col-ou": "O7.5",
                "col-hdp-odds half": " NULL",
                "col-ou-odds": "0.89 ",
                "col-1x2": "30.00 ",
                "col-hdp": "+0/0.5 "
            },
            {
                "col-ou-odds half": " NULL",
                "col-hdp-odds": "-0.93 ",
                "col-ou half": " NULL",
                "col-1x2 half divider": " NULL",
                "col-hdp half": " NULL",
                "col-ou": "U7.5",
                "col-hdp-odds half": " NULL",
                "col-ou-odds": "0.93 ",
                "col-1x2": "1.04 ",
                "col-hdp": "0/0.5 "
            },
            {
                'col-1x2': '1.20 ',
                'col-1x2 half divider': ' NULL'
            }
        ]
    }

    """
    key = '{0} vs {1}'.format(home[1].split(',')[1], away[0].split(',')[1])
    temp = []
    temp.append(getDataPerRow(home[2:12]))
    temp.append(getDataPerRow(away[1:-2]))
    if len(draw) > 2:
        temp.append(getDataPerRow([draw[1], draw[4]]))
    else:
        temp.append(getDataPerRow(draw))
    return {key: temp}


dict = {}
filename = "/root/project/OkChym/188bet/inplay.txt"
tbodies = getData(filename)
col = ['col-info', 'col-selection', 'col-1x2', 'col-hdp', 'col-hdp-odds', 'col-ou', 'col-ou-odds', 'col-1x2 half divider', 'col-hdp half', 'col-hdp-odds half', 'col-ou half', 'col-ou-odds half', 'col-oe', 'col-oe-odds', 'col-option']
draw_col = ['col-selection', 'col-1x2', 'colspan-4', 'colspan-6', 'col-1x2 half divider', 'col-hdp half']
queries = []
for tbody in tbodies:
    trs = tbody.find_all('tr')
    home = getInfo(trs[0], 'home', col)
    away = getInfo(trs[1], 'away', col, count=1)
    if len(trs) > 2:
        draw = getInfo(trs[2], 'draw', draw_col)
    else:
        draw = ['col-1x2,NULL', 'col-1x2 half divider, NULL']
    temp = home[0].split(',')
    if temp[-1] != ' NULL':
        match = doNormalData(home, away, draw)
        match.update({'time': temp[-2], 'home': temp[1], 'away': temp[3]})
        if len(temp) > 6:
            match.update({'time': temp[-2], 'home': temp[1], 'away': temp[3], 'minute': temp[4]})
        else:
            match.update({'time': temp[-2], 'home': temp[1], 'away': temp[3], 'minute': 'NULL'})
        print match
    #query_score_his = 
    #query_
