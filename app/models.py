from datetime import datetime
from .import db
from werkzeug.security import generate_password_hash, check_password_hash

#the user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)

    tasks = db.relationship('Task', backref = 'user', lazy = True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

#this is how I am modeling the tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = True)
    completed = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

