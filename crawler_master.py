# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 11:04:51 2015

@author: Administrator
"""

from url_list_fetch import url_list_fetch
import time
from mysql_updater_baseClass import MySQLUpdater

mysql = MySQLUpdater()

starting_page_num = 1
ending_page_num = 175

existed = []
pages = range(starting_page_num, ending_page_num+1)
pages.reverse()
for page in pages:
    url_list_fetch(page, existed, db = mysql)
    time.sleep(2)

mysql.clean_up()