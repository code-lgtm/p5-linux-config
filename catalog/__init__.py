from flask import Flask
from config import Config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

db = SQLAlchemy()

def create_app(confilg_file=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    Config.init_app(app)

    if confilg_file is not None:
        app.config.from_pyfile(confilg_file, silent=True)

    db.init_app(app)
    login_manager.init_app(app)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
