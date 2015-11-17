# -*- coding: utf-8 -*-

from url_list_fetch import url_list_fetch
import time
from mysql_updater_baseClass import MySQLUpdater
from check_remote_mysql import check_remote

time_span = 1*3600

pages = [1, 2, 3, 4, 5]
while True:
    # mysql = MySQLUpdater()
    # existed = mysql.pull_records()
    try:
        existed = check_remote(100)
    except:
        print("Remote check-court-record API unavailable")
        time.sleep(300)
        continue

    for page in pages:
        url_list_fetch(page, existed)
    # mysql.clean_up()
    time.sleep(time_span)
