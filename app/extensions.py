from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
scheduler = BackgroundScheduler()
db = SQLAlchemy()
