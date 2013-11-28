"""Copyright (c) 2013 aloBet Group.

This file is used to get information for website http://www.asianbookie.com.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation aloBet Group.

"""
#!/usr/bin/python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re


def dataNormalize(chym):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    val = data.find_all('span')

    return '{0} {1} {2}'.format(val[0].text, val[1]['class'], val[2].text)


soup = BeautifulSoup(open('javascript.txt'))
data = soup.find('tbody')
for tr in soup.find_all('tr'):
    for td in tr.find_all('td'):
        if td.a:
            print td.a['title'], td.a.text
