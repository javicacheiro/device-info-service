"""Device Information API

    list(): show the list of devices
    show(net): show the properties of given device
    register(net): register the given device

Schema:

    device = {
        'name': 'c17-1',
        'type': 'server',
        'group': 'hdp',
        'canonical_name': 'c17-1'
    }
"""
import kvstore

PREFIX = 'devices'


def connect(endpoint):
    """Set up the connection with the K/V store"""
    global _kv
    _kv = kvstore.Client(endpoint)


def register(device):
    """Register a new device

    Schema:

        device = {
            'name': 'c17-1',
            'type': 'server',
            'group': 'hdp',
            'canonical_name': 'c17-1'
        }
    """
    basedn = '{0}/{1}'.format(PREFIX, device['name'])
    for prop in device.keys():
        _kv.set('{0}/{1}'.format(basedn, prop), device[prop])


def delete(device):
    """Delete a device"""
    if device != '':
        _kv.delete('{0}/{1}'.format(PREFIX, device), recursive=True)


def list():
    """Returns the list of registered devices"""
    try:
        subtree = _kv.recurse(PREFIX)
    except kvstore.KeyDoesNotExist:
        subtree = {}
    return [subtree[k] for k in subtree.keys() if k.endswith('/name')]


def show(device):
    """Show the properties of a given device"""
    subtree = _kv.recurse('{0}/{1}'.format(PREFIX, device))
    properties = {}
    for k in subtree:
        properties[_parse_last_element(k)] = subtree[k]
    return properties


def _parse_last_element(key):
    return key.split('/')[-1]
