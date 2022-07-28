
import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute('Delete From menu')
print(cur.fetchall())
conn.close()