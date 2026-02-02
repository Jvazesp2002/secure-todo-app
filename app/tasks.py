from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from models import SessionLocal, Task

tasks_bp = Blueprint("tasks", __name__)
@tasks_bp.route("/tasks")
@login_required
def list_tasks():
    db = SessionLocal()
    tasks = db.query(Task).filter_by(user_id=current_user.id).all()
    return render_template("tasks.html", tasks=tasks)

@tasks_bp.route("/tasks/create", methods=["POST"])
@login_required
def create_task():
    title = request.form["title"]
    description = request.form.get("description")

    db = SessionLocal()

    task = Task(
        title=title,
        description=description,
        user_id=current_user.id
    )

    db.add(task)
    db.commit()

    return redirect(url_for("tasks.list_tasks"))
