#!/usr/bin/python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pymssql
from time import sleep


def dataNormalize(data):
    """Do get the Name of match.

    :param: data.
    :param type: BeautifuSoup.
    :returns: name of match.
    :raises: raise Error.

    """
    val = data.find_all('span')

    return '{0} {1} {2}'.format(val[0].text, val[1]['class'][0], val[2].text)


soup = BeautifulSoup(open('/root/project/OkChym/javascript.txt'))
data = soup.find('tbody')
server = "118.69.190.26"
db = 'tip'
User = 'sa'
pwd = 'abc@123'
conn = pymssql.connect(host=server, database=db, user=User, password=pwd)
cur = conn.cursor()
#cur.execute(query)
#time.sleep(1)
#conn.commit()

#conn.close()

#print all value of match
matches = []
count = 0
for tr in soup.find_all('tr'):
    if tr.find('div'):
        match = dataNormalize(tr)
    for td in tr.find_all('td'):
        if td.a:
            if td.a['title'].find(':') != -1:
                home, away = td.a['title'].split(':')
                #should be insert into DB
                if count % 2 == 0:
                    query = "INSERT INTO [match-scorebet-his] ([home-numberofgoals], [away-numberofgoals], [win-multiplier], [match-name], [update-time]) VALUES ({0}, {1}, {2}, '{3}', getdate())".format(home.strip(), away.strip(), td.a.text, match)
                    #print 'Full Time: {0} => {1}, {2}, {3}'.format(match, home.strip(), away.strip(), td.a.text)
                    print query
                    cur.execute(query)
                    conn.commit()
                    #sleep(0.01)
                else:
                    query = "INSERT INTO [match-firsthalf-scorebet-his] ([home-numberofgoals], [away-numberofgoals], [win-multiplier], [match-name], [update-time]) VALUES ({0}, {1}, {2}, '{3}', getdate())".format(home.strip(), away.strip(), td.a.text, match)
                    #print 'First Half: {0} => {1}, {2}, {3}'.format(match, home.strip(), away.strip(), td.a.text)
                    print query
                    cur.execute(query)
                    conn.commit()
                    #sleep(0.01)
            else:
                if td.a['title'].find('Any') != -1:
                    count += 1
#conn.commit()
conn.close()
