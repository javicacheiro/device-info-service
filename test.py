#!/usr/bin/env python
from __future__ import print_function
import os
import tempfile
import subprocess
import time
import requests
import json


def start_consul_instance(acl_master_token=None):
    """Starts a consul instance"""
    # If not in the PATH indicate the location of the consul binary here
    consul = 'consul'

    tmpdir = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(tmpdir)

    ports = {'ports': {
        'http': 1984, 'server': 1985, 'serf_lan': 1986, 'serf_wan': 1987,
        'dns': -1 }}
    with open(tmpdir + '/config.json', 'w') as conffile:
        json.dump(ports, conffile)

    p = subprocess.Popen(
        [consul, 'agent', '-server', '-bootstrap', '-bind=127.0.0.1',
         '-config-dir=.', '-data-dir=./data'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    base_uri = 'http://127.0.0.1:1984/v1/'
    wait_until_consul_is_running(base_uri)
    os.chdir(cwd)
    return p, base_uri + 'kv'


def wait_until_consul_is_running(base_uri):
    """Wait for consul to start"""
    while True:
        time.sleep(0.1)
        try:
            response = requests.get(base_uri + 'status/leader')
        except requests.ConnectionError:
            continue
        if response.text.strip() != '""':
            break


if __name__ == '__main__':
    # Start a consul instance for integration teststs
    print('Starting Consul')
    p, consul_url = start_consul_instance()
    os.environ['CONSUL_URL'] = consul_url
    print('Consul started: {}'.format(os.environ['CONSUL_URL']))

    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

    import unittest
    from tests import suite
    unittest.TextTestRunner(verbosity=2).run(suite)

    COV.stop()
    COV.report()

    print('Stopping Consul')
    p.kill()
    print('Consul stopped')
