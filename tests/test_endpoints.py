import app
import unittest
import os
import requests
import json

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['CONSUL_URL'] = os.environ['CONSUL_URL']
        self.app = app.app.test_client()

    def tearDown(self):
        # To avoid a terrible disaster we hardcode the URL
        requests.delete('http://127.0.0.1:1984/v1/kv/?recurse=1')

    def test_no_devices(self):
        rv = self.app.get('/v1/devices')
        expected = {'devices': []}
        result = json.loads(rv.data)
        self.assertEqual(result, expected)

    def test_invalid_url(self):
        rv = self.app.get('/v1/INVALID')
        self.assertEqual(rv.status_code, 404)

    def test_register_device(self):
        device = {'name': 'c17-1.local', 'type': 'server', 'group': 'g1',
                  'canonical_name': 'c17-1'}
        rv = self.app.post('/v1/devices', data=json.dumps(device),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 204)
        rv = self.app.get('/v1/devices')
        expected = {'devices': [device['name']]}
        result = json.loads(rv.data)
        self.assertEqual(result, expected)

    def test_register_device_missing_name(self):
        device = {'type': 'server', 'group': 'g1', 'canonical_name': 'c17-1'}
        rv = self.app.post('/v1/devices', data=json.dumps(device),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 400)

    def test_list_devices_full(self):
        device = {'name': 'c17-1.local', 'type': 'server', 'group': 'g1',
                  'canonical_name': 'c17-1'}
        self.app.post('/v1/devices', data=json.dumps(device),
                      content_type='application/json')
        rv = self.app.get('/v1/devices?full')
        expected = {'devices': {device['name']: device}}
        result = json.loads(rv.data)
        self.assertEqual(result, expected)

    def test_delete_device(self):
        device1 = {'name': 'c17-1.local', 'type': 'server', 'group': 'g1',
                   'canonical_name': 'c17-1'}
        device2 = {'name': 'c17-2.local', 'type': 'server', 'group': 'g1',
                   'canonical_name': 'c17-2'}
        self.app.post('/v1/devices', data=json.dumps(device1),
                           content_type='application/json')
        self.app.post('/v1/devices', data=json.dumps(device2),
                           content_type='application/json')
        rv = self.app.delete('/v1/devices/{}'.format(device1['name']))
        self.assertEqual(rv.status_code, 204)
        rv = self.app.get('/v1/devices')
        expected = {'devices': [device2['name']]}
        result = json.loads(rv.data)
        self.assertEqual(result, expected)

    def test_get_device_properties(self):
        device = {'name': 'c17-1.local', 'type': 'server', 'group': 'g1',
                  'canonical_name': 'c17-1'}
        self.app.post('/v1/devices', data=json.dumps(device),
                      content_type='application/json')
        rv = self.app.get('/v1/devices/{}'.format(device['name']))
        expected = device
        result = json.loads(rv.data)
        self.assertEqual(result, expected)

    def test_get_wrong_device(self):
        device = {'name': 'c17-1.local', 'type': 'server', 'group': 'g1',
                  'canonical_name': 'c17-1'}
        self.app.post('/v1/devices', data=json.dumps(device),
                      content_type='application/json')
        rv = self.app.get('/v1/devices/WRONG_DEVICE')
        self.assertEqual(rv.status_code, 400)

    def test_update_device(self):
        device = {'name': 'c17-1.local', 'type': 'server', 'group': 'g1',
                  'canonical_name': 'c17-1'}
        self.app.post('/v1/devices', data=json.dumps(device),
                      content_type='application/json')
        device['group'] = 'g2'
        rv = self.app.put('/v1/devices/{}'.format(device['name']),
                          data=json.dumps(
                              {'name': device['name'], 'group': device['group']}),
                          content_type='application/json')
        self.assertEqual(rv.status_code, 204)
        rv = self.app.get('/v1/devices/{}'.format(device['name']))
        expected = device
        result = json.loads(rv.data)
        self.assertEqual(result, expected)

    def test_update_device_names_do_not_match(self):
        device = {'name': 'c17-1.local', 'type': 'server', 'group': 'g1',
                  'canonical_name': 'c17-1'}
        self.app.post('/v1/devices', data=json.dumps(device),
                      content_type='application/json')
        device['group'] = 'g2'
        rv = self.app.put('/v1/devices/{}'.format(device['name']),
                          data=json.dumps(
                              {'name': 'WRONG_NAME', 'group': device['group']}),
                          content_type='application/json')
        self.assertEqual(rv.status_code, 400)

    def test_not_supported_delete_devices(self):
        rv = self.app.delete('/v1/devices')
        self.assertEqual(rv.status_code, 405)

