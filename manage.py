"""
Script to create and launch applications, run unit tests, perform db
migration or launch python shell.

Run command:
    1) python manage.py runserver to launch application
    2) python manage.py db migrate to detect changes in  schema
    3) python manage.py db upgrade to apply detected changes in  schema
    4) python manage.py test to run unit tests
    5) python manage.py shell to launch python shell with key modules imported
"""
from catalog import create_app
from flask.ext.script import Server, Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from catalog.model import User, Role, Item, Category
from catalog import model
from catalog import db

import os
# Configuration can be provided dynamically an environment variable
app = create_app(os.getenv('FLASK_CONFIG') or None)
manager = Manager(app)
server = Server(host='0.0.0.0', port=5000)
manager.add_command("runserver", server)

# Initializes Flask-Migrate extension to automatically handle
# modifications in schema
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Default imports available after launching the shell
def _make_context():
    return dict(app=app, model=model, db=db, User=User, Role=Role,
                Item=Item, Category=Category)


# Add command for detecting and running unit tests
@manager.command
def test():
    """ Run unit tests"""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# Set up roles and push initial data into database
@manager.command
def deploy():
    from flask.ext.migrate import upgrade
    upgrade()

    from catalog import sample_data as data
    data.main()


manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
