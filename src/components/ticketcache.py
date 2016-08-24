import sqlite3
import json


class TicketCache():
    '''This class provides storage facility for data being annotated.'''

    def __init__(self):
        '''Create new instance of TicketCache'''
        # Possibly activity counter should be on DB ?
        self._counter = 0

    def _getDB(self):
        '''Connect to DB'''
        db = sqlite3.connect('enrichments.db', check_same_thread=False)
        return db

    def getNextTicketId(self):
        '''Create a new (blank) entry in cache table and return the unique
        ticketID for the newly created entry.'''
        db = self._getDB()
        c = db.cursor()
        c.execute(
            "INSERT INTO tickets (origID,status,data,prov) "
            "VALUES ('','','','')")
        db.commit()
        return 'ticket-' + str(c.lastrowid)

    def getNextActivityId(self):
        '''Generate a new unique activity identifier'''
        self._counter += 1
        return 'activity-' + str(self._counter)

    def updateTicket(self, ticketID, column, data):
        '''Update an entry on the cache table.'''
        db = self._getDB()
        c = db.cursor()
        ticketID = ticketID.replace('ticket-', '')
        if column == 'data' or column == 'prov':
            data = json.dumps(data)
        c.execute("UPDATE tickets SET %s='%s' WHERE ticketID=%s" %
                  (column, data, ticketID))
        db.commit()

    def getStatus(self, ticketID):
        '''Retrieve `status` column of the cache table for the given
        ticketID.'''
        c = self._getDB().cursor()
        ticketID = ticketID.replace('ticket-', '')
        c.execute('SELECT status FROM tickets WHERE ticketID=?', [ticketID])
        result = c.fetchone()
        return result[0] if result is not None else None

    def getData(self, ticketID):
        '''Retrieve `origID`, `data` and `prov` columns of the cache table
        for the given ticketID.'''
        c = self._getDB().cursor()
        ticketID = ticketID.replace('ticket-', '')

        c.execute(
            'SELECT origID,data,prov FROM tickets WHERE ticketID=?',
            [ticketID])
        result = c.fetchone()
        if result is not None:
            itemId, content, prov = result
            content = json.loads(content)
            prov = json.loads(prov)
        else:
            itemId, prov, content = None, None, None

        return itemId, prov, content
