#!/usr/bin/python
#-*- coding: utf-8 -*-
"""Copyright (c) 2013 aloBet Group.

This file is used to get information for website http://www.asianbookie.com.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation aloBet Group.

"""
import _mssql
ser = "210.245.126.141"
db = 'tip'
U = 'sa'
P = 'abc@123'
conn = _mssql.connect(server=ser, database=db, user=U, password=P)
conn.execute_query('exec cal_bet')
conn.close()
