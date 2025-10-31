import sqlite3

conn = sqlite3.connect('dream_waters_inventory.db')
c = conn.cursor()

c.execute('SELECT * FROM accounts')
rows = c.fetchall()

for row in rows:
    print(row)