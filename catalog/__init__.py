"""
Intializes Application, Login Manager, SQLAlchemy, Bootstrap extensions
"""

from flask import Flask
from config import Config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask_wtf import CsrfProtect

# Initialize Flask-Login extension for management of user sessions
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# Integration with Bootstrap
bootstrap = Bootstrap()

# Initialize Flask-SQL Alchemy Extension
db = SQLAlchemy()

# Prevention of Cross-Site Request Forgery Attacks
csrf = CsrfProtect()


def create_app(confilg_file=None):
    """
    Creation of Application factory function. Allow mutliple application
    objects to be created and apply configuration changes dynamically

    :param confilg_file: Config File to apply dynamic changes

    :return: application object
    """

    # Initializes app and sets up the folder from where configuration
    # files would be picked up
    app = Flask(__name__, instance_relative_config=True)
    # Default Configurations
    app.config.from_object(Config)
    Config.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)

    # Read and apply configurations from the file provided in the application
    # factory
    if confilg_file is not None:
        app.config.from_pyfile(confilg_file, silent=True)

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
