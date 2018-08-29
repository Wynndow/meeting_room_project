#!/usr/bin/env python
from app import create_app
import os
from flask_script import Manager

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(application)

if __name__ == '__main__':
    manager.run()
