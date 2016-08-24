def flattenNestedDict(d, base=''):
    '''The following dictionary:
        {
            'a1': {
                'b1': 'x'
            },
            'a2': {
                'b1': 'x',
                'b2': 'y',
                'b3': 'z',
            },
            'a3': {
                'b1': 'x',
                'b2': 'x',
                'b3': {
                    'c1': 1,
                    'c2': 1
                },
            }
        }

    Will yield the following flat dict:
        {
            'a1.b1': 'x'
            'a2.b1': 'x'
            'a2.b2': 'y'
            'a2.b3': 'z'
            'a3.b1': 'x'
            'a3.b2': 'x'
            'a3.b3.c1': 1
            'a3.b3.c2': 1
        }
    '''
    if not isinstance(d, dict):
        raise Exception('Cannot flatten non-dict')

    flatDict = {}
    for key, value in d.iteritems():
        if isinstance(value, dict):
            tmp = flattenNestedDict(value, base=base + key + '.')
            flatDict.update(tmp)
        else:
            flatDict[base + key] = value
    return flatDict


def asIndexedDict(value):
    ''' Convert python list into index: item dictionary
    E.g:
    The following list:
        [ 'a', 'b', 'c' ]
    will become:
        {
            '0': 'a',
            '1': 'b',
            '2': 'c'
        }
    '''
    if isinstance(value, list):
        return {str(n): item for n, item in enumerate(value)}
    else:
        return {}


def unpackJSONDict(pyDict):
    '''Convert python dictionary to JSON list of key-value pairs:
    E.g:
    The following dictionary:
        {
            '0': 'a',
            '1': 'b',
            '2': 'c'
        }
    will yield the following:
        [
            {'key': '0', 'value': 'a'},
            {'key': '1', 'value': 'b'},
            {'key': '2', 'value': 'c'}
        ]
    '''
    return [{"key": k, "value": v} for k, v in pyDict.iteritems()]


def packJSONDict(jsonDict):
    '''Convert JSON list of key-value pairs to python dictionary:
    E.g:
    The following list of key-value pairs:
        [
            {'key': '0', 'value': 'a'},
            {'key': '1', 'value': 'b'},
            {'key': '2', 'value': 'c'}
        ]
    will yield the following:
        {
            '0': 'a',
            '1': 'b',
            '2': 'c'
        }
    '''
    return {item['key']: item['value'] for item in jsonDict}
