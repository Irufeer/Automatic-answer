#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from ttk import *

def center_window(w=300, h=200):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def btn():
    pass

root = Tk()
root.title('大英刷题脚本')

label_username = Label(root, text='用户名:')
label_password = Label(root, text='密码:')

books = StringVar()
bookChosen = Combobox(root, width=12, textvariable=books)
bookChosen['values'] = ('视听说教程1', '视听说教程2', '视听说教程3', '视听说教程4',
                        '听说教程1', '听说教程2', '听说教程3', '听说教程4')
bookChosen.grid(column=1, row=1)
bookChosen.current(0)
button_start = Button(root, text='开始', command=btn())


label_username.pack()
label_password.pack()
bookChosen.pack()
button_start.pack()



center_window(300, 120)
root.mainloop()
