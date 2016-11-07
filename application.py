#!/usr/bin/env python
from app import create_app
import os
from flask.ext.script import Manager
from apscheduler.schedulers.background import BackgroundScheduler
from app.lib.email_trigger import EmailTrigger

scheduler = BackgroundScheduler()
scheduler.add_job(EmailTrigger.call, 'cron', hour=7, minute=30, timezone='Europe/London')
scheduler.start()

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(application)

if __name__ == '__main__':
    manager.run()
