import unittest
from flask import current_app
from catalog import create_app
from catalog import db

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('application.testing.cfg')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_environment(self):
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql:///catalogtest')

    def test_app_exists(self):
        self.assertFalse(current_app is None)