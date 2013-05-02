import sqlite3, os
s
db = sqlite3.connect('data.db')
c = db.cursor()
c.execute('CREATE TABLE Inventory (mfg TEXT, lqr TEXT, amt TEXT)')
c.execute('CREATE TABLE Type (mfg TEXT, lqr TEXT, typ TEXT)')
c.execute('CREATE TABLE Recipe (name TEXT, score INTEGER, votes INTEGER, ing TEXT)')
c.close()
db.commit()

