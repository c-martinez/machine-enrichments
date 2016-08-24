from flask import jsonify, request
from .machineenrichments import MachineEnrichments

import settings

"""
The following functions provide 'glue code', to connect the functionality
provided by the MachineEnrichments class to the Labs enrichment API described
in the swagger.yaml file.
"""

_enrichmentProvider = MachineEnrichments()


def getStatus():
    '''Response from the /api/status route'''
    response = {
        'message': 'API is running',
        'status': 'success'
    }
    return jsonify(response)


def getCapabilities():
    '''Response from the /api/capabilities route'''
    nerdCapability = {
        'id': 'nerd',
        'parameters': [
            {'type': '?textBlock',
              'name': 'text',
              'description': 'Text to be annotated'}
        ],
        'provides': [
            {'type': 'List<String>',
             'name': 'Entities',
             'description': 'List of identified entitites'}
        ],
        'description': 'NERD - Named Entity Recognition and Disambiguation'
    }
    capabilities = []
    if settings.nerd_api_key != '':
        capabilities.append(nerdCapability)

    response = {
        'message': 'ok',
        'status': 'success',
        'capabilities': capabilities
    }
    return jsonify(response)


def sendAnnotation(capability):
    '''Response from the /api/annotation/send/{capability} route.

    Currently implemented capabilities:

     - nerd
     '''
    if capability == 'nerd' and settings.nerd_api_key != '':
        body = request.get_json()

        annotationStatus = []
        for item in body['data']:
            # process item using capability...
            status = _enrichmentProvider.processNerd(
                item['id'], item['content'])
            annotationStatus.append(status)

        response = {
            "status": "success",
            "message": "Annotations received",
            "annotationStatus": annotationStatus
        }
    else:
        response = {
            "status": "error",
            "message": "Capability not available",
            "annotationStatus": []
        }
    return jsonify(response)


def getAnnotationStatus():
    '''Response from the /api/annotation/status route'''
    body = request.get_json()
    tickets = body['tickets']
    ticketStatus = []
    for ticket in tickets:
        status = _enrichmentProvider.getAnnotationStatus(ticket)
        ticketStatus.append(status)
    response = {
        "status": "success",
        "message": "Call succeeded",
        "annotationStatus": ticketStatus
    }
    return jsonify(response)


def collectAnnotation():
    '''Response from the /api/annotation/collect route'''
    body = request.get_json()
    tickets = body['tickets']
    annotations = []
    for ticket in tickets:
        annotation = _enrichmentProvider.collectAnnotation(ticket)
        if annotation is None:
            response = {
                "status": "error",
                "message": "No annotations were found for ticket: " + ticket,
                "annotationStatus": []
            }
            return jsonify(response)
        annotations.append(annotation)
    response = {
        "status": "success",
        "message": "Returning annotations",
        "annotations": annotations
    }
    return jsonify(response)
