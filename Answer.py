#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import codecs
import string
import random
import re
import getpass
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")
main_url = 'http://10.13.54.81'
def signin(username, password):
    English_session.get(main_url)
    login_url = main_url + "/index.php?Horizon=" + English_session.cookies['Horizon']
    login_data = {
        'username': username,
        'password': password,
    }
    post_headers = {
        'User-Agent': user_agent,
        'Referer': 'http://10.13.54.81/',
    }
    # 发送账号密码
    English_session.post(login_url, data=login_data, headers=post_headers)
    res = English_session.get(main_url + '/login/nsindex_student.php')
    res = res.text
    pattern = 'BID=25&CID=(.*?)&Quiz=N">.*?'
    id = re.findall(pattern, res, re.S)
    url = main_url + "/book/index.php?BID=25&CID=" + id[0][0] + id[0][1] + id[0][2] + id[0][3] + "&Quiz=N"
    print url
    # 获取CID和BID
    English_session.get(url)
    English_session.get(main_url + "/template/loggingajax.php?whichURL=/login/nsindex_student.php")
    English_session.get(main_url + "/book/book25/index.php?Quiz=N&whichActionPage=")
    # 以上打开书本

def answer(target_url, UnitID, KidID, ItemID, Answer):
    SectionID = target_url[33]
    SisterID  = target_url[34]
    TestID    = SectionID + '.' + SisterID
    ans = 'Item_' + ItemID
    answer_data = {
        'UnitID': UnitID,
        'SectionID': SectionID,
        'SisterID': SisterID,
        'TestID': TestID,
        'KidID': KidID,
        'ItemID': ItemID,
        ans: Answer,
    }
    payload = {
        'whichAction': 'checkMyProgress',
        'whichUnitID': UnitID,
        'whichTestID': ''
    }
    post_headers = {
        'User-Agent': user_agent,
        'Referer': 'http://10.13.54.81/book/book25/dj21.php',
    }
    English_session.post(main_url + "/book/book25/jdls3ajax.php", data=payload)
    url = main_url + "/book/book25/unit_index.php?UnitID=" + UnitID
    res = English_session.get(url)
    # 提交部分start
    url_response = English_session.post(target_url, data=answer_data, headers=post_headers)





if __name__ == "__main__":
    English_session = requests.Session()
    username = raw_input("请输入用户名: ")
    # password = getpass.getpass()
    password = raw_input("请输入密码: ")
    signin(username, password)
    answer('http://10.13.54.81/book/book25/dj21.php', '10', '1', '371', 'A')