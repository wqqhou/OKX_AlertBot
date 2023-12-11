# We will use the SQLite database
import sqlite3

# Initialize database connection and cursor
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Create table "Users" with uid and balance rows
cur.execute('''CREATE TABLE IF NOT EXISTS Subscription(
                syb STRING,
                uid INTEGER
        )''')

def get_subscribers(syb):
    cur.execute(f'SELECT * FROM Subscription WHERE syb = {syb}')
    uid_list = cur.fetchone()
    if uid_list:
        return uid_list
    return False