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
def signin(username, password):
    login_url  = 'http://10.13.54.81/index.php'
    # login_url = 'http://10.13.54.81/login/nsindex_student.php'
    login_data = {
        'username': username,
        'password': password,
    }
    post_headers = {
        'User-Agent': user_agent,
        'Referer': 'http://10.13.54.81/',
    }
    login_res = English_session.post(login_url, data=login_data, headers=post_headers)
    if login_res.status_code == 200:
        print "Login Successfully!"
    else:
        print "Login failed..."

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
    post_headers = {
        'User-Agent': user_agent,
        'Referer': 'http://10.13.54.81/book/book25/dj21.php',
    }
    cookies = {
        'Hm_lvt_8a1d0cf914523c7ed112dbd25e018957': '1479901106',
        'NHCELoginCounter': '1',
    }
    url_response = English_session.post(target_url, data=answer_data, headers=post_headers, cookies=cookies)
    print English_session.cookies
    print url_response.content






if __name__ == "__main__":
    English_session = requests.Session()
    # username = raw_input("请输入用户名: ")
    username = '2015302407'
    # password = getpass.getpass()
    # password = raw_input("请输入密码: ")
    password = 'nhce111'
    signin(username, password)
    answer('http://10.13.54.81/book/book25/dj21.php', '7', '1', '245', 'C')