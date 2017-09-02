import sqlite3
cx = sqlite3.connect("data.sqlite3")
cu = cx.cursor()
cu.execute("SELECT * FROM TSJC4")
data = cu.fetchall()
for answer in data:
    # print(answer)
    for item in answer:
        