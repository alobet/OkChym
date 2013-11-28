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
    """Data is the tbody.

    :param: data.
    :param type: type variable.
    :returns: value is match(home and away name).
    :raises: raise Error.

    """
    count = 0
    match = ''
    date = ''
    for td in data.find_all('td'):
        if td['class'][0] == 'col-selection' and count == 1:
            match += ' vs ' + td.getText().strip()
            return '{0};{1}'.format(match, date)
        if td['class'][0] == 'col-selection':
            match += td.getText().strip()
            count += 1
        if td['class'][0] == 'col-info':
            date += td.getText().strip()

filename = '/root/project/OkChym/188bet/premier_league.txt'
data = BeautifulSoup(open(filename))
tbody = data.find_all('tbody')
dict = {}
for value in tbody:
    #get match
    key, date = getMatch(value).split(';')
    if not key in dict:
        dict[key] = date

for key, value in dict.items():
    print key, value
