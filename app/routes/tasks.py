from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task, db
from datetime import datetime

bp = Blueprint('tasks', __name__)

#get all tasks for the logged in user
@bp.route('/', methods = ['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id = user_id).all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed,
            "created_at": t.created_at.isoformat(),
            "due_date": t.due_date.isoformat() if t.due_date else None  # Fixed here
        } for t in tasks])


#create a new task
@bp.route('/', methods = ['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_task = Task(
        title = data.get('title'),
        description = data.get('description'),
        due_date = datetime.fromisoformat(data.get('due_date')) if data.get('due_date') else None,
        user_id = user_id
    ) 
    db.session.add(new_task)
    db.session.commit()   

    return jsonify({"message": "Task created", id: new_task.id}), 201