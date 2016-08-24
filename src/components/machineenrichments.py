from nerd import NERD
from .ticketcache import TicketCache
from utils.utils import flattenNestedDict, packJSONDict, unpackJSONDict, \
                        asIndexedDict
import settings
from threading import Thread


class MachineEnrichments():
    '''This class provides functionality for machine enrichment capabilities.
    Currently available enrichment capabilities:

     - NERD - provided by `processNerd`

    A TicketCache is used to keep track of the status and results of the data
    being annotated.'''

    def __init__(self):
        '''Create new MachineEnrichments instance and initialize required
        components.'''
        self._cache = TicketCache()
        self._nerdClient = NERD('nerd.eurecom.fr', settings.nerd_api_key)

    def processNerd(self, itemId, content):
        '''Use NERD client to annotate the given content to identify entities.
        A itemId must be provided which will be used to identify the original
        ID of the content. Additionally, a ticketID is generated which serves
        as an internal identifier within MachineEnrichments.'''
        content = packJSONDict(content)
        ticketID = self._cache.getNextTicketId()
        text = content['text']

        # Perform NERD in separate thread
        Thread(target=self._NERDThread,
               args=(text, ticketID)).start()
        self._cache.updateTicket(ticketID, 'origId', itemId)

        status = {
            "status": "accepted",
            "ticket": ticketID,
            "id": itemId,
        }
        return status

    def _NERDThread(self, text, ticketID):
        '''Perform call to NERD service in a thread. Thread calls NERD using
        the given text and updates the given ticketID when annotation is
        complete.'''
        # Initialize cache with ticket status as `pending`
        self._cache.updateTicket(ticketID, 'status', 'pending')

        try:
            text = text.encode('ascii', 'replace')
            extractedData = self._nerdClient.extract(text, 'combined', 30)
            self._nerdClient.http.close()

            # After NERD has completed...
            # update in cache ticket status and data
            self._cache.updateTicket(ticketID, 'data', extractedData)
            self._cache.updateTicket(ticketID, 'status', 'ready')
            self._cache.updateTicket(ticketID, 'prov', {
                'activityId': self._cache.getNextActivityId()
            })
        except Exception:
            # update in cache ticket status and data
            self._cache.updateTicket(ticketID, 'data', [])
            self._cache.updateTicket(ticketID, 'status', 'failed')

    def getAnnotationStatus(self, ticketID):
        '''Check (in the cache) the status of the given ticketID.'''
        status = self._cache.getStatus(ticketID)
        status = 'Unknown' if status is None else status
        return {
            "status": status,
            "ticket": ticketID
        }

    def collectAnnotation(self, ticketID):
        '''Check in the cache if the given ticketID is ready for collection and,
        if it is, return the ticket's content and provenance data.'''
        itemId, prov, content = self._cache.getData(ticketID)

        if itemId is None:
            return None
        content = {'Entities': asIndexedDict(content)}
        prov = {
            'prov:wasAttibutedTo': 'dive:nerdTool',
            'prov:wasGeneratedBy': 'dive:myActivity' + prov['activityId'],
            'dive:settings': {
                'URL': 'nerd.eurecom.fr',
                'extractor': 'combined',
                'timeout': 30
            }
        }

        return {
            "ticket": ticketID,
            "provenance": {
                "data": unpackJSONDict(flattenNestedDict(prov))
            },
            "data": [
                {
                    "content": unpackJSONDict(flattenNestedDict(content)),
                    "id": itemId
                }
            ]
        }
