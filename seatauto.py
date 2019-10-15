#!/usr/bin/env python
# -*- coding: utf-8 -*-

# USCLib Host地址:https://seat.usc.edu.cn:8443

import requests
import datetime
import json
import sys
import urllib3
import time
import schedule

urllib3.disable_warnings()


#存储座位预约信息
page_json = {
    "data": [
        {
            #开始时间，从零点开始以分钟计算
            'startTime': '480',
            #结束时间
            'endTime': '840',
            #座位号
            'seatId': '16254',
            #学号
            'studentNum': '20160000000',
            #密码
            'password': '000000'
        }
    ],
    #字典长度
    "length": 1

}

login_headers = {
    'Host': 'seat.usc.edu.cn:8443',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'doSingle/11 CFNetwork/811.5.4 Darwin/16.6.0',
    'Accept-Language': 'zh-cn',
    'token': 'Q6NTRKQ4DV07050600',
    'Accept-Encoding': 'gzip',
    'X-Forwarded-For': '10.167.159.118'
}


def seatcrawler():
    for i in range(page_json['length']):
        try:
            getTokenURL = 'http://seat.usc.edu.cn:80/rest/auth?username=' + page_json['data'][i][
                'studentNum'] + '&password=' + page_json['data'][i]['password']
            print(page_json['data'][i][
                      'studentNum'] + "**" + page_json['data'][i]['password'])

            tokenResponse = requests.get(getTokenURL, headers=login_headers, verify=False)
            login_json = json.loads(tokenResponse.text)
            token = login_json['data']['token']

            date = datetime.date.today()
            date += datetime.timedelta(days=1)
            strdate = date.strftime('%Y-%m-%d')
            print(strdate)
            headers = {
                'Host': 'seat.usc.edu.cn:8443',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'token': login_json['data']['token'],
                'User-Agent': 'doSingle/11 CFNetwork/811.5.4 Darwin/16.6.0',
                'Accept-Language': 'zh-cn',
                'X-Forwarded-For': '10.167.159.118'
            }
            postdata = {
                't': 1,
                'startTime': page_json['data'][i]['startTime'],
                'endTime': page_json['data'][i]['endTime'],
                'date': strdate,
                'seat': page_json['data'][i]['seatId'],
                't2': 2
            }
            mainURL = 'https://seat.usc.edu.cn:8443/rest/v2/freeBook'
            s = requests.post(mainURL, data=postdata, headers=headers, verify=False)
            print(s.text)
            # if (s["status"] != "fail"): quit()
        except:
            continue

# 定时，每天22.15.01准时开约
schedule.every().day.at("22:15:01").do(seatcrawler)

while True:
    schedule.run_pending()
    time.sleep(1)
