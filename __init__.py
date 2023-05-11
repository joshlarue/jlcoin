from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    ## add a better secret key than that buster
    ## for dev purposes only

    app.config['SECRET_KEY'] = 'jlcoin'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    CORS(app)
    
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.init_app(app)
        import models
        db.create_all()

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

#reimplement, taken into extensions
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    return app