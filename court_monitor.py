# -*- coding: utf-8 -*-

from url_list_fetch import url_list_fetch
import time
from mysql_updater_baseClass import MySQLUpdater

time_span = 1*3600

pages = [1,2,3]
while True:
    mysql = MySQLUpdater()
    existed = mysql.pull_records()
    for page in pages:
        url_list_fetch(page, mysql, existed)
    mysql.clean_up()
    time.sleep(time_span)