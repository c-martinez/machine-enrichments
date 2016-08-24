import sqlite3

_db = sqlite3.connect('enrichments.db')

c = _db.cursor()

# Create table
c.execute('''
        CREATE TABLE tickets
        (
        ticketID integer primary key autoincrement,
        origID,
        status,
        data,
        prov
        )
        ''')
