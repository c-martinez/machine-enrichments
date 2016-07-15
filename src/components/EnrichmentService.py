from flask import jsonify, request
from .machineenrichments import MachineEnrichments

import settings

"""
TODO: Document
"""

enrichments = MachineEnrichments()

def getStatus():
    # TODO: Check status of required stuff (DB, if we have one, for instance?)
    response = {
        'message'     : 'API is running',
        'status'      : 'success'
    }
    return jsonify(response)

def getCapabilities():
    # TODO: Get capabilities from MachineEnrichments
    nerdCapability = {
        'id'        : 'nerd',
        'parameters': [
            { 'type': '?textBlock',
              'name': 'text',
              'description': 'Text to be annotated' }
        ],
        'provides': [
            { 'type': 'List<String>',
              'name': 'Entities',
              'description': 'List of identified entitites' }
        ],
        'description': 'NERD - Named Entity Recognition and Disambiguation'
    }
    capabilities = []
    if settings.nerd_api_key!='':
        capabilities.append(nerdCapability)

    response = {
        'message'     : 'ok',
        'status'      : 'success',
        'capabilities': capabilities
    }
    return jsonify(response)

def sendAnnotation(capability):
    if capability=='nerd' and settings.nerd_api_key!='':
        body = request.get_json()

        annotationStatus = []
        for item in body['data']:
            # process item using capability...
            status = enrichments.processNerd(item['id'], item['content'])
            annotationStatus.append(status)

        response = {
              "status": "success",
              "message": "string",
              "annotationStatus": annotationStatus
            }
    else:
        response = {
            "status": "Error",
            "message": "Capability not available",
            "annotationStatus": []
            }
    return jsonify(response)

def getAnnotationStatus():
    body = request.get_json()
    tickets = body['tickets']
    ticketStatus = []
    for ticket in tickets:
        status = enrichments.getAnnotationStatus(ticket)
        ticketStatus.append(status)
    response = {
          "status": "success",
          "message": "string",
          "annotationStatus": ticketStatus
        }
    return jsonify(response)

def collectAnnotation():
    body = request.get_json()
    tickets = body['tickets']
    annotations = []
    for ticket in tickets:
        annotation = enrichments.collectAnnotation(ticket)
        annotations.append(annotation)
    response = {
          "status": "success",
          "message": "string",
          "annotations": annotations
        }
    return jsonify(response)
