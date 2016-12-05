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

main_url = 'http://10.13.54.81'
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")


def signin(username, password):
    English_session.get(main_url)
    login_url = main_url + '/index.php?Horizon=' + English_session.cookies['Horizon']
    login_data = {
        'username': username,
        'password': password,
    }
    login_headers = {
        'User-Agent': user_agent,
        'Referer': 'http://10.13.54.81/',
    }

    # Sign in
    English_session.post(login_url, data=login_data, headers=login_headers)



def answer(BookID):
    response = English_session.get(main_url + '/login/nsindex_student.php')
    pattern = 'BID=%d&CID=(.*?)&Quiz=N">.*?' % BookID
    CID = re.findall(pattern, response.text, re.S)
    book_url = main_url + '/book/index.php?BID=%d&CID=' % BookID + CID[0][0] + CID[0][1] + CID[0][2] + CID[0][3] + '&Quiz=N'

    # Open the book
    English_session.get(book_url)
    English_session.get(main_url + '/template/loggingajax.php?whichURL=/login/nsindex_student.php')
    English_session.get(main_url + '/book/book%d/index.php?Quiz=N&whichActionPage=' % BookID)

    #choose the book
    if BookID == 41:
        book = open('Books/STSJC3.txt', 'r')


    lines = book.readlines()
    for line in lines:
        if line == '' or line[0] == '#':
            continue
        content   = line.split('##')
        URL       = content[0].strip()
        UnitID    = content[1]
        TestID    = content[2]
        SectionID = TestID[0]
        SisterID  = TestID[2]
        KidID     = content[3]
        ItemID    = content[4]
        Answer    = content[5]

        payload = {
            'whichAction': 'checkMyProgress',
            'whichUnitID': UnitID,
            'whichTestID': ''
        }
        post_headers = {
            'User-Agent': user_agent,
            'Referer': URL,
        }
        English_session.post(main_url + "/book/book%d/nslsajax.php" % BookID, data=payload)
        url = main_url + "/book/book%d/unit_index.php?UnitID=" % BookID + UnitID
        English_session.get(url)
        base_data = {
            'UnitID': UnitID,
            'SectionID': SectionID,
            'SisterID': SisterID,
            'TestID': TestID,
            'KidID': KidID,
            'ItemID': ItemID,
        }
        answer_data = dict(base_data.items()+eval(Answer).items())

        # Submit answers
        English_session.post(URL, data=answer_data, headers=post_headers)


    # Finish and close the book
    book.close()



if __name__ == "__main__":
    English_session = requests.Session()
    username = raw_input("Please input your StudentID: ")
    # password = getpass.getpass("Please input your Password(Hided): ")
    password = raw_input("Please input your Password: ")
    # BookID = int(raw_input("Choose the book with BookID: "))
    signin(username, password)


    answer(41)