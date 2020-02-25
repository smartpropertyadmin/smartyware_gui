from flask import Flask
# from flaskwebgui import FlaskUI
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_project.config import Config
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_principal import Principal



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # ui = FlaskUI(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Principal(app)

    from flask_project.users.routes import users
    from flask_project.posts.routes import posts
    from flask_project.main.routes import main
    from flask_project.mcst.routes import mcst
    from flask_project.temp.routes import temp
    from flask_project.errors.handlers import errors
    from flask_project.models import User, Role
    # from flask_project.copier.routes import copier
    def user_datastore():
        return  SQLAlchemySessionUserDatastore( db, User, Role)
        security = Security(app, user_datastore)
    # with app.app_context():
    #     db.create_all()
    #     print('this')

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(mcst)
    app.register_blueprint(temp)
    # app.register_blueprint(copier)
    return app



