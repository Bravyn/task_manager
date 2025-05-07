from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app():
    from .routes import auth, tasks

    app = Flask(__name__)
    app.config.from_object('config.Config')


    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    mail.init_app(app)

    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(tasks.bp, url_prefix='/tasks')

    with app.app_context():
        db.create_all()

    return app

