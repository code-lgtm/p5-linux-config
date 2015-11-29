from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin, current_user
from flask import current_app, url_for
from . import db
from . import login_manager
import os
from datetime import datetime

class Permission:
    VIEW_CATALOG = 0x01
    WRITE_ITEMS = 0x02
    MODERATE_CONTENT = 0x04
    ADMINISTER = 0x80


class User(UserMixin, db.Model):
    """ This class maps to user table in database containing information of
    registered users. Table consists of following columns

    id - Unique auto generated id of the User
    name - User name
    password_hash - Hash of the user password using werkabzeug framework.
        Actual password is never stored in the database
    email - Email address of the user. Unique contstraint is applied
    age - Users age
    role_id - One of admin, user. Taken from roles table
    """
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if os.getenv('FLASK_CONFIG') is not None and \
                            self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        if self.role is not None:
            return self.role.permissions is not None and \
                   (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


    def __repr__(self):
        return "<username : %s>" % self.name

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        if(permissions == Permission.VIEW_CATALOG or \
           permissions == Permission.VIEW_CATALOG):
            return True
        else:
            return False

    def is_administrator(self):
        return False

class Role(db.Model):
    """

    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.VIEW_CATALOG |
                     Permission.WRITE_ITEMS, True),
            'Moderator': (Permission.VIEW_CATALOG |
                          Permission.WRITE_ITEMS |
                          Permission.MODERATE_CONTENT, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %s>'% self.name

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    items = db.relationship('Item', backref='category', lazy='dynamic')

    def to_json(self):
        json_post = {
            'id' : self.id,
            'name' : self.name
        }
        return json_post

    def __repr__(self):
        return '<Category %s>' % self.name


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def isOwner(self):
        if not current_user.is_authenticated():
            return 0
        if int(current_user.get_id()) == self.owner_id:
            return 1
        return 0


    def to_json(self):
        json_post = {
            'id' : self.id,
            'name' : self.name,
            'isOwner' : self.isOwner(),
            'timestamp' : str(self.timestamp),
            'description' : self.description,
            'category' : self.category_id,
        }
        return json_post

    def __repr__(self):
        return '<Category %s>' % self.name


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))