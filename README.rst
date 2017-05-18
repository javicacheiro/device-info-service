Device Info Service REST API
============================

Purpose
-------
The objective of this service is to provide a REST API to retrieve
meta information about a given device

REST API
--------
Endpoint: http://devices:5000/v1/

::
    GET devices
    {
        "devices": ["c13-1", "c13-2", "c13-3"]
    }

    GET devices?full
    {
        "devices": {
            "c13-1": {
                "canonical_name": "c13-1", 
                "group": "gluster", 
                "name": "c13-1", 
                "type": "server"
            }, 
            "c13-2": {
                "canonical_name": "c13-2", 
                "group": "hdp", 
                "name": "c13-2", 
                "type": "server"
            } 
    }

    POST devices
    {
        "name": "c13-1", 
        "type": "server"
        "group": "gluster", 
        "canonical_name": "c13-1", 
    }

    PUT devices/<name>
    {
        "name": "c13-1", 
        "group": "hdp", 
    }

    GET devices/<name>
    {
        "name": "c13-1", 
        "type": "server"
        "group": "hdp", 
        "canonical_name": "c13-1", 
    }

Examples
--------

::
    http http://localhost:5000/v1/devices
    http http://localhost:5000/v1/devices?full
    http http://localhost:5000/v1/devices/c13-1
    http --json POST http://localhost:5000/v1/devices name=c14-1 type=server group=hdp_testing canonical_name=c14-1
    http --json PUT http://localhost:5000/v1/devices/c14-1 group=gluster

KV Store
--------
/devices/<name>/

Deployment
----------

Installation::

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn

Running the application in production:

    su - restuser
    cd <install_dir>
    . venv/bin/activate
    FLASK_CONFIG=production gunicorn --workers=2 --bind=:5000 wsgi:application


Building a docker image
-----------------------
```
docker build -t device-info-service:0.1.0 .
docker tag ae2476dfecab docker-registry.cesga.es:5000/device-info-service:0.1.0
docker push docker-registry.cesga.es:5000/device-info-service:0.1.0

```

Running the service
-------------------
```
docker-executor run instances/sistemas/devices/0.1.0/1/nodes/networks1
docker-executor run instances/sistemas/devices/0.1.0/1/nodes/networks2
```
