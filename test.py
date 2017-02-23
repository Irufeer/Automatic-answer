import sqlite3

cx = sqlite3.connect("data.sqlite3")
cu = cx.cursor()

cu.execute("select * from TSJC4")
data = cu.fetchall()
for answer in data:
    URL       = answer[1]
    UnitID    = answer[2]
    TestID    = answer[3]
    KidID     = answer[4]
    ItemID    = answer[5]
    Answer    = eval(answer[6])



