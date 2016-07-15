import ast
import os
import json
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def create_client_secret_json():
    client_secret_file_path = os.path.join(os.path.dirname(__file__), '../client_secret.json')
    client_secret_dict = ast.literal_eval(os.environ['MR_CLIENT_SECRET_JSON'])
    with open(client_secret_file_path, 'w') as outfile:
        json.dump(client_secret_dict, outfile, indent=4)
        outfile.close()
