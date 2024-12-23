
from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS

# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_bootstrap import Bootstrap4

from app.config import Config



from flask_migrate import Migrate
# Bootstrap()
db = SQLAlchemy()

# bcrypt =Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'



def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # bcrypt.init_app(app)
    login_manager.init_app(app)
    Session(app)
    CORS(app)
    app.app_context().push()
    migrate = Migrate(app, db)
    from app.users.routes import user
    from app.exam.routes import exam
    from app.errors.handlers import errors

    app.register_blueprint(user)
    app.register_blueprint(exam)
    app.register_blueprint(errors)

    return app
