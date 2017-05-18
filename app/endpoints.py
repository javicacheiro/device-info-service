from flask import jsonify, request
from . import api
from . import devices
from kvstore import KeyDoesNotExist
from werkzeug.exceptions import BadRequest


@api.route('/devices', methods=['GET'])
def get_devices():
    """Show the registered devices
       Using the '?full' option you can get all the stored meta info
    """
    names = devices.list()
    if request.args.get('full') is not None:
        data = {d: devices.show(d) for d in names}
    else:
        data = names
    return jsonify({'devices': data})


@api.route('/devices', methods=['POST'])
def register_device():
    """Register a new device

    Payload example:
    {
        'name': 'c17-1',
        'type': 'server',
        'group': 'hdp',
        'canonical_name': 'c17-1'
    }
    """
    payload = request.get_json()
    return _register_device(payload)


@api.route('/devices/<device>', methods=['GET'])
def get_device_properties(device):
    """Get the meta information of a given device"""
    results = devices.show(device)
    return jsonify(results)


@api.route('/devices/<device>', methods=['DELETE'])
def delete_device(device):
    """Delete the given device"""
    if device in devices.list():
        devices.delete(device)
        return '', 204
    else:
        raise BadRequest('The given device name does not exist')


@api.route('/devices/<device>', methods=['PUT'])
def update_device(device):
    """Update the information of a given device"""
    payload = request.get_json()
    if ('name' in payload) and (payload['name'] != device):
        raise BadRequest(
            'Device name does not match between URL and JSON payload')
    try:
        properties = devices.show(device)
        for k in payload:
            properties[k] = payload[k]
    except KeyDoesNotExist:
        properties = payload
    return _register_device(properties)


def _register_device(payload):
    """Register a device"""
    if _valid_device(payload):
        devices.register(payload)
        return '', 204
    else:
        raise BadRequest('Invalid device data')


def _valid_device(device):
    """Check if device data is valid"""
    required_fields = ('name', 'type', 'group', 'canonical_name')
    if all(field in device for field in required_fields):
        return True
    return False
