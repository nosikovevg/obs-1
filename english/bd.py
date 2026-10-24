import sqlite3
from tkinter import *
db=sqlite3.connect('mydict.db')
c=db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS dict (
    n integer PRIMARY KEY,
    t text,
    en text,
    ru text,
    komm text
)""")
# способ 1
# c.execute("INSERT INTO dict VALUES(0,'00:00:00','english', 'russian', 'komment')")

# способ 2
# sql_req = "INSERT INTO dict VALUES(?, ?, ?, ?, ?)"
# c.execute(sql_req, (0, '00:00:00', 'english', 'russian', 'komment'))

####################################################
from tkinter import *
root = Tk()
root.title("Урок по tkinter")
root.geometry("400x200+700+500")

root.mainloop()
####################################################
c.execute("SELECT * FROM dict")
print(c.fetchall())
db.commit()
db.close()