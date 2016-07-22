from nerd import NERD
import settings
from threading import Thread

class MachineEnrichments():
    def __init__(self):
        self._counter = 0       # TODO: generate unique tickets
        self._dbStatus = {}     # TODO: use real DB (sqlite at least?)
        self._dbResults = {}
        self._dbOrigIds = {}

        self._nerdClient = NERD ('nerd.eurecom.fr', settings.nerd_api_key)

    def getNextTicketId(self):
        self._counter += 1
        return 'ticket-' + str(self._counter)

    def processNerd(self, itemId, content):
        content = _packJSONDict(content)
        ticketID = self.getNextTicketId()
        text = content['text']

        Thread(target=self._NERDThread,
               args=(text, ticketID)).start()
        self._dbOrigIds[ticketID] = itemId

        status = {
          "status": "accepted",
          "ticket": ticketID,
          "id": itemId,
        }
        return status


    def _NERDThread(self, text, ticketID):
        self._dbStatus[ticketID] = 'pending';

        try:
            text = text.encode('ascii', 'replace')
            extractedData = self._nerdClient.extract(text, 'combined', 30)
            self._nerdClient.http.close()
            #print 'FAKE NERD BEING USED!'
            #import time
            #time.sleep(50)
            #extractedData = 'Some data extracted via fake-NERD'

            # After NERD has completed...
            self._dbResults[ticketID] = extractedData
            self._dbStatus[ticketID] = 'ready'
        except Exception:
            self._dbResults[ticketID] = []
            self._dbStatus[ticketID] = 'failed'

    def getAnnotationStatus(self, ticketID):
        status = self._dbStatus[ticketID] if ticketID in self._dbStatus else 'unknown'
        return {
            "status": status,
            "ticket": ticketID
        }

    def collectAnnotation(self, ticketID):
        provenace = {
            'Tool': 'NERD'
        }
        itemId = self._dbOrigIds[ticketID] if ticketID in self._dbOrigIds else None
        content = {}
        if ticketID in self._dbResults:
            entities = self._dbResults[ticketID]
            content['Entities'] = entities

        return {
          "ticket": ticketID,
          "provenance": {
            "data": _unpackJSONDict(provenace)
          },
          "data": [
            {
              "content": _unpackJSONDict(content),
              "id": itemId
            }
          ]
        }

def _packJSONDict(jsonDict):
    ''' Convert JSON list of key-value pairs to python dictionary '''
    return { item['key']: item['value'] for item in jsonDict }

def _unpackJSONDict(pyDict):
    ''' Convert python dictionary to JSON list of key-value pairs'''
    return [ { "key": k, "value": v } for k,v in pyDict.iteritems() ]
