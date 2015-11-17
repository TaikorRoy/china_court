# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:46:53 2015

@author: Administrator
"""
import requests
import re 
import MySQLdb
import codecs
from format_converter import cn2digits_master
from format_converter import date_handle
from format_converter import handle_punctuations
from format_converter import delete_none
from mysql_updater_baseClass import MySQLUpdater
from lib import get_formated_time
import json


def crawl_and_parse(url, db = None):
    r = requests.get(url)
    html = r.text
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    html = html.replace("\t", "")
    #公告ID
    postId = re.findall(u"id/([0-9]+?)\.",url)
    if len(postId) == 0 or postId == " " or postId == "":
        postYmd = u"空"
    #公告日期
    postYmd = re.findall(u'刊登日期：(.+?)<br' ,html)
    if len(postYmd) == 0 or postYmd == " " or postYmd == "":
        postYmd = u"空"
    #当事人公司
    postCorp = re.findall(r'<div class="dsrnr">(.+?)</div>',html)
    if len(postCorp) == 0 or postCorp == " " or postCorp == "":
        postCorp = u"空"
    #公告法院
    postCourt = re.findall(r'>.+?<div class="affiliation">(.+?)<br' ,html)
    if len(postCourt) == 0 or postCourt == " " or postCourt == "":
        postCourt = u"空"
    #公告完整内容
    postContent = re.findall(r'<div class="dsrnr">(.+?)</div>',html)
    if len(postContent) == 0 or postContent == " " or postContent == "":
        postContent = [u"空", u"空"]

    #汇票票号
    billsId = re.findall(u'(?:票号|号码|编号|汇票号码|支票号码|编码)(?:为|:|：|分别为|是|)(.+?[0-9])(?:，|,|（|的|号|、|；|银行承兑|票面金额)', html )
    if billsId == []:
        billsId = re.findall(u'(?:签发的|出具的|持有的)(.+?)银行承兑汇票',html)
        if billsId == []:
            billsId = u"空"
    elif billsId[0].find(u"<") > -1:
        billsId = u"空"
    #汇票金额
    billsAmount = re.findall(u'(?:金额|人民币|持股数|出票金额|票面金额|面额)(?:为|:|：|分别为|均为|)(.+?元)', html)
    if billsAmount == []:
       billsAmount = re.findall(u'(?:金额|人民币|金额人民币|票面金额人)(?:为|:|：|)(.+?)(?: ，|\)|、|;)',html)
       if billsAmount == []:
           billsAmount = u"空"
           
    #出票公司（银行）
    billsCorp = re.findall(u'(?:出票人|出票行|出票方|开户行)(?:为|:|：|全称|均为|是|)(.+?)(?:，|,|、|；|。|的)',html)
    if billsCorp == []:
        billsCorp = u"空"
    #收款人（公司）
    billsGain = re.findall(u'收款人(?:为|:|：|全称：|全称|均为|是|名称：)(.+?)(?:，|,|、|；|。|的银行承兑汇票|[0-9]|的承兑汇票)',html)
    if billsGain == []:
        billsGain = u"空"
    #付款行（公司）
    
    billsPay = re.findall(u'(?:付款行|付款人|支付人|付款行全称|发行公司名称)(?:为|:|：|全称：|全称|均为|是|)(.+?)(?:，|。|,|、|；|）|的银行承兑汇票|[0-9]|的承兑汇票|])',html)
    if billsPay == []:
        billsPay = re.findall(u'(?:遗失|持有的|持有|遗失的)(.+?)(?:签发的|出具的)', html)
        if billsPay == []:
            billsPay = u"空"
            
    #出票日期
    billsYmdStart = re.findall(u'出票日期(?:为|:|：|均为|)(.+?)(?:，|的|、|；|。)',html)
    if billsYmdStart == []:
        billsYmdStart = re.findall(u'于(.+?日)办理',html)
        if billsYmdStart == []:
           billsYmdStart = u"空"
        
    
    #到期日期
    billsYmdEnd = re.findall(u'(?:汇票到期日|到期日)(?:为|:|：|均为|期|期为|期：)(.+?日)(?:，|的|、|；|。)',html)
    if billsYmdEnd == []:
        billsYmdEnd = u"空"
    
    postSection = re.findall(u'刊登版面(?::|：)(.+?)<br',html)
    if postSection == []:
        postSection = u"空"
            
    a = postYmd[0]
    b = postCorp[0]
    c =  postCourt[0].strip(" ")
    d =  postContent[1]
    e =  billsId[0]
    f =  billsAmount[0]
    g =  billsCorp[0]
    h =  billsGain[0]
    i =  billsPay[0]
    j = billsYmdStart[0]
    k =  billsYmdEnd[0]
    l = postSection[0]
    m = a
    n = a
    t = postId[0]
    
    b = re.sub(u"、|，", "", b)
    e = re.sub(u":|号|：", "", e)
    f = re.sub(u"￥|人民币|元|整|,| ","",f)
    g = re.sub(u"：|、|，", "", g)
    h = re.sub(u"承兑汇票一张|、|，","",h)
    h = re.sub(u"公司）",u"公司", h)
    k = re.sub(u"为|是", "", k)

    a = date_handle(a)
    m = date_handle(a)
    n = date_handle(a)
    j = date_handle(j)
    k = date_handle(k)

    e = handle_punctuations(e)
    f = cn2digits_master(f)
    
    info = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, t]

    billNo = info[4]
    if billNo != u"空":
        for info_item in range(len(info)):
            if info[info_item] == u"空":
                info[info_item] = None

        if info[5]:
            info[5] = float(info[5])

        if db:
            sql = r"INSERT INTO billloss (postId, postUrl, postYmd, postCorp, postCourt, postContent, billsId, billsAmount, billsCorp, billsGain, billsPay, billsYmdStart, billsYmdEnd, postSection, pubDate, uploadDate) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (info[14], url, info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10],info[11],info[12],info[13])
            print(sql)
            db.query(sql)
            print("Python MySQL update OK")
        else:
            current_formated_time = get_formated_time()
            billloss_dict = {
                    "billNo": info[4],
                    "possId": info[14],
                    "possUrl": url,
                    "possDate": info[0],
                    "company": info[1],
                    "court": info[2],
                    "content": info[3],
                    "faceAmount": info[5],
                    "payerCompany": info[6],
                    "payerBank": info[7],
                    "payeeCompany": info[8],
                    "issueDate": info[9],
                    "dueDate": info[10],
                    "postSection": info[11],
                    "status": u"状态",
                    "recorder": u"操作员",
                    "remark": u"无",
                    "createTime": current_formated_time,
                    # "createTime": "2015-08-28 01:30:00", for debug use only
                    "updateTime": current_formated_time
                    }

            billloss_dict = delete_none(billloss_dict)
            # delete none value keys, ensure all date time field has value

            court_data = {
                             "head": {
                                 "comeFrom": 1
                             },
                "sign": "6cd7a0cec3ba9bbab2f95a4570aa54a5",
                "args": {
                    "billLoss": billloss_dict
                }
            }

            api_url = "http://taomandev.piaojiaowang.com/PJWServices/bill/addBillLoss"
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            json_str = json.dumps(court_data, ensure_ascii=True)
            r = requests.post(api_url, data=json_str, headers=headers)
            print(r.text)

if __name__ == "__main__":

    # mysql = MySQLUpdater()
    crawl_and_parse(r"http://www.live.chinacourt.org/fygg/detail/2015/06/id/2736426.shtml", db = None)
