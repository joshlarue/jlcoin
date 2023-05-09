from flask import Flask
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

    from routes import api
    app.register_blueprint(api)

    with app.app_context():
        db.init_app(app)


    #app.register_blueprint(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    #login_manager.init_app(app)

    #app.add_url_rule('/mine', 'mine', mine, methods=['GET'])
    #app.add_url_rule('/blocks', 'get_blocks', get_blocks, methods=['GET'])
    #app.add_url_rule('/txion', 'transactions', transactions, methods=['POST'])
    #node.register_blueprint(auth, url_prefix ='/auth')
    return app