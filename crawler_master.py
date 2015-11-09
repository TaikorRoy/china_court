# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 11:04:51 2015

@author: Administrator
"""

from url_list_fetch import url_list_fetch
import time
from mysql_updater_baseClass import MySQLUpdater
from check_remote_mysql import check_remote

mysql = MySQLUpdater()

starting_page_num = 1
ending_page_num = 90

existed = []
pages = range(starting_page_num, ending_page_num+1)
pages.reverse()
for page in pages:
    url_list_fetch(page, existed, db = None)
    time.sleep(2)

mysql.clean_up()