import sqlite3, os
db = sqlite3.connect('data.db')
c = db.cursor()
c.execute('CREATE TABLE if not exists Inventory (mfg TEXT, lqr TEXT, amt TEXT)')
c.execute('CREATE TABLE if not exists Type (mfg TEXT, lqr TEXT, typ TEXT)')
c.execute('CREATE TABLE if not exists Recipe (name TEXT, score INTEGER, votes INTEGER, ing TEXT)')
c.close()
db.commit()

