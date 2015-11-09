# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import MySQLdb
import time
import codecs
import requests
import json

class MySQLUpdater(object):
    HOST = "localhost"
    USER = "root"
    PASSWD = ""
    DB = "court"

    def __init__(self):
        self.db = MySQLdb.Connect(
            host=MySQLUpdater.HOST,
            user=MySQLUpdater.USER,
            passwd=MySQLUpdater.PASSWD,
            db=MySQLUpdater.DB,
        )
        self.db.query('SET NAMES utf8')
        self.cursor = self.db.cursor()


    def query(self, sql):
        sql = sql.encode('utf8')
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("DB Insertion Succeed !")
        except:
            print("DB Insertion Failed !")
            with codecs.open("debug_sql_log", "a", encoding="utf8") as fl:
                fl.write(unicode(sql, "utf8"))
            self.db.rollback()

    def pull_records(self):
        sql = r"select postUrl from billloss order by id desc limit 100"
        sql = sql.encode('utf8')
        self.cursor.execute(sql)
        self.db.commit()
        urls = list()
        list_buffer = self.cursor.fetchall()
        for item in list_buffer:
            urls.append(item[0])
        return urls

    def pull_records_remote(self):
        api_url = "http://taomandev.piaojiaowang.com/PJWServices/bill/addBillLoss"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        court_data = {}
        json_str = json.dumps(court_data, ensure_ascii=True)
        r = requests.post(api_url, data=json_str, headers=headers)
        data = r.text
        # To Do: Requests Details

    def clean_up(self):
        self.db.close()



