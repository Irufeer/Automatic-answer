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
        content   = line.split()
        URL       = content[0]
        UnitID    = content[1]
        KidID     = content[2]
        ItemID    = content[3]
        Answer    = content[4]
        SectionID = URL[33]
        SisterID  = URL[34]
        TestID    = SectionID + '.' + SisterID
        Item_N    = 'Item_' + ItemID

        payload = {
            'whichAction': 'checkMyProgress',
            'whichUnitID': UnitID,
            'whichTestID': ''
        }
        post_headers = {
            'User-Agent': user_agent,
            'Referer': URL,
        }
        English_session.post(main_url + "/book/book%d/jdls3ajax.php" % BookID, data=payload)
        url = main_url + "/book/book%d/unit_index.php?UnitID=" % BookID + UnitID
        English_session.get(url)
        base_data = {
            'UnitID': UnitID,
            'SectionID': SectionID,
            'SisterID': SisterID,
            'TestID': TestID,
            'KidID': '1',
        }
        if TestID == '2.1':
            answer_data = dict(base_data.items()+{
                'KidID': KidID,
                'ItemID': ItemID,
                Item_N: Answer,
            }.items())
        elif TestID == '2.2' or TestID == '2.3':
            item = [('Item_'+ItemID)]*5
            for i in range(1,5):
                item[i] = 'Item_' + str(int(ItemID)+i)
            answer_data = dict(base_data.items()+{
                'ItemID': '',
                item[0]: Answer[0],
                item[1]: Answer[1],
                item[2]: Answer[2],
                item[3]: Answer[3],
                item[4]: Answer[4],
            }.items())
        elif TestID == '2.4':
            answer = line.find('answer:')
            answer = line[answer+7:].split('#')
            answer_data = dict(base_data.items()+{
                'ItemID': ItemID,
                'Item_0':answer[0],
                'Item_1': answer[1],
                'Item_2': answer[2],
                'Item_3': answer[3],
                'Item_4': answer[4],
            }.items())
        elif TestID == '5.1' or TestID == '5.2':
            answer_data = dict(base_data.items()+{
                'ItemID': ItemID,
                'Item_1': Answer[0],
                'Item_2': Answer[1],
                'Item_3': Answer[2],
                'Item_4': Answer[3],
                'Item_5': Answer[4],
            }.items())
        elif TestID == '5.3':
            answer = line.find('answer:')
            answer = line[answer + 7:].split('#')
            answer_data = dict(base_data.items()+{
                'ItemID': ItemID,
                'Item_0': answer[0],
                'Item_1': answer[1],
                'Item_2': answer[2],
                'Item_3': answer[3],
                'Item_4': answer[4],
                'Item_5': answer[5],
                'Item_6': answer[6],
                'Item_7': answer[7],
                'Item_8': answer[8],
                'Item_9': answer[9],
            }.items())

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