import sqlite3
db=sqlite3.connect('mydict.db')
c=db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS dict (
    n integer PRIMARY KEY,
    t text,
    en text,
    ru text,
    komm text
)""")
# c.execute("INSERT INTO dict VALUES(0,'english', 'russian', 'komment')")
c.execute("SELECT * FROM dict")
print(c.fetchall())
db.commit()
db.close()