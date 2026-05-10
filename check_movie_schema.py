import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("PRAGMA table_info('movie_app_movie')")
for row in cur.fetchall():
    print(row)
conn.close()
