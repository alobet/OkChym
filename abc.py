"""Copyright (c) 2013 aloBet Group.

This file is used to get information for website http://www.asianbookie.com.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation aloBet Group.

"""
#!/usr/bin/env python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import time


def getTimeZone(data):
    """Do get Information Time Zone.

    :param name: data.
    :param type: BeautifulSoup.
    :returns: always 'GMT+7'.
    :raises: raise Error.

    """
    value = data.body.find('option', {"selected": "selected"})

    return value.text

