#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


def dataNormalize(data):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    tr = re.sub('<(.*)>|\\n', '', data.prettify())
    return re.sub('  +', ',', tr).split(',')


def getMatch(data):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    if len(data) > 15:
        return 'date: {0}  {1}, match => {2}, {3}, {4}| 1x2 => {5}, {6}, {7}| handicap => {8}, {9}, {10}, {11}| OU => {12}, {13}, {14}, {15}'.format(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16])
    return 'date: {0}  {1}, match => {2}, {3}, {4}| handicap => {5}, {6}, {7}, {8}| OU => {9}, {10}, {11}, {12}'.format(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13])

soup = BeautifulSoup(open('/root/project/OkChym/handicap_premierleague.txt'))
tbody = soup.find('tbody')
trs = tbody.find_all('tr')
for tr in trs:
    value = dataNormalize(tr)
    print getMatch(value)
