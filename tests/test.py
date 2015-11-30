"""
Application Test Cases
"""

import unittest
from flask import current_app
from catalog import create_app
from catalog import db
from flask.ext.login import current_user, login_user, logout_user
from catalog.model import User, Category, Item

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

    def test_login(self):
        """
        Checks log in and log out functionality

        :return:
        """
        u = User(email='j@h.com', password='cat')
        db.session.add(u)
        db.session.commit()

        login_user(u)
        test_u = User.query.filter_by(email='j@h.com').first()
        self.assertEqual(u.id, int(current_user.get_id()))
        logout_user()
        self.assertIsNone(current_user.get_id())