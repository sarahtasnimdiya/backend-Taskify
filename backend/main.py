from flask import request, jsonify
from config import app, db
from model import Task
from datetime import datetime

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    json_tasks = list(map(lambda task: task.to_json(), tasks))
    return jsonify({"Tasks":json_tasks})

@app.route('/create-tasks', methods=['POST'])
def create_task():
    title = request.json.get("title")
    notes = request.json.get("notes")
    time = request.json.get("time")
    done = request.json.get("done")

    if not title or not time:
        return jsonify({"Message": "Missing data"}), 400


    new_task = Task(title=title, notes=notes, time=datetime.fromisoformat(time), done=done)
    try:
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({"message": "Task created successfully"}), 201


@app.route('/update-task/<int:user_id>', methods=['PATCH'])
def update_task(user_id):
    task = Task.query.get(user_id)

    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    data= request.json
    task.title = data.get("title", task.title)
    task.notes = data.get("notes", task.notes)
    task.time = data.get("time", task.time)
    task.done = data.get("done", task.done)

    db.session.commit()

    return jsonify({"message": "Task updated successfully"}), 200

@app.route('/delete-task/<int:user_id>', methods=['DELETE'])
def delete_task(user_id):
    task = Task.query.get(user_id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
