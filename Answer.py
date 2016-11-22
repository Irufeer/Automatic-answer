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
    login_url  = 'http://10.13.54.81/'
    login_data = {
        'username': username,
        'password': password,
    }
    post_headers = {
        'User-Agent': user_agent,
        'Referer': 'http://10.13.54.81/',
    }

    try:
        login_res = English_session.post(login_url, data=login_data, headers=post_headers)
    except requests.exceptions.RequestException, e:
        print "Post failed...\n", e
        sys.exit(2)

    if login_res.status_code == 200:
        print "Login Successfully!"
    else:
        print "Login failed..."
        sys.exit(2)






if __name__ == "__main__":
    English_session = requests.Session()
    username = raw_input("请输入用户名: ")
    # password = getpass.getpass()
    password = raw_input("请输入密码: ")
    signin(username, password)

    book_url = 'http://10.13.54.81/book/index.php'