#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Entries
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, Entries=Entries)
manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
