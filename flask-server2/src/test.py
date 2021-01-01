import sqlite3
conn = sqlite3.connect('../db_file/mydb')
c = conn.cursor()
query = "select * from users"
c.execute(query)
rows = c.fetchall()
for row in rows:
    print(row)