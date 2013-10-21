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
import re


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
                value = val
    return value


#we can use the argv of the system as variables for url
#url = "http://www.asianbookie.com/index.cfm?league={0}&tz={1}"\
#        .format(argv[0], argv[1])
url = "http://www.asianbookie.com/index.cfm?league=6&tz=7"

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
for row in match_rows:
    columms = row.find_all('td')
    matches = []
    for value in columms:
        matches.append(dataNormalize(str(value)))
    values.append(matches)

for value in values:
    print ','.join(value)
