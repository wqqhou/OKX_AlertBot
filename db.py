# We will use the SQLite database
import sqlite3

# Initialize database connection and cursor
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Create table "Subscription" with uid and balance rows
cur.execute('''CREATE TABLE IF NOT EXISTS Subscription(
                syb STRING,
                uid INTEGER
        )''')

def get_subscribers(syb):
    cur.execute(f'SELECT * FROM Subscription WHERE syb = "{syb}"')
    uid_list = cur.fetchone()
    if uid_list:
        return uid_list
    return False

def add_subscriber(syb, uid):
    syb = syb
    list = [get_subscribers(syb)]
    new_list = list.append(uid)
    cur.execute(f'UPDATE Subscription SET uid = {new_list} WHERE syb = "{syb}"')
    con.commit()

def check_subscriber(syb, uid):
    list = get_subscribers(syb)
    if list:
        if uid in list:
            return True
    return False

def remove_subscriber(syb, uid):
    list = get_subscribers(syb)
    if list:
        if uid in list:
            list.remove(uid)
            cur.execute(f'UPDATE Subscription SET uid = {list} WHERE syb = "{syb}"')
            con.commit()
            return True
    return False