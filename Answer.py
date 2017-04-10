#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import getpass
import sqlite3

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
    res = English_session.post(login_url, data=login_data, headers=login_headers)
    if res.text.find('Loading') != -1:
        print 'Login successfully !'
    else:
        print 'Wrong StudentID or Password !'
        name = raw_input("Please input your StudentID again: ")
        pwd = getpass.getpass("Please input your Password again (Hided): ")
        signin(name, pwd)


def answer(BookID, unit=[1]):
    response = English_session.get(main_url + '/login/nsindex_student.php')
    pattern = 'BID=%d&CID=(.*?)&Quiz=N">.*?' % BookID
    CID = re.findall(pattern, response.text, re.S)
    try:
        book_url = main_url + '/book/index.php?BID=%d&CID=' % BookID + CID[0][0] + CID[0][1] + CID[0][2] + CID[0][3] + '&Quiz=N'

        # Open the book
        English_session.get(book_url)
        English_session.get(main_url + '/template/loggingajax.php?whichURL=/login/nsindex_student.php')
        English_session.get(main_url + '/book/book%d/index.php?Quiz=N&whichActionPage=' % BookID)
    except:
        print 'You have NOT REGISTER for this book or our script encountered an unknown error !'
        print 'Please CHECK your account on the website and run the script again !'
        return

    # Get the post data from database
    cx = sqlite3.connect("data.sqlite3")
    cu = cx.cursor()
    if BookID < 30:
        cu.execute("SELECT * FROM TSJC" + str(BookID-22))
    else:
        cu.execute("SELECT * FROM STSJC" + str(BookID - 38))
    data = cu.fetchall()

    current_unit = '0'
    for answer in data:
        URL    = answer[1]
        UnitID = answer[2]
        if int(UnitID) not in unit:
            continue
        TestID = answer[3]
        KidID  = answer[4]
        ItemID = answer[5]
        Answer = eval(answer[6])

        # Can be deleted
        # payload = {
        #     'whichAction': 'checkMyProgress',
        #     'whichUnitID': UnitID,
        #     'whichTestID': ''
        # }
        # post_headers = {
        #     'User-Agent': user_agent,
        #     'Referer': URL,
        # }
        # English_session.post(main_url + "/book/book%d/jdls3ajax.php" % BookID, data=payload)
        # url = main_url + "/book/book%d/unit_index.php?UnitID=" % BookID + UnitID
        # English_session.get(url)

        answer_data = dict(Answer.items() + {
            'UnitID': UnitID,
            'SectionID': TestID[0],
            'SisterID': TestID[2],
            'TestID': TestID,
            'KidID': KidID,
            'ItemID': ItemID,
        }.items())

        # Submit answers
        English_session.post(URL, data=answer_data)
        
        # Mark the current unit and give hints
        if current_unit != UnitID and current_unit != '0':
            print 'Unit %s finished.' % current_unit
        current_unit = UnitID
    print 'Unit %s finished.' % current_unit
            
if __name__ == "__main__":
    # username = raw_input("Please input your StudentID: ")
    # if username == '':
    #     print "StudentID cannot be empty!"
    #     print "Please run the script again!"
    #     exit()
    # password = getpass.getpass("Please input your Password(hided, nhce111 as default): ")
    # if password == '':
    #     password = 'nhce111'
    # # password = raw_input("Please input your Password: ")
    # # print username, password

    # Login in
    English_session = requests.Session()
    signin(username, password)

    # print '听说教程1（23）'.decode('utf-8').encode('GBK')
    # print '听说教程2（24）'.decode('utf-8').encode('GBK')
    # print '听说教程3（25）'.decode('utf-8').encode('GBK')
    # print '听说教程4（26）'.decode('utf-8').encode('GBK')
    # print '视听说教程1（39）'.decode('utf-8').encode('GBK')
    # print '视听说教程2（40）'.decode('utf-8').encode('GBK')
    # print '视听说教程3（41）'.decode('utf-8').encode('GBK')
    # print '视听说教程4（42）'.decode('utf-8').encode('GBK')

    BookID = 0
    # try:
    #     num = raw_input("Choose the book with BookID: ")
    #     BookID = int(num)
    #     if BookID < 23 or 26 < BookID and BookID < 39 or BookID > 42:
    #         raise ValueError('Invalid value')
    # except ValueError, e:
    #     print "You have a wrong number!"
    #     print "Please run the script again!"
    #     exit()

    answer(26, [1,2,3,4,5])