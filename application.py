#!/usr/bin/env python
from app import create_app, create_client_secret_json
import os
from flask.ext.script import Manager

create_client_secret_json()
application = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(application)

if __name__ == '__main__':
    manager.run()
