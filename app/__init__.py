import os
from flask import Flask
from flask import Blueprint

app = Flask(__name__)
# Read configuration to apply from environment
config_name = os.environ.get('FLASK_CONFIG', 'development')
# apply configuration
cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
app.config.from_pyfile(cfg)
# Overwrite CONSUL_URL config option if present in the env
if 'CONSUL_URL' in os.environ:
    app.config['CONSUL_URL'] = os.environ['CONSUL_URL']

# Connect to Consul
from . import devices
devices.connect(app.config['CONSUL_URL'])

# Create a blueprint
api = Blueprint('api', __name__)
# Import the endpoints belonging to this blueprint
from . import endpoints
from . import errors

# register blueprints
app.register_blueprint(api, url_prefix='/v1')
