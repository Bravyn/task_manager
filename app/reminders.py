from datetime import datetime, timedelta
from flask_mail import Message
from app.extensions import Mail
from app.models import Task, User, db

def send_reminders():
    now = datetime.utcnow()
    soon = now + timedelta(hours=24)

    tasks = Task.query.filter(
        Task.completed == False,
        Task.due_date != None,
        Task.due_date <= soon,
        Task.due_date >= now
    ).all()

    for task in tasks:
        user = User.query.get(task.user_id)
        if not user:
            continue

        msg  = Message(
            subject=f"Reminder: {task.title} is due soon!",
            recipients=[user.email],
            body=f"Hi there, Just a reminder that your task is due. Don't forget"
        )

        try:
            Mail.send(msg)
        except Exception as e:
            print(f"Error sending email to {user.email} {str(e)}")