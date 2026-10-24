import sqlite3
db=sqlite3.connect('mdb.db')
c=db.cursor()

# c.execute("""CREATE TABLE articles (
#     title text,
#     full_text text,
#     views integer,
#     avtor text
# )""")
# c.execute("INSERT INTO articles VALUES('dddd11','eeee22', 3333, 'four444')")
c.execute("SELECT * FROM articles")
print(c.fetchall())
db.commit()
db.close()