"""Copyright (c) 2013 aloBet Group.

This file is used to get information for website http://www.asianbookie.com.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation aloBet Group.

"""
#!/usr/bin/python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2


def getLinkPerPage(data):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    links = []
    for link in data.find_all('a'):
        if link.find('span'):
            links.append(link.get('href'))

    return links


def getNextPage(data):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    if data.find('a', {'class': 'next'}):
        return data.find('a', {'class': 'next'}).get('href')
    return 'end'


def writeData2File(url):
    """Do get Information and return value.

    :param: variable.
    :param type: type variable.
    :returns: type value.
    :raises: raise Error.

    """
    webdata = urllib2.urlopen(url)
    print url
    soup = BeautifulSoup(webdata.read())
    data = soup.prettify()
    print data
    f_name = url.split('/')[-1]
    f = open(f_name, 'w')
    f.write(data.encode('utf8'))
    f.close()


url = 'http://www.mangdatphong.vn/du-thuyen-cruise'
chym = 'begin'
while chym != 'end':
    webdata = urllib2.urlopen(url)
    soup = BeautifulSoup(webdata.read())
    chym = getNextPage(soup)
    url = 'http://www.mangdatphong.vn/' + chym
    for link in getLinkPerPage(soup):
        writeData2File(link)
