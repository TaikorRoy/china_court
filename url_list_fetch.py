# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:57:13 2015

@author: Administrator
"""

import requests
import re 
from url_content_fetch import crawl_and_parse
import codecs


def url_list_fetch(starting_page_num, existed, db = None):
    url_list_url = r"http://www.live.chinacourt.org/fygg/index/kindid/5/page/" + str(starting_page_num) +".shtml"
    r = requests.get(url_list_url)
    html = r.text
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    html = html.replace("\t", "")
    
    postUrl = re.findall(r'<tr class="fygg_contents"><td><a href=\'(.+?)\'>.+?</a>', html)
    size = len(postUrl)
    s = "http://www.live.chinacourt.org"
    for i in range(size):
        postUrl[i] = s + postUrl[i]
        
    for url in postUrl:
        try:
            if url not in existed:
                crawl_and_parse(url, db)
        except:
            print(url)
            print("Problem Found !")
            with codecs.open("failed_urls_log", "a", encoding="utf8") as fl:
                fl.write(url)