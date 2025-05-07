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

    return jsonify({"message": "Task created", "id": new_task.id}), 201

@bp.route('/<int:task_id>', methods = ['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id = user_id).first()

    if not task:
        return jsonify({"Error: Task does not exist"}), 404
        
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    if data.get('due_date'):
        task.due_date = datetime.fromisoformat(data['due_date'])

    db.session.commit()
    return jsonify({"message": "Task Updated Successfully!"}), 200

#delete task
@bp.route('/<int:task_id>', methods = ['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id = task_id, user_id = user_id).first()

    if not task:
        return jsonify({"Error:" : "Task not found"}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200

