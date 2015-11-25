from catalog import create_app
from flask.ext.script import Server, Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from catalog.model import User, Role, Item, Category
from catalog import model
from catalog import db

import os

app = create_app(os.getenv('FLASK_CONFIG') or None)
manager = Manager(app)
server = Server(host='0.0.0.0', port=5000)
manager.add_command("runserver", server)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def _make_context():
    return dict(app=app, model=model, db=db, User=User, Role=Role,
                Item= Item, Category=Category)

@manager.command
def test():
    """ Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command("shell" , Shell(make_context=_make_context))

if __name__ == '__main__':
    # print app.config['FOUND']
    manager.run()
