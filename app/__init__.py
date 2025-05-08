from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from .extensions import db, mail, scheduler
from .reminders import send_reminders
from .reminders import bp as reminders_bp

jwt = JWTManager()
mail = Mail()


def create_app():
    from .routes import auth, tasks

    app = Flask(__name__)
    app.config.from_object('config.Config')

    mail.init_app(app)
    scheduler.start()

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    mail.init_app(app)

    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(tasks.bp, url_prefix='/tasks')
    app.register_blueprint(reminders_bp)

    with app.app_context():
        db.create_all()

    scheduler.add_job(func=send_reminders, trigger="interval", minutes=60)
    return app

