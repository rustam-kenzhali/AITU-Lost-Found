from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Configuration
SECRET_KEY = '%G#Am@e)Of(*/T*hrone$..(1000/0)Mops'
DB_NAME = 'database.db'

# Data Base
db = SQLAlchemy()

def create_app():           # creat flask WSGI
    app = Flask(__name__)   # __name__ runing file name
    app.config['SECRET_KEY'] = SECRET_KEY  # ecrpt session data and coockies
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)  # initialisation DB by giving Flask Aplication

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # acsess to all URL that's store in views blueprint file
    app.register_blueprint(auth, url_prefix='/')  # prefix it's nessesary item when we @auth.route("/") page

    from .models import User, Post

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where do we need to go if we not log in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):   # if database doesn't exist. We create it
    if not path.exists(f'var/website-instance/{DB_NAME}'):
        with app.app_context():
            db.create_all()
        print('Created Database!')